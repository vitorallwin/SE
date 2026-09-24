"""Test bench (bancada): the same run flow as the sealed rounds, driven from a browser.

A run is a folder in lab_runs/ with the source files, the extracted insumo, the request and every attempt,
all written by case_runner. The bench adds nothing to the rules: it creates runs, submits states (pasted by
an operator or produced by an API author) and reads back what the engine recorded.
"""
from __future__ import annotations

import base64
import json
import re
import shutil
import threading
import unicodedata
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .ai import ClaudeClient, GeminiClient, load_dotenv
from .case_runner import ROOT, author_loop, engine_config, prepare_run, record_attempt
from .feasibility import compute, paragraph
from .violation_codes import code_of

RUNS = ROOT / "lab_runs"
SOURCE_SUFFIXES = {".txt", ".md", ".eml", ".json", ".csv", ".html", ".docx", ".pdf"}
LEGITIMATE_BLOCKS = {"GATE-INSUMO", "GATE-CATALOGO", "DECISAO-ABERTA"}
MAX_UPLOAD = 15 * 1024 * 1024

_jobs: dict[str, dict[str, Any]] = {}
_lock = threading.Lock()


class LabError(Exception):
    def __init__(self, message: str, status: int = 400):
        super().__init__(message)
        self.status = status


def _slug(text: str) -> str:
    plain = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode().casefold()
    return re.sub(r"[^a-z0-9]+", "-", plain).strip("-")[:40] or "caso"


def _run_dir(run_id: str) -> Path:
    if not re.fullmatch(r"[a-z0-9-]{1,80}", run_id or ""):
        raise LabError("execução inválida", 404)
    path = RUNS / run_id
    if not (path / "request.json").exists():
        raise LabError("execução não encontrada", 404)
    return path


def _read_json(path: Path, default: Any) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return default


def authors() -> dict[str, Any]:
    load_dotenv(ROOT)
    config = engine_config()
    return {
        "gemini": GeminiClient().status(),
        "claude": ClaudeClient(config["configurations"]["B"]["author_model"]).status(),
    }


def status() -> dict[str, Any]:
    config = engine_config()
    return {
        "engine_version": config["engine_version"],
        "rules_version": config["rules_version"],
        "template_version": config["template_version"],
        "max_iterations": config["max_iterations"],
        "authors": authors(),
        "pdf": shutil.which("soffice") is not None,
    }


