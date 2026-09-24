from __future__ import annotations

import json
import re
import unicodedata
from datetime import date, timedelta
from pathlib import Path
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


def validate_proposal_rules(proposal: dict[str, Any], source_text: str | None = None) -> list[str]:
    """Return every violation of the v5 fidelity and integrity rules (empty list = compliant).

    `source_text` is the extracted source material; from rules v9 on, case approvals are checked against it.
    """
    gate = _pre_proposal_gate(proposal)
    if gate is not None:
        return gate
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
    if int(proposal.get("rules_version", 0) or 0) >= 8:
        errors.extend(_validate_rules_v8(proposal))
    if int(proposal.get("rules_version", 0) or 0) >= 9 and source_text is not None:
        errors.extend(_validate_approval_quotes(proposal, source_text))
    return errors


LATEST_RULES_VERSION = 9
DATA_MODES = {"test", "production"}
# Prefixos normalizados (sem acento, minúsculos): aceitam "Arquiteto", "arquiteta", "Engenheira de redes"...
_TECHNICAL_ROLE_PREFIXES = ("arquitet", "engenh", "delivery", "pre-vendas tecnic", "pre vendas tecnic", "presales tecnic")
_IMPLICIT_APPROVAL = re.compile(r"ao seguir|impl[ií]cit|t[aá]cit|presumid|por padr[aã]o|dado de teste", re.IGNORECASE)
_WHITELIST = Path(__file__).resolve().parents[1] / "assets" / "institutional_whitelist.json"


def _is_technical_role(role: Any) -> bool:
    normalized = unicodedata.normalize("NFKD", str(role or "")).encode("ascii", "ignore").decode().casefold().strip()
    return normalized.startswith(_TECHNICAL_ROLE_PREFIXES)


def is_populos_standard(decision: dict[str, Any]) -> bool:
    """An institutional standard is versioned with the template, not approved per case."""
    return decision.get("basis") == "populos_standard"


def approved_template_version() -> str:
    return str(json.loads(_WHITELIST.read_text(encoding="utf-8")).get("template_version", ""))


def _license_lead_unknown(lead_times: Any) -> bool:
    lead = (lead_times or {}).get("licenciamento") or {}
    return lead.get("weeks") is None


def _license_lead_problem(lead_times: Any) -> str | None:
    lead = (lead_times or {}).get("licenciamento")
    if not lead:
        return "sem prazo de licenciamento declarado"
    if lead.get("weeks") is None:
        return None if lead.get("pending_question") else "com prazo de licenciamento desconhecido sem pergunta aberta"
    return None if lead.get("source") else "com prazo de licenciamento sem origem"


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
    template_version = approved_template_version()
    for key, decision in proposal.get("governance", {}).items():
        if decision.get("state") != "commitment":
            continue
        if is_populos_standard(decision):
            if decision.get("template_version") != template_version:
                errors.append(f"padrão institucional sem a versão vigente do template ({template_version}): {key}")
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
        if key.endswith("_estimate") and not _is_technical_role(decision.get("approver_role")):
            errors.append(f"estimativa de esforço aprovada por papel não técnico: {key}")

    # Estimativa de esforço tem dono técnico.
    for estimate in proposal.get("estimates", []):
        if not _is_technical_role(estimate.get("owner_role")):
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

    # O prazo de licenciamento entra em qualquer cálculo de viabilidade: conhecido (semanas e origem)
    # ou desconhecido (weeks null e pergunta aberta). Com prazo desconhecido, nada pode ser classificado como 'fits'.
    for item in proposal.get("event_feasibility", []):
        problem = _license_lead_problem(item.get("lead_times"))
        if problem:
            errors.append(f"viabilidade {problem}: {item.get('event')}")
        elif _license_lead_unknown(item.get("lead_times")) and item.get("classification") == "fits":
            errors.append(f"viabilidade 'fits' com prazo de licenciamento desconhecido: {item.get('event')}")
    track = proposal.get("fast_track")
    if track and track.get("components"):
        problem = _license_lead_problem(track.get("lead_times"))
        if problem:
            errors.append(f"trilha rápida {problem}")
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
        if int(proposal.get("rules_version", 0) or 0) >= 7 and is_populos_standard(decision):
            continue  # padrão institucional: versionado com o template (checado na v7), sem aprovação por caso
        if not decision.get("approved_by") or not decision.get("approved_at"):
            errors.append(f"decisão sem aprovador e data: {key}")
        if "confirmar" in str(decision.get("source", "")).casefold():
            errors.append(f"decisão com origem pendente de confirmação: {key}")
        if decision.get("value") != decision.get("approved_value"):
            errors.append(f"texto da decisão difere do valor aprovado: {key}")
        if key != "engagement_type" and decision.get("engagement_ref") != engagement:
            errors.append(f"decisão tomada para outro engajamento ({decision.get('engagement_ref')} ≠ {engagement}): {key}")
    sla = governance.get("sla", {})
    if int(proposal.get("rules_version", 0) or 0) < 8 and engagement not in sla.get("applies_to", []):
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


