"""Feasibility against critical events, computed by the engine (auditoria v10: N1, N2, A4).

The author declares only inputs: the proposal date, the event and freeze dates, the ordered path of steps that
must happen before the event (committed phases, optional waves, lead times such as licensing) and, when approved,
a stabilization buffer. The engine computes every date and classification, so three authors reading the same
source material produce the same dates, and no date in the proposal comes from mental arithmetic.
"""
from __future__ import annotations

import math
import re
import unicodedata
from dataclasses import dataclass, field
from datetime import date, timedelta
from typing import Any

MONTHS = {"janeiro": 1, "fevereiro": 2, "marco": 3, "abril": 4, "maio": 5, "junho": 6, "julho": 7,
          "agosto": 8, "setembro": 9, "outubro": 10, "novembro": 11, "dezembro": 12}


@dataclass
class Step:
    ref: str
    label: str
    weeks: tuple[int, int] | None  # None: unknown duration (a lead time without a source)
    pending_question: str = ""


@dataclass
class Feasibility:
    event: str
    event_date: date
    target: date                     # latest completion date: event or freeze start, minus stabilization
    target_reason: str
    classification: str              # fits | partially_fits | does_not_fit | conditional
    end_earliest: date | None
    end_latest: date | None
    start_deadline: date | None      # latest date to start the first step
    step_deadlines: dict[str, date] = field(default_factory=dict)  # unknown steps: latest date they must be done
    caveats: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    start: date | None = None
    steps: list[str] = field(default_factory=list)
    after_unknown: tuple[int, int] | None = None  # semanas conhecidas depois do último passo sem prazo

    def dates(self) -> list[date]:
        values = [self.event_date, self.target, self.end_earliest, self.end_latest, self.start_deadline, *self.step_deadlines.values()]
        return [value for value in values if value]


def _iso(value: Any) -> date | None:
    try:
        return date.fromisoformat(str(value))
    except ValueError:
        return None


def _weeks(value: Any) -> tuple[int, int] | None:
    if isinstance(value, int):
        return (value, value)
    if isinstance(value, (list, tuple)) and len(value) == 2 and all(isinstance(v, int) for v in value):
        return (value[0], value[1])
    return None


def stabilization_days(proposal: dict[str, Any]) -> int | None:
    """Calendar days of the approved stabilization buffer, or None when no buffer was approved.

    There is no institutional default: the buffer exists only as an approved decision of the case.
    """
    decision = proposal.get("governance", {}).get("stabilization_buffer") or {}
    if decision.get("state") != "commitment":
        return None
    match = re.search(r"(\d+)\s*dias?\s*(úteis|uteis|corridos)?", str(decision.get("value", "")), re.IGNORECASE)
    if not match:
        return None
    days = int(match.group(1))
    business = (match.group(2) or "").casefold().startswith(("út", "ut"))
    return math.ceil(days * 7 / 5) if business else days


def _steps(proposal: dict[str, Any], item: dict[str, Any]) -> tuple[list[Step], list[str]]:
    phases = {p.get("name"): p for p in proposal.get("delivery", {}).get("phases", [])}
    waves = {w.get("id"): w for w in (proposal.get("optional_phase") or {}).get("waves", []) if w.get("id")}
    leads = item.get("lead_times") or {}
    steps, errors = [], []
    for ref in item.get("path", []):
        if ref in phases:
            steps.append(Step(ref, str(ref), _weeks(phases[ref].get("weeks"))))
        elif ref in waves:
            weeks = _weeks(waves[ref].get("weeks"))
            if weeks is None:
                errors.append(f"onda opcional no caminho sem faixa de semanas (weeks): {ref}")
            steps.append(Step(ref, f"{waves[ref].get('name', ref)} (opcional)", weeks))
        elif ref in leads:
            lead = leads[ref] or {}
            weeks = _weeks(lead.get("weeks"))
            if weeks is None and not lead.get("pending_question"):
                errors.append(f"prazo desconhecido sem pergunta aberta (lead_times.{ref}.pending_question): {item.get('event')}")
            if weeks is not None and not lead.get("source"):
                errors.append(f"prazo sem origem (lead_times.{ref}.source): {item.get('event')}")
            steps.append(Step(ref, str(lead.get("label") or ref), weeks, str(lead.get("pending_question") or "")))
        else:
            errors.append(f"passo do caminho não é fase, onda nem prazo declarado: {ref} ({item.get('event')})")
    for ref in leads:
        if ref not in item.get("path", []):
            errors.append(f"prazo declarado fora do caminho até o evento: {ref} ({item.get('event')})")
    return steps, errors


