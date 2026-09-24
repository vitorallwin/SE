"""Case-agnostic validation, attempt tracking, and composition shared by every authoring configuration."""
from __future__ import annotations

import json
import traceback
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .neutral_template_builder import build_neutral_template_docx
from .proposal_rules import LATEST_RULES_VERSION, approved_template_version, validate_proposal_rules


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "assets" / "proposal_neutral_template.docx"
ENGINE_CONFIG = ROOT / "engine_config.json"


def engine_config() -> dict[str, Any]:
    return json.loads(ENGINE_CONFIG.read_text(encoding="utf-8"))


def validate_state(state: Any, source_text: str | None = None) -> list[str]:
    """Rule violations for an authored state; a malformed state is reported, never raised."""
    if not isinstance(state, dict):
        return ["estado malformado: o documento raiz não é um objeto JSON"]
    if int(state.get("rules_version", 0) or 0) < LATEST_RULES_VERSION:
        return [f"rules_version deve ser {LATEST_RULES_VERSION} para o gerador genérico"]
    try:
        return validate_proposal_rules(state, source_text)
    except Exception as exc:  # noqa: BLE001 - malformed fields must come back as feedback to the author
        return [f"estado malformado ({type(exc).__name__}): {exc}"]


def compose(state: dict[str, Any], out_dir: Path) -> dict[str, Any]:
    """Build the DOCX and the coverage report; composer blocks are returned, not raised."""
    out_dir.mkdir(parents=True, exist_ok=True)
    output = out_dir / f"{state.get('code', 'proposta')}.docx"
    try:
        build_neutral_template_docx(state, TEMPLATE, output)
    except Exception as exc:  # noqa: BLE001
        return {"status": "blocked_by_composer", "error": f"{type(exc).__name__}: {exc}", "trace": traceback.format_exc(limit=3)}
    (out_dir / "relatorio-cobertura.md").write_text(coverage_report(state), encoding="utf-8")
    return {"status": "emitted", "docx": str(output)}


def record_attempt(run_dir: Path, state_path: Path) -> dict[str, Any]:
    """Validate one authoring attempt, enforcing the configured iteration limit.

    Every attempt is copied to passN.json and logged in attempts.json. When an attempt is clean,
    the proposal is composed into run_dir/final.
    """
    run_dir.mkdir(parents=True, exist_ok=True)
    log_path = run_dir / "attempts.json"
    log = json.loads(log_path.read_text(encoding="utf-8")) if log_path.exists() else {"attempts": []}
    limit = int(engine_config()["max_iterations"])
    if len(log["attempts"]) >= limit:
        return {"status": "limit_reached", "limit": limit, "attempt": None}
    number = len(log["attempts"]) + 1
    raw = state_path.read_text(encoding="utf-8")
    (run_dir / f"pass{number}.json").write_text(raw, encoding="utf-8")
    try:
        state = json.loads(raw)
    except json.JSONDecodeError as exc:
        state, errors = None, [f"JSON inválido: {exc}"]
    else:
        source = run_dir / "insumo.md"
        errors = validate_state(state, source.read_text(encoding="utf-8") if source.exists() else None)
        if not source.exists():
            errors.append("insumo.md ausente na pasta da execução: aprovações não podem ser conferidas")
    entry = {"attempt": number, "at": datetime.now(timezone.utc).isoformat(), "errors_count": len(errors), "errors": errors}
    if not errors and state is not None:
        entry["composition"] = compose(state, run_dir / "final")
    log["attempts"].append(entry)
    log_path.write_text(json.dumps(log, ensure_ascii=False, indent=2), encoding="utf-8")
    return {"status": "ok" if not errors else "violations", "limit": limit, **entry}


TEXT_SUFFIXES = {".txt", ".md", ".eml", ".json", ".csv", ".html"}


def read_source_material(folder: Path) -> str:
    """Extract every source file into one text, identically for every authoring configuration."""
    from docx import Document  # local import keeps the runner light when only validating

    parts: list[str] = []
    for path in sorted(p for p in folder.rglob("*") if p.is_file()):
        name = path.relative_to(folder).as_posix()
        suffix = path.suffix.casefold()
        if suffix in TEXT_SUFFIXES:
            text = path.read_text(encoding="utf-8", errors="replace")
        elif suffix == ".docx":
            document = Document(path)
            text = "\n".join(p.text for p in document.paragraphs)
            for table in document.tables:
                text += "\n" + "\n".join(" | ".join(cell.text for cell in row.cells) for row in table.rows)
        elif suffix == ".pdf":
            from pypdf import PdfReader
            text = "\n".join(page.extract_text() or "" for page in PdfReader(path).pages)
        else:
            text = f"[arquivo em formato não suportado pelo extrator: {name}]"
        parts.append(f"## Arquivo: {name}\n\n{text.strip()}\n")
    return "\n".join(parts)


def prepare_run(source_dir: Path, run_dir: Path, proposal_date: str, data_mode: str, configuration: str) -> None:
    """Materialize exactly what an author receives: extracted source, catalog, and the request."""
    from .catalog import PRODUCTS

    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / "insumo.md").write_text(read_source_material(source_dir), encoding="utf-8")
    (run_dir / "catalog.json").write_text(json.dumps(PRODUCTS, ensure_ascii=False, indent=2), encoding="utf-8")
    config = engine_config()
    request = {
        "proposal_date": proposal_date,
        "data_mode": data_mode,
        "template_version": approved_template_version(),
        "configuration": configuration,
        "author_model": config["configurations"][configuration]["author_model"],
        "engine_version": config["engine_version"],
        "rules_version": config["rules_version"],
        "skill_sha256": skill_hash(),
        "max_iterations": config["max_iterations"],
        "source_folder": source_dir.name,
    }
    (run_dir / "request.json").write_text(json.dumps(request, ensure_ascii=False, indent=2), encoding="utf-8")


