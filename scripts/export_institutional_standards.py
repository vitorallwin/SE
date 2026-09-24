"""Export the institutional standards of the approved template to the skill (A1, auditoria v10).

The author compares client demands with these values; without them it cannot declare a demand compatible.
Usage: python scripts/export_institutional_standards.py   (rerun whenever the template version changes)
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

from docx import Document

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

TEMPLATE = ROOT / "assets" / "proposal_neutral_template.docx"
TARGET = ROOT / "skills" / "akamai-proposal-authoring" / "references" / "institutional-standards.json"


def institutional_standards() -> dict:
    whitelist = json.loads((ROOT / "assets" / "institutional_whitelist.json").read_text(encoding="utf-8"))
    table = Document(TEMPLATE).tables[10]
    rows = [[cell.text.strip() for cell in row.cells] for row in table.rows[1:]]
    return {
        "template_version": whitelist["template_version"],
        "sla": {
            "scope": "Atuação da equipe POPULOS sobre falhas ou defeitos decorrentes exclusivamente dos serviços executados, durante a execução e a garantia técnica. Não é sustentação nem suporte gerenciado.",
            "support_window": "Não definida na tabela institucional (a tabela não fixa horário de atendimento).",
            "severities": [
                {"severity": severity, "response": response, "resolution": resolution, "description": description}
                for severity, response, resolution, description in rows
            ],
        },
        "decisions_without_standard": [
            "warranty", "license_supply", "engagement_type", "stabilization_buffer", "sla_applicability (fora de implementation)",
        ],
    }


if __name__ == "__main__":
    TARGET.write_text(json.dumps(institutional_standards(), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(TARGET)
