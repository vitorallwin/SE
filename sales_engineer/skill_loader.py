from __future__ import annotations

from pathlib import Path


def load_authoring_skill(root: Path) -> str:
    skill = root / "skills" / "akamai-proposal-authoring"
    paths = [
        skill / "SKILL.md",
        skill / "references" / "global-rules.md",
        skill / "references" / "agent-contracts.md",
        skill / "references" / "section-model.md",
        skill / "references" / "solution-gating.md",
    ]
    chunks = []
    for path in paths:
        if path.exists():
            chunks.append(f"\n--- {path.name} ---\n{path.read_text(encoding='utf-8')}")
    if not chunks:
        raise RuntimeError("Skill de autoria Akamai não encontrado")
    return "".join(chunks)
