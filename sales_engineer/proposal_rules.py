from __future__ import annotations

import re
from datetime import date, timedelta
from typing import Any, Iterable

from .document_validation import normalize_document_text


RULES_VERSION = 5
ENGAGEMENT_TYPES = {"assessment", "design", "implementation", "phased"}
NUMBER_DESTINATIONS = {"meta", "contexto_de_dor", "dimensionamento", "descartado_com_motivo"}
COVERAGE_STATUSES = {"coberto", "pendente", "descartado"}
COVERAGE_TARGETS = {"sumário", "escopo", "exclusões", "premissas", "dimensionamento", "engajamento"}

_NUMBER_WORDS = {
    "um": 1, "uma": 1, "dois": 2, "duas": 2, "três": 3, "quatro": 4, "cinco": 5, "seis": 6,
    "sete": 7, "oito": 8, "nove": 9, "dez": 10, "onze": 11, "doze": 12, "treze": 13,
    "quatorze": 14, "catorze": 14, "quinze": 15, "dezesseis": 16,
}
_RANGE = re.compile(r"(?:entre\s+)?(\d+|[a-zçê]+)\s+(?:a|e)\s+(\d+|[a-zçê]+)\s+(?:semanas|sem\.)", re.IGNORECASE)


def _as_number(token: str) -> int | None:
    token = token.casefold()
    return int(token) if token.isdigit() else _NUMBER_WORDS.get(token)


def week_ranges(text: str) -> list[tuple[int, int]]:
    ranges = []
    for low, high in _RANGE.findall(text):
        low_n, high_n = _as_number(low), _as_number(high)
        if low_n is not None and high_n is not None:
            ranges.append((low_n, high_n))
    return ranges


def _client_visible_texts(proposal: dict[str, Any]) -> Iterable[str]:
    for section in proposal.get("sections", []):
        yield from section.get("paragraphs", [])
    yield from proposal.get("document_text", {}).values()
    yield from proposal.get("restrictions", [])
    yield from proposal.get("assumptions", [])