def skill_hash() -> str:
    """SHA-256 over every skill file (path and content), recorded in the tag and in each execution."""
    import hashlib

    skill = ROOT / "skills" / "akamai-proposal-authoring"
    digest = hashlib.sha256()
    for path in sorted(p for p in skill.rglob("*") if p.is_file()):
        digest.update(path.relative_to(skill).as_posix().encode("utf-8"))
        digest.update(path.read_bytes().replace(b"\r\n", b"\n"))
    return digest.hexdigest()


ENGINE_FILES = [
    "engine_config.json",
    "authoring/AUTHOR_BRIEF.md",
    "assets/proposal_neutral_template.docx",
    "assets/institutional_whitelist.json",
    "assets/case_residue.json",
    "scripts/validate_attempt.py",
    "scripts/author_with_gemini.py",
    *(f"sales_engineer/{name}.py" for name in (
        "__init__", "ai", "case_runner", "catalog", "document_validation",
        "institutional_policy", "neutral_template_builder", "proposal_rules",
    )),
]


SEALED_VALIDATOR = '''"""Submete uma tentativa ao motor, que fica fora desta pasta.

Uso: python scripts/validate_attempt.py execucao execucao/estado.json
"""
import subprocess
import sys
from pathlib import Path

ENGINE = Path({engine!r})
args = [str(Path(arg).resolve()) for arg in sys.argv[1:]]
sys.exit(subprocess.call([sys.executable, str(ENGINE / "scripts" / "validate_attempt.py"), *args]))
'''


def make_workspace(workspace: Path, source_dir: Path, proposal_date: str, data_mode: str, configuration: str,
                   sealed: bool = False) -> Path:
    """Physical isolation: a folder with only what production gives the author (engine, skill, brief, one case).

    No tests, fixtures, previous proposals, other cases, or version history are copied. A sealed workspace
    also leaves the engine out: the author gets the brief, the skill and the case, and submits through a
    wrapper, so the rules are known only through the skill and the validator's messages.
    Returns the execution folder inside the workspace.
    """
    import shutil

    if workspace.exists():
        raise FileExistsError(f"Workspace já existe: {workspace}")
    if sealed:
        brief = workspace / "authoring" / "AUTHOR_BRIEF.md"
        brief.parent.mkdir(parents=True)
        shutil.copy2(ROOT / "authoring" / "AUTHOR_BRIEF.md", brief)
        shutil.copytree(ROOT / "skills", workspace / "skills")
        wrapper = workspace / "scripts" / "validate_attempt.py"
        wrapper.parent.mkdir(parents=True)
        wrapper.write_text(SEALED_VALIDATOR.format(engine=str(ROOT)), encoding="utf-8")
        run_dir = workspace / "execucao"
        prepare_run(source_dir, run_dir, proposal_date, data_mode, configuration)
        return run_dir
    for relative in ENGINE_FILES:
        target = workspace / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ROOT / relative, target)
    shutil.copytree(ROOT / "skills", workspace / "skills")
    env_file = ROOT / ".env"
    if env_file.exists() and configuration == "A":
        shutil.copy2(env_file, workspace / ".env")
    run_dir = workspace / "execucao"
    prepare_run(source_dir, run_dir, proposal_date, data_mode, configuration)
    return run_dir


def skill_bundle() -> str:
    """The brief plus every skill file, as given to an author that cannot read files itself."""
    skill = ROOT / "skills" / "akamai-proposal-authoring"
    files = [ROOT / engine_config()["author_brief"], skill / "SKILL.md", *sorted((skill / "references").glob("*"))]
    return "\n\n".join(f"### {path.relative_to(ROOT).as_posix()}\n\n{path.read_text(encoding='utf-8')}" for path in files if path.is_file())


def coverage_report(state: dict[str, Any]) -> str:
    lines = [
        f"# Relatório de cobertura — {state.get('client_name', 'cliente')} ({state.get('code', '')})",
        "",
        f"- Regras: v{state.get('rules_version')}",
        f"- Modo dos dados: {state.get('data_mode')}",
        f"- Engajamento: {state.get('governance', {}).get('engagement_type', {}).get('value')}",
        "",
        "## Decisões",
        "",
        "| Decisão | Valor | Aprovado por | Data | Modo |",
        "|---|---|---|---|---|",
    ]
    for key, decision in state.get("governance", {}).items():
        lines.append(f"| {key} | {decision.get('value')} | {decision.get('approved_by')} | {decision.get('approved_at')} | {decision.get('mode')} |")
    lines += ["", "## Cobertura do insumo", "", "| Referência | Trecho | Status | Destino |", "|---|---|---|---|"]
    for entry in state.get("source_coverage", []):
        lines.append(f"| {entry.get('ref')} | {entry.get('statement')} | {entry.get('status')} | {', '.join(entry.get('targets', [])) or entry.get('reason', '')} |")
    lines += ["", "## Requisitos", "", "| REQ | Requisito | Origem | Falantes |", "|---|---|---|---|"]
    for item in state.get("traceability", []):
        lines.append(f"| {item.get('requirement_id')} | {item.get('requirement')} | {item.get('source')} | {', '.join(item.get('speakers', []))} |")
    lines += ["", "## Números do cliente", ""]
    lines += [f"- {n.get('ref')}: {n.get('quote')} → {n.get('destination')}" for n in state.get("client_numbers", [])] or ["- nenhum"]
    lines += ["", "## Perguntas abertas", ""]
    lines += [f"- {q}" for q in dict.fromkeys(state.get("open_questions", []))] or ["- nenhuma"]
    return "\n".join(lines) + "\n"
