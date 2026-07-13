"""Client oracle abstrait (X-53).

Toute interaction LLM passe par cette couche :
- modèle interchangeable par config YAML (aucun changement du code appelant) ;
- comptabilité tokens/coût par appel selon pricing.yaml, agrégée par task_id ;
- plafond budget_usd_per_task : appel REFUSÉ (BudgetExceededError) si dépassé ;
- cache SQLite (clé = hash(model + prompt + params)) — un prompt n'est jamais
  payé deux fois ; désactivable (use_cache=False / --no-cache) ;
- retry backoff exponentiel sur 429/5xx (max 5) ;
- journalisation JSON lines de chaque appel ;
- prompts versionnés chargés depuis prompts/<id>_<version>/.
"""

from __future__ import annotations

import hashlib
import json
import sqlite3
import time
from collections import defaultdict
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import Any, TextIO

import yaml

PACKAGE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = PACKAGE_DIR.parents[1]
PRICING_PATH = PACKAGE_DIR / "pricing.yaml"
PROMPTS_DIR = PROJECT_ROOT / "prompts"
DEFAULT_CACHE_PATH = PROJECT_ROOT / "oracle_cache.db"
DEFAULT_LOG_PATH = PROJECT_ROOT / "oracle_calls.jsonl"

MAX_RETRIES = 5


class BudgetExceededError(RuntimeError):
    """Le plafond budget_usd_per_task est atteint : appel refusé."""


class TransientOracleError(RuntimeError):
    """Erreur 429/5xx — retryable avec backoff exponentiel."""


@dataclass(frozen=True)
class OracleConfig:
    model: str
    max_tokens: int = 4096
    temperature: float = 0.0
    budget_usd_per_task: float = 0.25  # plafond dur, appel refusé si dépassé

    @classmethod
    def from_yaml(cls, path: Path | str) -> OracleConfig:
        raw = yaml.safe_load(Path(path).read_text())
        return cls(**raw)


@dataclass(frozen=True)
class OracleResponse:
    text: str
    input_tokens: int
    output_tokens: int
    cost_usd: float
    cached: bool


# Un transport prend la requête {model, max_tokens, temperature, prompt} et
# retourne {text, input_tokens, output_tokens}. Le transport réel appelle
# l'API Anthropic ; les tests injectent un mock — aucun appel réseau.
Transport = Callable[[dict[str, Any]], dict[str, Any]]


def anthropic_transport(request: dict[str, Any]) -> dict[str, Any]:
    """Transport réel : API Anthropic Messages (clé via ANTHROPIC_API_KEY)."""
    import anthropic

    client = anthropic.Anthropic()
    try:
        response = client.messages.create(
            model=request["model"],
            max_tokens=request["max_tokens"],
            temperature=request["temperature"],
            messages=[{"role": "user", "content": request["prompt"]}],
        )
    except anthropic.RateLimitError as exc:
        raise TransientOracleError(str(exc)) from exc
    except anthropic.APIStatusError as exc:
        if exc.status_code >= 500:
            raise TransientOracleError(str(exc)) from exc
        raise
    text = "".join(block.text for block in response.content if block.type == "text")
    return {
        "text": text,
        "input_tokens": response.usage.input_tokens,
        "output_tokens": response.usage.output_tokens,
    }


def load_pricing(path: Path | None = None) -> dict[str, dict[str, float]]:
    return yaml.safe_load((path or PRICING_PATH).read_text())


def load_prompt(prompt_ref: str) -> dict[str, Any]:
    """Charge un prompt versionné depuis prompts/<id>_<version>/.

    Retourne {id, version, template, sha256}. Le hash journalisé garantit le
    gel des prompts pendant une étude comparative.
    """
    prompt_dir = PROMPTS_DIR / prompt_ref
    template = (prompt_dir / "template.txt").read_text()
    meta = yaml.safe_load((prompt_dir / "meta.yaml").read_text())
    return {
        "id": meta["id"],
        "version": meta["version"],
        "template": template,
        "sha256": hashlib.sha256(template.encode()).hexdigest(),
    }