def validate_proposal_rules(proposal: dict[str, Any]) -> list[str]:
    """Return every violation of the v5 fidelity and integrity rules (empty list = compliant)."""
    errors: list[str] = []
    governance = proposal.get("governance", {})

    # Every internal decision must be resolved, with a source.
    for key, decision in governance.items():
        if decision.get("state") == "populos_internal_decision" and not decision.get("value"):
            errors.append(f"decisão interna aberta: {key}")
        elif not decision.get("source"):
            errors.append(f"decisão sem origem registrada: {key}")

    # F-01: engagement type is a fact or a registered decision, never inferred.
    engagement = governance.get("engagement_type", {})
    if engagement.get("value") not in ENGAGEMENT_TYPES:
        errors.append("engagement_type ausente ou inválido")
    client_scope = proposal.get("client_scope", {})
    if not client_scope.get("source"):
        errors.append("client_scope sem referência ao insumo")
    phases = proposal.get("delivery", {}).get("phases", [])
    if client_scope.get("excludes_implementation") and engagement.get("value") != "implementation":
        for phase in phases:
            if phase.get("kind") == "implementation":
                errors.append(f"fase contratada com implantação contra o escopo do cliente: {phase.get('name')}")

    # Q-01: declared ranges equal the sum of committed phases.
    low = sum(phase.get("weeks", [0, 0])[0] for phase in phases)
    high = sum(phase.get("weeks", [0, 0])[1] for phase in phases)
    for phase in phases:
        if not phase.get("weeks"):
            errors.append(f"fase sem faixa numérica de semanas: {phase.get('name')}")
    for text in _client_visible_texts(proposal):
        for found in week_ranges(str(text)):
            if found != (low, high):
                errors.append(f"faixa {found[0]}–{found[1]} semanas diverge da soma das fases ({low}–{high}): {str(text)[:90]}")

    # Q-02 / Q-03: waves are contractual units.
    recommended = [d["product_id"] for d in proposal.get("solution_decisions", []) if d.get("status") == "recommended"]
    optional = [d["product_id"] for d in proposal.get("solution_decisions", []) if d.get("status") == "optional"]
    waves = (proposal.get("optional_phase") or {}).get("waves", [])
    if waves:
        for product in recommended:
            count = sum(product in wave.get("components", []) for wave in waves)
            if count != 1:
                errors.append(f"produto recomendado em {count} ondas (esperado 1): {product}")
        for wave in waves:
            if wave.get("goes_to_production") and not wave.get("acceptance"):
                errors.append(f"onda em produção sem marco de aceite: {wave.get('name')}")
            for product in wave.get("components", []):
                if product in optional:
                    errors.append(f"produto opcional dentro de onda: {product}")

    # Q-04: optional products stay out of the primary solution columns.
    optional_names = {"alb": "ALB", "account_protector": "Account Protector"}
    for item in proposal.get("traceability", []):
        for product in optional:
            label = optional_names.get(product, product)
            if label.casefold() in str(item.get("solution", "")).casefold():
                errors.append(f"opcional na matriz de rastreabilidade: {item.get('requirement_id')} cita {label}")

    # Provenance per requirement.
    requirement_ids = {item.get("requirement_id") for item in proposal.get("traceability", [])}
    for item in proposal.get("traceability", []):
        if not item.get("source"):
            errors.append(f"requisito sem referência de origem: {item.get('requirement_id')}")

    # F-06: every client number has a destination; pain context shows up in the summary.
    summary = normalize_document_text(" ".join(
        paragraph for section in proposal.get("sections", []) for paragraph in section.get("paragraphs", [])
    ))
    for number in proposal.get("client_numbers", []):
        destination = number.get("destination")
        if destination not in NUMBER_DESTINATIONS:
            errors.append(f"número do cliente sem destino: {number.get('quote')}")
        if destination == "contexto_de_dor" and normalize_document_text(number.get("summary_marker", "")) not in summary:
            errors.append(f"número de dor ausente do sumário: {number.get('quote')}")
        if destination == "descartado_com_motivo" and not number.get("reason"):
            errors.append(f"número descartado sem motivo: {number.get('quote')}")

    # Reverse coverage: source statement -> proposal.
    for entry in proposal.get("source_coverage", []):
        status = entry.get("status")
        if status not in COVERAGE_STATUSES:
            errors.append(f"cobertura sem status válido: {entry.get('ref')} {entry.get('statement')}")
            continue
        if status == "coberto":
            targets = entry.get("targets", [])
            if not targets:
                errors.append(f"cobertura sem destino: {entry.get('ref')}")
            for target in targets:
                if target not in requirement_ids and target not in COVERAGE_TARGETS:
                    errors.append(f"destino de cobertura inexistente: {target} ({entry.get('ref')})")
        if status == "descartado" and not entry.get("reason"):
            errors.append(f"trecho do insumo descartado sem motivo: {entry.get('ref')}")

    # F-07: estimates need an owner.
    for estimate in proposal.get("estimates", []):
        if not estimate.get("owner"):
            errors.append(f"estimativa sem responsável: {estimate.get('item')}")
    for row in proposal.get("dimensioning", []):
        if len(row) > 3 and row[3] == "Estimativa":
            errors.append(f"dimensionamento estimado sem premissa de responsável: {row[0]}")

    # F-02: exported data carries a sensitive-data control when privacy is required.
    exports_data = any("siem" in str(item).casefold() for item in proposal.get("scope", {}).get("included", []))
    privacy_required = any("logs" in str(entry.get("statement", "")).casefold() for entry in proposal.get("source_coverage", []))
    if exports_data and privacy_required and not any(
        "mascaramento" in str(item).casefold() for item in proposal.get("scope", {}).get("included", [])
    ):
        errors.append("integração SIEM sem controle de dados sensíveis")

    if int(proposal.get("rules_version", 0) or 0) >= 6:
        errors.extend(_validate_rules_v6(proposal))
    if int(proposal.get("rules_version", 0) or 0) >= 7:
        errors.extend(_validate_rules_v7(proposal))
    return errors


LATEST_RULES_VERSION = 7
DATA_MODES = {"test", "production"}
TECHNICAL_ROLES = {"arquiteto", "engenharia", "delivery", "pré-vendas técnica"}
_IMPLICIT_APPROVAL = re.compile(r"ao seguir|impl[ií]cit|t[aá]cit|presumid|por padr[aã]o|dado de teste", re.IGNORECASE)


def _production_options(proposal: dict[str, Any]) -> list[dict[str, Any]]:
    options = [wave for wave in (proposal.get("optional_phase") or {}).get("waves", []) if wave.get("goes_to_production")]
    track = proposal.get("fast_track")
    if track and track.get("production_change"):
        options.append(track)
    return options