PRODUCT_STATUSES = {"recommended", "optional", "needs_information", "excluded", "already_contracted"}
INPUT_STATUSES = {"sufficient", "insufficient"}
CATALOG_FIT = {"fits", "no_catalog"}
MAX_QUALIFICATION_QUESTIONS = 8

# Slots do template cujo texto depende do caso. Na v8 o compositor não tem texto padrão para eles:
# ou o estado traz o texto, ou a emissão bloqueia (o texto padrão antigo carregava um caso anterior).
REQUIRED_DOCUMENT_TEXT = (
    "about_solution", "coverage", "dimensioning_intro", "methodology_intro", "tests",
    "schedule_intro", "schedule_sequence", "closing", "callout_migration", "callout_milestones",
    "diagram_users", "diagram_users_detail", "diagram_origins_title", "diagram_origins",
)
REQUIRED_LISTS = {"assessment_items": (3, 3), "restrictions": (4, 4), "client_roles": (1, 4), "dimensioning": (1, 3)}


def _rules_version(proposal: dict[str, Any]) -> int:
    return int(proposal.get("rules_version", 0) or 0)


def _pre_proposal_gate(proposal: dict[str, Any]) -> list[str] | None:
    """v8: before any proposal rule, decide whether a proposal may be written at all.

    An insufficient input returns qualification questions; a request outside the catalog returns
    the missing vendor package. Both block emission for their own reason, whatever else is missing.
    """
    if _rules_version(proposal) < 8:
        return None
    errors: list[str] = []
    assessment = proposal.get("input_assessment") or {}
    status = assessment.get("status")
    if status not in INPUT_STATUSES:
        return ["input_assessment.status ausente ou inválido (sufficient | insufficient)"]
    if status == "insufficient":
        questions = [q for q in proposal.get("open_questions", []) if str(q).strip()]
        if not assessment.get("missing"):
            errors.append("insumo insuficiente sem a lista do que falta (input_assessment.missing)")
        if not 1 <= len(questions) <= MAX_QUALIFICATION_QUESTIONS:
            errors.append(f"insumo insuficiente: devolva de 1 a {MAX_QUALIFICATION_QUESTIONS} perguntas essenciais (open_questions tem {len(questions)})")
        errors.append("GATE insumo_insuficiente: não gerar proposta; devolver as perguntas de qualificação")
        return errors
    client_requirements = [
        item for item in proposal.get("traceability", [])
        if not item.get("hypothesis") and set(item.get("speakers", [])) & {"client", "input_document"}
    ]
    if not _text_value(proposal.get("client_name")) or not client_requirements:
        return ["insumo declarado suficiente sem cliente identificado ou sem requisito do cliente: use input_assessment.status 'insufficient'"]
    fit = proposal.get("catalog_fit") or {}
    if fit.get("status") not in CATALOG_FIT:
        return ["catalog_fit.status ausente ou inválido (fits | no_catalog)"]
    if fit.get("status") == "no_catalog":
        if not fit.get("requested") or not fit.get("reason"):
            errors.append("catalog_fit no_catalog sem o que foi pedido (requested) e o motivo (reason)")
        errors.append(f"GATE sem_catalogo: pedido fora do catálogo disponível ({fit.get('requested')}); requer pacote do fabricante")
        return errors
    return None


def _text_value(value: Any) -> str:
    return " ".join(str(value or "").split())


def sla_applicable_engagements() -> list[str]:
    return list(json.loads(_WHITELIST.read_text(encoding="utf-8")).get("sla_applies_to", []))