class OracleClient:
    def __init__(
        self,
        config: OracleConfig,
        transport: Transport | None = None,
        cache_path: Path | str | None = None,
        log_stream: TextIO | None = None,
        use_cache: bool = True,
        pricing: dict[str, dict[str, float]] | None = None,
    ) -> None:
        self.config = config
        self.transport = transport or anthropic_transport
        self.use_cache = use_cache
        self.pricing = pricing or load_pricing()
        if config.model not in self.pricing:
            raise KeyError(f"modèle absent de pricing.yaml : {config.model!r}")
        self._log_stream = log_stream
        self._log_path = DEFAULT_LOG_PATH
        self.cost_by_task: dict[str, float] = defaultdict(float)
        self.total_cost_usd = 0.0
        self.network_calls = 0
        self._db = sqlite3.connect(str(cache_path or DEFAULT_CACHE_PATH))
        self._db.execute("CREATE TABLE IF NOT EXISTS cache (key TEXT PRIMARY KEY, value TEXT)")
        self._db.commit()

    # -- comptabilité ------------------------------------------------------
    def _cost(self, input_tokens: int, output_tokens: int) -> float:
        price = self.pricing[self.config.model]
        return (
            input_tokens * price["input_usd_per_mtok"]
            + output_tokens * price["output_usd_per_mtok"]
        ) / 1_000_000

    # -- cache -------------------------------------------------------------
    def _cache_key(self, request: dict[str, Any]) -> str:
        payload = json.dumps(request, sort_keys=True, ensure_ascii=False)
        return hashlib.sha256(payload.encode()).hexdigest()

    def _cache_get(self, key: str) -> dict[str, Any] | None:
        row = self._db.execute("SELECT value FROM cache WHERE key = ?", (key,)).fetchone()
        return json.loads(row[0]) if row else None

    def _cache_put(self, key: str, value: dict[str, Any]) -> None:
        self._db.execute(
            "INSERT OR REPLACE INTO cache (key, value) VALUES (?, ?)", (key, json.dumps(value))
        )
        self._db.commit()

    # -- journalisation ----------------------------------------------------
    def _log(self, record: dict[str, Any]) -> None:
        line = json.dumps(record, ensure_ascii=False)
        if self._log_stream is not None:
            self._log_stream.write(line + "\n")
        else:
            with self._log_path.open("a") as fh:
                fh.write(line + "\n")

    # -- appel principal ----------------------------------------------------
    def complete(
        self,
        prompt: str,
        task_id: str = "_no_task",
        temperature: float | None = None,
        prompt_ref: str | None = None,
    ) -> OracleResponse:
        """Appelle le LLM (ou le cache). Budget vérifié AVANT tout appel réseau."""
        request = {
            "model": self.config.model,
            "max_tokens": self.config.max_tokens,
            "temperature": self.config.temperature if temperature is None else temperature,
            "prompt": prompt,
        }
        key = self._cache_key(request)

        cached = self._cache_get(key) if self.use_cache else None
        if cached is not None:
            result, is_cached, cost = cached, True, 0.0
        else:
            if self.cost_by_task[task_id] >= self.config.budget_usd_per_task:
                raise BudgetExceededError(
                    f"budget par tâche atteint pour {task_id!r} : "
                    f"{self.cost_by_task[task_id]:.4f} USD >= "
                    f"{self.config.budget_usd_per_task} USD — appel refusé"
                )
            result = self._call_with_retry(request)
            is_cached = False
            cost = self._cost(result["input_tokens"], result["output_tokens"])
            self.cost_by_task[task_id] += cost
            self.total_cost_usd += cost
            if self.use_cache:
                self._cache_put(key, result)

        self._log(
            {
                "model": request["model"],
                "task_id": task_id,
                "temperature": request["temperature"],
                "prompt_sha256": hashlib.sha256(prompt.encode()).hexdigest(),
                "prompt_ref": prompt_ref,
                "input_tokens": result["input_tokens"],
                "output_tokens": result["output_tokens"],
                "cost_usd": round(cost, 6),
                "cached": is_cached,
            }
        )
        return OracleResponse(
            text=result["text"],
            input_tokens=result["input_tokens"],
            output_tokens=result["output_tokens"],
            cost_usd=cost,
            cached=is_cached,
        )

    def _call_with_retry(self, request: dict[str, Any]) -> dict[str, Any]:
        delay = 1.0
        for attempt in range(MAX_RETRIES):
            try:
                self.network_calls += 1
                return self.transport(request)
            except TransientOracleError:
                if attempt == MAX_RETRIES - 1:
                    raise
                time.sleep(delay)
                delay *= 2
        raise AssertionError("unreachable")