def _validate_rules_v7(proposal: dict[str, Any]) -> list[str]:
    """Engine-wide issues from the V6 audit: explicit approvals, technical estimate owners,
    acceptance for every production option, license lead time, and test mode as a flag."""
    errors: list[str] = []

    # Modo de teste é marcação de origem, nunca desliga checagem.
    if proposal.get("data_mode") not in DATA_MODES:
        errors.append("data_mode ausente ou inválido (use 'test' ou 'production')")

    # Aprovação explícita: aprovador, data ISO, registro da aprovação e modo; sem aprovação implícita.
    for key, decision in proposal.get("governance", {}).items():
        if decision.get("state") != "commitment":
            continue
        try:
            date.fromisoformat(str(decision.get("approved_at", "")))
        except ValueError:
            errors.append(f"decisão sem data de aprovação válida (AAAA-MM-DD): {key}")
        if not decision.get("approval_record"):
            errors.append(f"decisão sem registro da aprovação explícita: {key}")
        if decision.get("mode") not in DATA_MODES:
            errors.append(f"decisão sem modo de dado (test/production): {key}")
        for field in ("approved_by", "approval_record", "source"):
            if _IMPLICIT_APPROVAL.search(str(decision.get(field, ""))):
                errors.append(f"aprovação implícita ou marcação de teste no texto ({field}): {key}")
        if key.endswith("_estimate") and decision.get("approver_role") not in TECHNICAL_ROLES:
            errors.append(f"estimativa de esforço aprovada por papel não técnico: {key}")

    # Estimativa de esforço tem dono técnico.
    for estimate in proposal.get("estimates", []):
        if estimate.get("owner_role") not in TECHNICAL_ROLES:
            errors.append(f"estimativa sem dono técnico (owner_role): {estimate.get('item')}")

    # Toda opção que toca produção tem critério de aceite próprio.
    options = _production_options(proposal)
    option_ids = {option.get("id") for option in options}
    for option in options:
        if not option.get("id"):
            errors.append(f"opção que toca produção sem id: {option.get('name') or option.get('title')}")
        elif not any(c.get("option_id") == option["id"] for c in proposal.get("acceptance_criteria", [])):
            errors.append(f"opção que toca produção sem critério de aceite próprio: {option['id']}")
    for criterion in proposal.get("acceptance_criteria", []):
        if criterion.get("phase") != "committed" and criterion.get("option_id") not in option_ids:
            errors.append(f"critério de fase opcional sem opção existente: {criterion.get('option_id')}")

    # O prazo de licenciamento entra em qualquer cálculo de viabilidade.
    for item in proposal.get("event_feasibility", []):
        lead = (item.get("lead_times") or {}).get("licenciamento")
        if not lead or lead.get("weeks") is None or not lead.get("source"):
            errors.append(f"viabilidade sem prazo de licenciamento declarado (semanas e origem): {item.get('event')}")
    track = proposal.get("fast_track")
    if track and track.get("components"):
        lead = (track.get("lead_times") or {}).get("licenciamento")
        if not lead or lead.get("weeks") is None or not lead.get("source"):
            errors.append("trilha rápida sem prazo de licenciamento declarado")
        if not any("licen" in str(text).casefold() for text in track.get("items", [])):
            errors.append("trilha rápida não lista o licenciamento entre os pré-requisitos")
    return errors


SPEAKER_ROLES = {"client", "vendor", "input_document"}
FEASIBILITY = {"fits", "partially_fits", "does_not_fit"}


def _date(value: str) -> date:
    return date.fromisoformat(value)


def phase_window(reference: date, phases: list[dict[str, Any]]) -> tuple[date, date]:
    """Earliest and latest end of the committed phases when work starts on the reference date."""
    low = sum(phase.get("weeks", [0, 0])[0] for phase in phases)
    high = sum(phase.get("weeks", [0, 0])[1] for phase in phases)
    return reference + timedelta(weeks=low), reference + timedelta(weeks=high)


