# SOLVEUR — règles pour les agents

Projet : solveur ARC-AGI explicable (LLM proposeur + vérifieur bayésien/MDL).
Ce dossier `solveur/` est autonome dans le monorepo `impact_social` : tout se
lance depuis `solveur/` (`make install`, `make test`, `make eval`, `make report`).
Ne pas toucher au reste du repo (projet REX) ni au `CLAUDE.md` racine.

## Les 5 règles

1. **Conventions du repo.** Package `solveur/`, tests dans `tests/`, prompts
   versionnés dans `prompts/`, rapports dans `reports/`. Python 3.11+, deps
   gérées par `uv` (lockfile `uv.lock` committé). `make lint && make test`
   vert avant tout push. Une PR par ticket, jamais de merge par un agent.

2. **Un ticket = une nuit.** Chaque ticket Linear (X-nn) se traite en une
   session : lire le ticket, implémenter les tests nommés dans les critères
   d'acceptation, puis le code, ouvrir la PR, passer le ticket en "In Review"
   avec un commentaire de synthèse. Si le ticket ne tient pas dans la nuit,
   le découper en sous-tickets plutôt que de livrer partiel.

3. **Interdiction ABSOLUE de lire le split final.** Aucun chargement, log,
   affichage ou statistique sur le split `final` sans `FINAL_RUN=1` posé par
   un humain. Le verrou `FinalSetLockedError` ne se contourne jamais, y
   compris dans les tests. Une fuite du set final invalide le résultat public.

4. **Rapport après tout run.** Tout run d'évaluation écrit dans `runs.db` et
   doit être suivi d'un rapport (`python -m solveur.report --run <run_id>`)
   committé dans `reports/`. Un run sans rapport n'existe pas.

5. **Format des commits.** `X-nn: description courte` (référence au ticket
   Linear). Aucun secret en clair (clés API via variables d'environnement
   uniquement). Pas d'appel API réel pour tester la plomberie : mocks.