def compute(proposal: dict[str, Any]) -> list[Feasibility]:
    start = _iso(proposal.get("proposal_date"))
    events = {e.get("name"): e for e in proposal.get("critical_events", [])}
    buffer = stabilization_days(proposal)
    results = []
    for item in proposal.get("event_feasibility", []):
        event = events.get(item.get("event")) or {}
        event_date = _iso(event.get("date"))
        if not start or not event_date:
            continue
        steps, errors = _steps(proposal, item)
        caveats: list[str] = []
        target, reason = event_date, f"{item.get('event')} em {event_date:%d/%m/%Y}"
        freeze_ref = item.get("freeze")
        if freeze_ref:
            freeze = events.get(freeze_ref) or {}
            freeze_date = _iso(freeze.get("date"))
            if freeze_date is None:
                caveats.append(f"a data do congelamento de mudanças ({freeze_ref}) não foi informada; o prazo considera o evento, sem congelamento")
            elif freeze_date < target:
                target, reason = freeze_date, f"início de {freeze_ref} em {freeze_date:%d/%m/%Y}"
        if buffer is None:
            caveats.append("não há folga de estabilização aprovada: a conclusão pode coincidir com a data limite")
        else:
            target -= timedelta(days=buffer)
            reason += f", menos {buffer} dias corridos de estabilização"
        unknown = [s for s in steps if s.weeks is None]
        low = sum(s.weeks[0] for s in steps if s.weeks)
        high = sum(s.weeks[1] for s in steps if s.weeks)
        step_deadlines: dict[str, date] = {}
        for index, step in enumerate(steps):
            if step.weeks is None:
                after = sum(s.weeks[1] for s in steps[index + 1:] if s.weeks)
                step_deadlines[step.label] = target - timedelta(weeks=after)
                caveats.append(f"{step.label}: prazo desconhecido ({step.pending_question or 'pergunta aberta'})")
        start_deadline = target - timedelta(weeks=high) if not unknown else None
        end_earliest = start + timedelta(weeks=low) if not unknown else None
        end_latest = start + timedelta(weeks=high) if not unknown else None
        if unknown or (freeze_ref and _iso((events.get(freeze_ref) or {}).get("date")) is None):
            classification = "conditional"
        elif end_latest <= target:
            classification = "fits"
        elif end_earliest > target:
            classification = "does_not_fit"
        else:
            classification = "partially_fits"
        results.append(Feasibility(str(item.get("event")), event_date, target, reason, classification,
                                   end_earliest, end_latest, start_deadline, step_deadlines, caveats, errors,
                                   start, [s.label for s in steps], _after_unknown(steps)))
    return results


def _after_unknown(steps: list[Step]) -> tuple[int, int] | None:
    unknown = [i for i, s in enumerate(steps) if s.weeks is None]
    if not unknown:
        return None
    rest = [s.weeks for s in steps[unknown[-1] + 1:] if s.weeks]
    return (sum(w[0] for w in rest), sum(w[1] for w in rest)) if rest else None


CLASSIFICATION_TEXT = {
    "fits": "cabe no prazo",
    "partially_fits": "cabe apenas no cenário mais rápido",
    "does_not_fit": "não cabe no prazo",
    "conditional": "depende de informações pendentes",
}


def paragraph(result: Feasibility) -> str:
    """Client-facing feasibility paragraph, written by the engine (never by the author)."""
    parts = [f"Viabilidade frente a {result.event} ({result.event_date:%d/%m/%Y}): {CLASSIFICATION_TEXT[result.classification]}."]
    if result.target != result.event_date or "," in result.target_reason:
        parts.append(f"A data limite considerada é {result.target:%d/%m/%Y} ({result.target_reason}).")
    if result.end_earliest and result.end_latest:
        parts.append(f"Com início em {result.start:%d/%m/%Y} e a sequência {' → '.join(result.steps)}, a conclusão fica entre "
                     f"{result.end_earliest:%d/%m/%Y} e {result.end_latest:%d/%m/%Y}.")
    if result.start_deadline:
        parts.append(f"Para cumprir a data limite, o início deve ocorrer até {result.start_deadline:%d/%m/%Y}.")
    for label, deadline in result.step_deadlines.items():
        parts.append(f"Prazo limite para a etapa \"{label}\": {deadline:%d/%m/%Y}.")
    if result.after_unknown:
        low, high = result.after_unknown
        parts.append(f"Depois das pendências, a execução leva de {low} a {high} semanas.")
    if result.caveats:
        parts.append("Ressalvas: " + "; ".join(result.caveats) + ".")
    return " ".join(parts)


_DATE = re.compile(r"(?<!\d)(\d{1,2})/(\d{1,2})(?:/(\d{2,4}))?(?!\d)")
_ISO = re.compile(r"(?<!\d)(\d{4})-(\d{2})-(\d{2})(?!\d)")
_WRITTEN = re.compile(r"(?<!\d)(\d{1,2})(?:o|º)?\s+de\s+([a-z]+)", re.IGNORECASE)


def day_months(text: str) -> set[tuple[int, int]]:
    """Every (day, month) written in a text: 11/01, 11/01/2027, 2027-01-11 or 11 de janeiro."""
    plain = unicodedata.normalize("NFKD", str(text)).encode("ascii", "ignore").decode().casefold()
    found = {(int(d), int(m)) for d, m, _ in _DATE.findall(plain)}
    found |= {(int(d), int(m)) for _, m, d in _ISO.findall(plain)}
    found |= {(int(d), MONTHS[m]) for d, m in _WRITTEN.findall(plain) if m in MONTHS}
    return {(d, m) for d, m in found if 1 <= d <= 31 and 1 <= m <= 12}