def _validate_rules_v6(proposal: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    governance = proposal.get("governance", {})
    engagement = governance.get("engagement_type", {}).get("value")

    # Decisions are approved, unedited after approval, and bound to the engagement they were made for.
    for key, decision in governance.items():
        if decision.get("state") != "commitment":
            continue
        if not decision.get("approved_by") or not decision.get("approved_at"):
            errors.append(f"decisão sem aprovador e data: {key}")
        if "confirmar" in str(decision.get("source", "")).casefold():
            errors.append(f"decisão com origem pendente de confirmação: {key}")
        if decision.get("value") != decision.get("approved_value"):
            errors.append(f"texto da decisão difere do valor aprovado: {key}")
        if key != "engagement_type" and decision.get("engagement_ref") != engagement:
            errors.append(f"decisão tomada para outro engajamento ({decision.get('engagement_ref')} ≠ {engagement}): {key}")
    sla = governance.get("sla", {})
    if engagement not in sla.get("applies_to", []):
        errors.append(f"bloco institucional de SLA não declarado aplicável ao engajamento {engagement}")

    # Provenance per speaker: vendor-only statements are hypotheses.
    for item in proposal.get("traceability", []):
        speakers = set(item.get("speakers", []))
        if not speakers or not speakers <= SPEAKER_ROLES:
            errors.append(f"requisito sem papel de quem falou: {item.get('requirement_id')}")
        elif speakers == {"vendor"} and not item.get("hypothesis"):
            errors.append(f"requisito apoiado só na fala do fabricante sem marcação de hipótese: {item.get('requirement_id')}")

    # Committed deliverables cannot require what the scope boundary forbids.
    forbidden = [normalize_document_text(term) for term in proposal.get("client_scope", {}).get("forbidden_in_committed", [])]
    committed = [c.get("criterion", "") for c in proposal.get("acceptance_criteria", []) if c.get("phase", "committed") == "committed"]
    committed += proposal.get("scope", {}).get("included", []) + proposal.get("scope", {}).get("deliverables", [])
    for text in committed:
        for term in forbidden:
            if term in normalize_document_text(text):
                errors.append(f"entrega contratada exige ação proibida pelo limite de escopo ('{term}'): {str(text)[:80]}")

    # Critical events with a known date: feasibility is computed now, not promised for later.
    summary = normalize_document_text(" ".join(
        paragraph for section in proposal.get("sections", []) for paragraph in section.get("paragraphs", [])
    ))
    feasibility = {item.get("event"): item for item in proposal.get("event_feasibility", [])}
    phases = proposal.get("delivery", {}).get("phases", [])
    for event in proposal.get("critical_events", []):
        if not event.get("date"):
            if not event.get("pending_question"):
                errors.append(f"evento sem data e sem pergunta pendente: {event.get('name')}")
            continue
        item = feasibility.get(event.get("name"))
        if not item:
            errors.append(f"evento com data conhecida sem viabilidade declarada: {event.get('name')}")
            continue
        earliest, latest = phase_window(_date(item["reference_date"]), phases)
        if (item.get("phase1_end_earliest"), item.get("phase1_end_latest")) != (earliest.isoformat(), latest.isoformat()):
            errors.append(f"janela da Fase 1 declarada diverge do cálculo ({earliest:%d/%m}–{latest:%d/%m}): {event.get('name')}")
        if item.get("classification") not in FEASIBILITY or not item.get("reason"):
            errors.append(f"viabilidade sem classificação válida ou motivo: {event.get('name')}")
        if earliest >= _date(event["date"]) and item.get("classification") != "does_not_fit":
            errors.append(f"Fase 1 termina depois do evento, mas a viabilidade não é 'não cabe': {event.get('name')}")
        for marker in (f"{earliest:%d/%m}", f"{latest:%d/%m}", item.get("summary_marker", "")):
            if normalize_document_text(marker) not in summary:
                errors.append(f"sumário não declara a viabilidade do evento ({marker}): {event.get('name')}")

    # An optional fast track that touches production says so, with its own controls.
    track = proposal.get("fast_track")
    if track:
        recommended = {d["product_id"] for d in proposal.get("solution_decisions", []) if d.get("status") == "recommended"}
        if not track.get("production_change"):
            errors.append("trilha rápida não declara a entrada na borda como mudança em produção")
        for control in ("janela", "reversão", "aprovação"):
            if control not in track.get("controls", []):
                errors.append(f"trilha rápida sem controle próprio: {control}")
        if track.get("deadline_reference") != "freeze":
            errors.append("trilha rápida deve caber antes do congelamento, não apenas antes do evento")
        if not track.get("first_question"):
            errors.append("trilha rápida sem a pergunta inicial sobre hostnames já na Akamai")
        for product in track.get("components", []):
            if product not in recommended:
                errors.append(f"trilha rápida com produto não recomendado: {product}")
        if "prolexic" in track.get("components", []):
            errors.append("trilha rápida não pode prometer Prolexic antes da validação de rede")
    return errors


def assert_proposal_rules(proposal: dict[str, Any]) -> None:
    errors = validate_proposal_rules(proposal)
    if errors:
        raise ValueError("Regras v5 violadas: " + "; ".join(errors))
