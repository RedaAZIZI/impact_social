"""X-53 — critères d'acceptation du client oracle. Tout est mocké : zéro réseau."""

from __future__ import annotations

import io
import json
from pathlib import Path
from typing import Any

import pytest

from solveur.oracle.client import (
    BudgetExceededError,
    OracleClient,
    OracleConfig,
    TransientOracleError,
)

PRICING = {
    "model-a": {"input_usd_per_mtok": 1.0, "output_usd_per_mtok": 5.0},
    "model-b": {"input_usd_per_mtok": 3.0, "output_usd_per_mtok": 15.0},
}


class MockTransport:
    def __init__(self, text: str = "réponse", fail_first: int = 0) -> None:
        self.calls: list[dict[str, Any]] = []
        self.text = text
        self.fail_first = fail_first

    def __call__(self, request: dict[str, Any]) -> dict[str, Any]:
        self.calls.append(request)
        if len(self.calls) <= self.fail_first:
            raise TransientOracleError("429")
        return {"text": self.text, "input_tokens": 1000, "output_tokens": 2000}


def make_client(tmp_path: Path, transport: MockTransport, **cfg: Any) -> OracleClient:
    config = OracleConfig(model=cfg.pop("model", "model-a"), **cfg)
    return OracleClient(
        config,
        transport=transport,
        cache_path=tmp_path / "cache.db",
        log_stream=io.StringIO(),
        pricing=PRICING,
    )


def test_cache_hit(tmp_path: Path) -> None:
    transport = MockTransport()
    client = make_client(tmp_path, transport)
    r1 = client.complete("même prompt", task_id="t1")
    r2 = client.complete("même prompt", task_id="t1")
    assert len(transport.calls) == 1  # un seul appel réseau
    assert not r1.cached and r2.cached
    assert r2.cost_usd == 0.0
    assert client.total_cost_usd == pytest.approx(r1.cost_usd)  # coût compté une fois


def test_budget_ceiling(tmp_path: Path) -> None:
    transport = MockTransport()
    # 1er appel coûte 1000*1 + 2000*5 = 11000 µUSD = 0.011 USD >= budget 0.01
    client = make_client(tmp_path, transport, budget_usd_per_task=0.01)
    client.complete("prompt 1", task_id="t1")
    with pytest.raises(BudgetExceededError):
        client.complete("prompt 2", task_id="t1")
    assert len(transport.calls) == 1  # pas d'appel réseau pour le 2e


def test_cost_accounting(tmp_path: Path) -> None:
    client = make_client(tmp_path, MockTransport())
    r = client.complete("p", task_id="t1")
    # pricing model-a : 1000 tokens in à 1 $/M + 2000 out à 5 $/M
    assert r.cost_usd == pytest.approx((1000 * 1.0 + 2000 * 5.0) / 1_000_000)
    assert client.cost_by_task["t1"] == pytest.approx(r.cost_usd)


def test_model_swap(tmp_path: Path) -> None:
    # Changer le modèle = changer la config. Le code appelant est identique.
    def run(model: str) -> float:
        transport = MockTransport()
        (tmp_path / model).mkdir(exist_ok=True)
        client = make_client(tmp_path / model, transport, model=model)
        r = client.complete("prompt identique", task_id="t")
        assert transport.calls[0]["model"] == model
        return r.cost_usd

    cost_a, cost_b = run("model-a"), run("model-b")
    assert cost_b == pytest.approx(3 * cost_a)  # même code, prix du modèle B


def test_retry_backoff(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("solveur.oracle.client.time.sleep", lambda _s: None)
    transport = MockTransport(fail_first=3)
    client = make_client(tmp_path, transport)
    r = client.complete("p", task_id="t")
    assert r.text == "réponse"
    assert len(transport.calls) == 4  # 3 échecs 429 puis succès


def test_no_cache_flag(tmp_path: Path) -> None:
    transport = MockTransport()
    config = OracleConfig(model="model-a")
    client = OracleClient(
        config,
        transport=transport,
        cache_path=tmp_path / "cache.db",
        log_stream=io.StringIO(),
        pricing=PRICING,
        use_cache=False,
    )
    client.complete("p", task_id="t")
    client.complete("p", task_id="t")
    assert len(transport.calls) == 2  # mesure propre : pas de cache


def test_call_logging(tmp_path: Path) -> None:
    stream = io.StringIO()
    config = OracleConfig(model="model-a")
    client = OracleClient(
        config,
        transport=MockTransport(),
        cache_path=tmp_path / "cache.db",
        log_stream=stream,
        pricing=PRICING,
    )
    client.complete("p", task_id="t42")
    record = json.loads(stream.getvalue().splitlines()[0])
    assert record["task_id"] == "t42"
    assert record["model"] == "model-a"
    assert not record["cached"]