def _validate_rules_v8(proposal: dict[str, Any]) -> list[str]:
    """Issues from the diverse-case round: no inherited template text, explicit product states for
    the existing contract, SLA applicability decided by the institution (not by the author)."""
    errors: list[str] = []
    decisions = proposal.get("solution_decisions", [])
    for decision in decisions:
        if decision.get("status") not in PRODUCT_STATUSES:
            errors.append(f"status de produto inválido: {decision.get('product_id')} = {decision.get('status')}")
        if decision.get("status") == "already_contracted" and not decision.get("contract_ref"):
            errors.append(f"produto já contratado sem referência ao contrato vigente (contract_ref): {decision.get('product_id')}")
    if not any(d.get("status") in {"recommended", "optional", "needs_information"} for d in decisions):
        errors.append("nenhum produto do catálogo em avaliação: se o pedido está fora do catálogo, use catalog_fit 'no_catalog'")
    contracted = {d.get("product_id") for d in decisions if d.get("status") == "already_contracted"}
    offered = set(proposal.get("products", []))
    for wave in (proposal.get("optional_phase") or {}).get("waves", []):
        offered |= set(wave.get("components", []))
    for product in sorted(contracted & offered):
        errors.append(f"produto já contratado oferecido de novo: {product}")

    # Texto do documento: todo slot dependente do caso vem do estado.
    document_text = proposal.get("document_text") or {}
    for key in REQUIRED_DOCUMENT_TEXT:
        if not _text_value(document_text.get(key)):
            errors.append(f"document_text.{key} ausente: o compositor não usa texto padrão para este slot")
    for key, (low, high) in REQUIRED_LISTS.items():
        items = [item for item in proposal.get(key) or [] if item]
        if not low <= len(items) <= high:
            errors.append(f"{key} deve ter de {low} a {high} itens (tem {len(items)})")
    if not any(str(s.get("title", "")).casefold() == "resumo executivo" and s.get("paragraphs") for s in proposal.get("sections", [])):
        errors.append("sections sem 'Resumo executivo'")

    # SLA institucional: a aplicabilidade é da instituição (whitelist) ou de uma decisão aprovada do caso.
    engagement = proposal.get("governance", {}).get("engagement_type", {}).get("value")
    applicability = proposal.get("governance", {}).get("sla_applicability") or {}
    if engagement not in sla_applicable_engagements() and not (
        applicability.get("state") == "commitment" and engagement in (applicability.get("value") or [])
    ):
        errors.append(
            f"decisão interna aberta: sla_applicability (a tabela institucional de SLA não está prevista para '{engagement}')"
        )
    return errors


# Palavra que a citação da aprovação precisa conter, por decisão: impede citar a linha de outra decisão.
_APPROVAL_TOPICS = {
    "warranty": ("garantia",),
    "license_supply": ("licen",),
    "engagement_type": ("engajamento", "engagement"),
    "sla_applicability": ("sla",),
}
_ESTIMATE_TOPICS = ("estimativa", "semana")
MIN_QUOTE_LENGTH = 15


def _quote_text(value: Any) -> str:
    """Normalized text for quote matching: table pipes and markup never decide a match."""
    text = re.sub(r"[|*_`>#]", " ", str(value or ""))
    return normalize_document_text(text)


def _validate_approval_quotes(proposal: dict[str, Any], source_text: str) -> list[str]:
    """v9: a case approval exists only if the source material says so, literally.

    Every committed case decision cites `approval_quote`, a verbatim excerpt of the source material
    that names the decision topic and the approver. An approval absent from the material blocks.
    """
    errors: list[str] = []
    source = _quote_text(source_text)
    for key, decision in proposal.get("governance", {}).items():
        if decision.get("state") != "commitment" or is_populos_standard(decision):
            continue
        quote = _quote_text(decision.get("approval_quote"))
        if len(quote) < MIN_QUOTE_LENGTH:
            errors.append(f"aprovação sem citação literal do insumo (approval_quote): {key}")
            continue
        if quote not in source:
            errors.append(f"aprovação citada não existe no insumo (approval_quote): {key}")
            continue
        topics = _ESTIMATE_TOPICS if key.endswith("_estimate") else _APPROVAL_TOPICS.get(key, ())
        if topics and not any(topic in quote for topic in topics):
            errors.append(f"citação da aprovação não trata desta decisão ({'/'.join(topics)}): {key}")
        value = decision.get("approved_value", decision.get("value"))
        if isinstance(value, str) and _quote_text(value) not in quote:
            errors.append(f"valor aprovado não aparece na citação do insumo: {key}")
        approver = _quote_text(str(decision.get("approved_by", "")).split("(")[0]).split(" ")[0]
        if approver and approver not in quote:
            errors.append(f"citação da aprovação não nomeia o aprovador ({decision.get('approved_by')}): {key}")
    return errors


def assert_proposal_rules(proposal: dict[str, Any]) -> None:
    errors = validate_proposal_rules(proposal)
    if errors:
        raise ValueError("Regras v5 violadas: " + "; ".join(errors))