def create_run(payload: dict[str, Any]) -> dict[str, Any]:
    name = str(payload.get("name") or "").strip()
    proposal_date = str(payload.get("proposal_date") or "").strip()
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", proposal_date):
        raise LabError("data da proposta inválida (AAAA-MM-DD)")
    data_mode = payload.get("data_mode") or "real"
    if data_mode not in {"real", "demo"}:
        raise LabError("modo dos dados inválido")
    files = payload.get("files") or []
    text = str(payload.get("text") or "").strip()
    if not files and not text and not payload.get("inherited"):
        raise LabError("envie arquivos do insumo ou cole o texto")
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    run_id = f"{stamp}-{_slug(name or 'caso')}"
    suffix = 1
    while (RUNS / run_id).exists():
        suffix += 1
        run_id = f"{stamp}-{_slug(name or 'caso')}-{suffix}"
    run_dir = RUNS / run_id
    source = run_dir / "fonte"
    source.mkdir(parents=True)
    total = 0
    try:
        for item in files:
            filename = Path(str(item.get("name") or "")).name
            if Path(filename).suffix.casefold() not in SOURCE_SUFFIXES:
                raise LabError(f"formato não suportado: {filename}")
            content = base64.b64decode(str(item.get("content") or ""), validate=True)
            total += len(content)
            if total > MAX_UPLOAD:
                raise LabError("insumo acima de 15 MB")
            (source / filename).write_bytes(content)
        if text:
            (source / "texto-colado.md").write_text(text, encoding="utf-8")
        for extra in payload.get("inherited") or []:
            (source / extra["name"]).write_bytes(extra["bytes"])
        prepare_run(source, run_dir, proposal_date, data_mode, "B")
    except LabError:
        shutil.rmtree(run_dir, ignore_errors=True)
        raise
    except Exception as exc:  # noqa: BLE001 - extraction errors go back to the operator
        shutil.rmtree(run_dir, ignore_errors=True)
        raise LabError(f"falha ao extrair o insumo: {type(exc).__name__}: {exc}") from exc
    meta = {"name": name or run_id, "created_at": datetime.now(timezone.utc).isoformat(), "parent": payload.get("parent")}
    (run_dir / "bancada.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
    return detail(run_id)


def complement_run(run_id: str, text: str) -> dict[str, Any]:
    """A new run with the same sources plus an operator note (e.g. an approval e-mail); the old run is kept."""
    parent = _run_dir(run_id)
    text = text.strip()
    if not text:
        raise LabError("complemento vazio")
    request = _read_json(parent / "request.json", {})
    meta = _read_json(parent / "bancada.json", {})
    inherited = [{"name": p.name, "bytes": p.read_bytes()} for p in sorted((parent / "fonte").glob("*")) if p.is_file()]
    number = 1 + sum(1 for p in inherited if p["name"].startswith("complemento-"))
    inherited.append({"name": f"complemento-{number}.md", "bytes": text.encode("utf-8")})
    return create_run({"name": f"{meta.get('name', run_id)} + complemento {number}", "proposal_date": request.get("proposal_date"),
                       "data_mode": request.get("data_mode"), "inherited": inherited, "parent": run_id})


def submit_state(run_id: str, text: str) -> dict[str, Any]:
    run_dir = _run_dir(run_id)
    if _busy(run_id):
        raise LabError("um autor está rodando nesta execução", 409)
    candidate = run_dir / "candidate.json"
    candidate.write_text(text, encoding="utf-8")
    _set_author(run_dir, "manual", "operador")
    result = record_attempt(run_dir, candidate)
    if result["status"] == "limit_reached":
        raise LabError(f"limite de {result['limit']} tentativas atingido", 409)
    return detail(run_id)


def _set_author(run_dir: Path, engine: str, model: str) -> None:
    request = _read_json(run_dir / "request.json", {})
    request["configuration"] = {"gemini": "A", "claude": "B-api", "manual": "manual"}[engine]
    request["author_model"] = model
    (run_dir / "request.json").write_text(json.dumps(request, ensure_ascii=False, indent=2), encoding="utf-8")


def _busy(run_id: str) -> bool:
    with _lock:
        return _jobs.get(run_id, {}).get("state") == "running"


def start_author(run_id: str, engine: str) -> dict[str, Any]:
    run_dir = _run_dir(run_id)
    load_dotenv(ROOT)
    if engine == "gemini":
        client: Any = GeminiClient()
    elif engine == "claude":
        client = ClaudeClient(engine_config()["configurations"]["B"]["author_model"])
    else:
        raise LabError("autor inválido")
    if not client.configured:
        raise LabError(f"chave do autor {engine} ausente no .env do servidor", 412)
    attempts = _read_json(run_dir / "attempts.json", {"attempts": []})["attempts"]
    if len(attempts) >= int(engine_config()["max_iterations"]):
        raise LabError("limite de tentativas atingido", 409)
    with _lock:
        if _jobs.get(run_id, {}).get("state") == "running":
            raise LabError("um autor já está rodando nesta execução", 409)
        _jobs[run_id] = {"state": "running", "engine": engine, "model": client.model, "started_at": datetime.now(timezone.utc).isoformat()}
    _set_author(run_dir, engine, client.model)

    def work() -> None:
        try:
            log = author_loop(run_dir, client)
            errors = [a["error"] for a in log["attempts"] if "error" in a]
            outcome = {"state": "failed", "error": errors[-1]} if errors else {"state": "done"}
        except Exception as exc:  # noqa: BLE001
            outcome = {"state": "failed", "error": f"{type(exc).__name__}: {exc}"}
        with _lock:
            _jobs[run_id].update(outcome, finished_at=datetime.now(timezone.utc).isoformat())

    threading.Thread(target=work, daemon=True).start()
    return detail(run_id)


def render_pdf(run_id: str) -> dict[str, Any]:
    run_dir = _run_dir(run_id)
    docx = next((run_dir / "final").glob("*.docx"), None)
    if docx is None:
        raise LabError("não há proposta emitida", 409)
    from scripts.render_pdf import render

    try:
        render(docx, run_dir / "final" / "render")
    except Exception as exc:  # noqa: BLE001
        raise LabError(f"falha ao gerar PDF: {type(exc).__name__}: {exc}", 500) from exc
    return detail(run_id)


def verdict(attempts: list[dict[str, Any]], limit: int, running: bool) -> dict[str, str]:
    if running:
        return {"key": "running", "label": "Autor escrevendo"}
    if not attempts:
        return {"key": "waiting", "label": "Aguardando estado"}
    last = attempts[-1]
    composition = last.get("composition") or {}
    if composition.get("status") == "emitted":
        return {"key": "emitted", "label": "Proposta emitida"}
    if composition.get("status") == "blocked_by_composer":
        return {"key": "failed", "label": "Compositor bloqueou"}
    codes = set(last.get("codes") or [])
    if codes and codes <= LEGITIMATE_BLOCKS:
        return {"key": "blocked", "label": "Bloqueio legítimo"}
    if len(attempts) >= limit:
        return {"key": "failed", "label": "Limite esgotado"}
    return {"key": "violations", "label": "Violações do autor"}


def _last_state(run_dir: Path, attempts: list[dict[str, Any]]) -> dict[str, Any] | None:
    if not attempts:
        return None
    state = _read_json(run_dir / f"pass{attempts[-1]['attempt']}.json", None)
    return state if isinstance(state, dict) else None


def _pending(state: dict[str, Any] | None) -> dict[str, Any]:
    if not state:
        return {"readable": False, "questions": [], "decisions": [], "feasibility": []}
    decisions = [
        {"key": key, "value": item.get("value"), "state": item.get("state")}
        for key, item in (state.get("governance") or {}).items()
        if isinstance(item, dict) and item.get("state") not in {"commitment", None}
    ]
    try:
        feasibility = [{"event": r.event, "classification": r.classification, "text": paragraph(r), "errors": r.errors}
                       for r in compute(state)]
    except Exception:  # noqa: BLE001 - a malformed state already shows up as a violation
        feasibility = []
    return {"readable": True, "questions": list(dict.fromkeys(str(q) for q in state.get("open_questions", []) if str(q).strip())),
            "decisions": decisions, "feasibility": feasibility, "client": state.get("client_name"), "code": state.get("code")}


def _files(run_dir: Path) -> list[dict[str, Any]]:
    wanted = [*sorted(run_dir.glob("pass*.json")), *sorted((run_dir / "final").glob("*.docx")),
              *sorted((run_dir / "final").glob("*.md")), *sorted((run_dir / "final" / "render").glob("*.pdf")),
              run_dir / "insumo.md", run_dir / "attempts.json", run_dir / "notes.md"]
    return [{"path": p.relative_to(run_dir).as_posix(), "size": p.stat().st_size} for p in wanted if p.exists()]


def summary(run_dir: Path) -> dict[str, Any]:
    limit = int(engine_config()["max_iterations"])
    attempts = _read_json(run_dir / "attempts.json", {"attempts": []})["attempts"]
    meta = _read_json(run_dir / "bancada.json", {})
    request = _read_json(run_dir / "request.json", {})
    return {"id": run_dir.name, "name": meta.get("name", run_dir.name), "created_at": meta.get("created_at"),
            "attempts": len(attempts), "limit": limit, "author": request.get("configuration"),
            "verdict": verdict(attempts, limit, _busy(run_dir.name))}


def list_runs() -> list[dict[str, Any]]:
    if not RUNS.exists():
        return []
    return [summary(p) for p in sorted(RUNS.iterdir(), reverse=True) if (p / "request.json").exists()]


def detail(run_id: str) -> dict[str, Any]:
    run_dir = _run_dir(run_id)
    attempts = _read_json(run_dir / "attempts.json", {"attempts": []})["attempts"]
    insumo = (run_dir / "insumo.md").read_text(encoding="utf-8")
    pages = sorted((run_dir / "final" / "render").glob("*.png"))
    with _lock:
        job = dict(_jobs.get(run_id, {}))
    return {
        **summary(run_dir),
        "request": _read_json(run_dir / "request.json", {}),
        "parent": _read_json(run_dir / "bancada.json", {}).get("parent"),
        "insumo": insumo,
        "sources": [p.name for p in sorted((run_dir / "fonte").glob("*")) if p.is_file()],
        "attempt_log": [{**a, "items": [{"code": code_of(e), "message": e} for e in a.get("errors", [])]} for a in attempts],
        "notes": (run_dir / "notes.md").read_text(encoding="utf-8") if (run_dir / "notes.md").exists() else "",
        "pending": _pending(_last_state(run_dir, attempts)),
        "files": _files(run_dir),
        "pages": [p.relative_to(run_dir).as_posix() for p in pages],
        "job": job,
    }


def file_path(run_id: str, relative: str) -> Path:
    run_dir = _run_dir(run_id).resolve()
    target = (run_dir / relative).resolve()
    if run_dir not in target.parents or not target.is_file():
        raise LabError("arquivo não encontrado", 404)
    return target
