"""Configuration A: the author is a single Gemini call per attempt, under the same brief, skill,
validator and iteration limit as configuration B.

Usage: python scripts/author_with_gemini.py RUN_DIR   (run scripts/prepare_run.py first)
Requires GEMINI_API_KEY in the environment; GEMINI_MODEL overrides the model.
"""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from sales_engineer.ai import GeminiClient
from sales_engineer.case_runner import engine_config, record_attempt, skill_bundle


INSTRUCTION = (
    "Siga o brief e a skill abaixo. Responda somente com o objeto JSON do estado da proposta. "
    "Inclua o campo \"_notes\" com no máximo 15 linhas sobre pendências e bloqueios."
)


def _load_dotenv() -> None:
    """Read GEMINI_* from the git-ignored .env so the key never passes through the command line."""
    import os

    env_file = ROOT / ".env"
    if not env_file.exists():
        return
    for line in env_file.read_text(encoding="utf-8").splitlines():
        key, _, value = line.partition("=")
        if key.strip() in {"GEMINI_API_KEY", "GEMINI_MODEL"} and value.strip() and not os.getenv(key.strip()):
            os.environ[key.strip()] = value.strip()


def main() -> int:
    _load_dotenv()
    run_dir = Path(sys.argv[1])
    request = json.loads((run_dir / "request.json").read_text(encoding="utf-8"))
    client = GeminiClient()
    system = INSTRUCTION + "\n\n" + skill_bundle()
    payload = {
        "pedido": {"data_da_proposta": request["proposal_date"], "data_mode": request["data_mode"]},
        "catalogo": json.loads((run_dir / "catalog.json").read_text(encoding="utf-8")),
        "insumo": (run_dir / "insumo.md").read_text(encoding="utf-8"),
    }
    log = {"model": client.model, "started_at": datetime.now(timezone.utc).isoformat(), "attempts": []}
    for _ in range(int(engine_config()["max_iterations"])):
        try:
            state = client.generate_json(system, payload, max_output_tokens=65536)
        except RuntimeError as exc:
            log["attempts"].append({"error": str(exc)})
            break
        notes = state.pop("_notes", "")
        (run_dir / "notes.md").write_text(notes if isinstance(notes, str) else json.dumps(notes, ensure_ascii=False), encoding="utf-8")
        candidate = run_dir / "candidate.json"
        candidate.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")
        result = record_attempt(run_dir, candidate)
        log["attempts"].append({key: result.get(key) for key in ("attempt", "status", "errors_count")})
        if result["status"] != "violations":
            break
        payload["estado_anterior"] = state
        payload["violacoes_do_validador"] = result["errors"]
    log["finished_at"] = datetime.now(timezone.utc).isoformat()
    (run_dir / "gemini_run.json").write_text(json.dumps(log, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(log, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
