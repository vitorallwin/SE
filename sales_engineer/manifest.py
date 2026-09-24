from __future__ import annotations

from typing import Any

from .catalog import PRODUCTS, recommended_product_ids


def _section(proposal: dict[str, Any], title: str) -> list[str]:
    wanted = title.casefold().strip()
    for section in proposal.get("sections", []):
        if str(section.get("title", "")).casefold().strip() == wanted:
            return [str(item).strip() for item in section.get("paragraphs", []) if str(item).strip()]
    return []


def build_document_manifest(proposal: dict[str, Any]) -> dict[str, Any]:
    decisions = proposal.get("solution_decisions", [])
    recommended = recommended_product_ids(decisions)
    optional = [item for item in decisions if item.get("status") == "optional" and item.get("product_id") in PRODUCTS]
    discovery = proposal.get("discovery", {})
    architecture = proposal.get("architecture", {})

    blocks: list[dict[str, Any]] = [
        {
            "id": "executive_summary",
            "type": "narrative",
            "title": "Resumo executivo",
            "paragraphs": _section(proposal, "Resumo executivo"),
        },
        {
            "id": "discovery",
            "type": "discovery",
            "title": "Contexto e objetivos",
            "business_goals": discovery.get("business_goals", []),
            "pain_points": discovery.get("pain_points", []),
            "constraints": discovery.get("constraints", []),
        },
        {
            "id": "solution",
            "type": "solution",
            "title": "Solução recomendada",
            "summary": architecture.get("summary", ""),
            "flow": architecture.get("flow", []),
            "products": recommended,
            "decisions": [item for item in decisions if item.get("product_id") in recommended],
        },
    ]

    if optional:
        blocks.append({"id": "options", "type": "options", "title": "Opções condicionais", "decisions": optional})

    blocks.extend([
        {
            "id": "traceability",
            "type": "traceability",
            "title": "Rastreabilidade dos requisitos",
            "requirements": discovery.get("requirements", []),
            "rows": proposal.get("traceability", []),
        },
        {
            "id": "scope",
            "type": "scope",
            "title": "Escopo técnico",
            "included": proposal.get("scope", {}).get("included", []),
            "deliverables": proposal.get("scope", {}).get("deliverables", []),
            "excluded": proposal.get("scope", {}).get("excluded", []),
        },
        {
            "id": "delivery",
            "type": "delivery",
            "title": "Abordagem de entrega",
            "phases": proposal.get("delivery", {}).get("phases", architecture.get("implementation_waves", [])),
            "responsibilities": proposal.get("delivery", {}).get("responsibilities", []),
        },
        {
            "id": "assumptions_risks",
            "type": "risk",
            "title": "Premissas riscos e pendências",
            "assumptions": proposal.get("assumptions", []),
            "risks": proposal.get("risks", []),
            "open_questions": proposal.get("open_questions", []),
        },
        {
            "id": "acceptance",
            "type": "acceptance",
            "title": "Critérios de aceite",
            "criteria": proposal.get("acceptance_criteria", []),
        },
    ])

    support = _section(proposal, "Operação e suporte")
    if support:
        blocks.insert(-1, {"id": "support", "type": "narrative", "title": "Operação e suporte", "paragraphs": support})

    return {
        "schema_version": "3.0",
        "template_profile": "populos-neutral-technical-proposal-v1",
        "title": "Proposta técnica",
        "subtitle": proposal.get("opportunity", "Solução Akamai"),
        "client": proposal.get("client_name", ""),
        "proposal_code": proposal.get("code", ""),
        "version": "1.0",
        "status": "Para revisão",
        "blocks": [block for block in blocks if _has_content(block)],
        "assets": [],
    }


def _has_content(block: dict[str, Any]) -> bool:
    if block.get("id") in {"traceability", "scope", "delivery", "assumptions_risks", "acceptance"}:
        return True
    return any(value for key, value in block.items() if key not in {"id", "type", "title"})
