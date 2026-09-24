# Proposal state schema (rules v7)

The author produces one JSON object. The validator (`scripts/validate_attempt.py`) checks the rules; the compositor maps the fields below into fixed slots of the approved template. Text fields are client-facing Portuguese unless noted. Values in angle brackets are placeholders, not examples to copy.

## Identity and mode

| Field | Type | Notes |
|---|---|---|
| `rules_version` | int | Must be `7`. |
| `data_mode` | `"test"` or `"production"` | Marks where the data comes from. It never relaxes a check. |
| `client_name`, `opportunity`, `code`, `opportunity_id` | string | `code` names the output file. |

## Client scope and governance

- `client_scope`: `{ "type": <engagement the client asked for>, "excludes_implementation": bool, "source": <quote/reference from the source material>, "forbidden_in_committed": [<terms the committed phase may not require, e.g. production-only actions>] }`.
- `governance`: object keyed by decision. Required keys: `engagement_type` (`assessment`, `design`, `implementation`, `phased`), `warranty`, `license_supply`, `sla`. Estimate decisions use a key ending in `_estimate`.
- Each decision: `{ "state": "commitment" | "populos_internal_decision", "value", "approved_value", "source", "approved_by", "approved_at" (YYYY-MM-DD), "approval_record", "mode", "engagement_ref", "approver_role" (estimates), "applies_to" (sla: list of engagement types) }`.
  - A decision is `commitment` only when the source material contains an explicit approval: who, when, and where it is recorded (`approval_record`). Otherwise keep `populos_internal_decision` with `value: null`; emission then blocks, which is the correct outcome.
  - `approved_value` equals `value`. `engagement_ref` equals the current `engagement_type` value.
  - An institutional standard (such as the fixed SLA table) is not approved per case: use `{ "state": "commitment", "basis": "populos_standard", "value", "source", "template_version": <current template version>, "applies_to": [...] }`, without approver fields.

## Discovery and provenance

- `discovery.business_goals`: list of strings, verb first, ending with the REQ ids in parentheses.
- `traceability`: `[{ "requirement_id": "REQ-nn", "requirement", "solution", "evidence", "source": <reference into the source material>, "speakers": ["client" | "vendor" | "input_document"], "hypothesis": bool }]`. A requirement supported only by a vendor statement sets `hypothesis: true`.
- `source_coverage`: every relevant statement of the source material: `{ "ref", "statement", "status": "coberto" | "pendente" | "descartado", "targets": [REQ ids or "sumário", "escopo", "exclusões", "premissas", "dimensionamento", "engajamento"], "reason" (when discarded) }`.
- `client_numbers`: every number the client said: `{ "quote", "ref", "destination": "meta" | "contexto_de_dor" | "dimensionamento" | "descartado_com_motivo", "summary_marker" (pain context: a phrase that appears in the executive summary), "reason" }`.
- `open_questions`: list of strings.

## Solution

- `solution_decisions`: one entry per catalog product evaluated: `{ "product_id" (catalog id), "status": "recommended" | "optional" | "needs_information" | "excluded", "requirement_ids", "rationale", "client_summary", "capabilities" (up to 3 shown), "implementation_status" ("modality_pending" when applicable), "trigger" (optional products: business reason and prerequisite) }`.
- `products`: ids of recommended products.
- `architecture.summary`: one paragraph.
- `sections`: `[{ "title": "Resumo executivo", "paragraphs": [...] }]`.

## Sizing, scope and delivery

- `dimensioning`: up to 3 rows `[item, quantity, planning basis, classification]`; classification `Confirmado`, `Pendente` or `Estimativa` (an estimate needs a technical owner).
- `estimates`: `[{ "item", "value", "owner", "owner_role": "arquiteto" | "engenharia" | "delivery" | "pré-vendas técnica" }]`.
- `assessment_items`: exactly 3 strings (section 5).
- `scope`: `{ "included": [...], "deliverables": [...], "excluded": [...] }`.
- `delivery.phases`: committed phases, at most 4: `{ "name", "kind", "weeks": [min, max], "duration", "objective", "dependency", "outputs": [...] }`. Every week range written in client text must equal the sum of these phases.
- `delivery.responsibilities`: client-side parties; `populos_roles`: optional list of `[role, responsibility, commitment]` rows (table capacity 12 rows in total).
- `optional_phase` (optional): `{ "title", "intro", "conditions": [...], "waves": [{ "id", "name", "components": [product ids], "goes_to_production": bool, "activities", "acceptance", "milestone" }] }`. Each recommended product appears in exactly one wave.
- `fast_track` (optional): `{ "id", "title", "components", "production_change": bool, "controls": ["janela", "reversão", "aprovação"], "deadline_reference": "freeze", "first_question", "paragraphs", "items", "schedule_row", "lead_times": { "licenciamento": { "weeks", "source" } } }`. When the license lead time is unknown, use `{ "weeks": null, "pending_question": <question> }` instead of estimating.
- `assumptions` (up to 8), `restrictions` (exactly 4), `risks`: `[{ "risk", "impact", "mitigation" }]`.
- `acceptance_criteria`: `[{ "requirement_id", "phase": "committed" | "optional", "option_id" (for optional: the id of the wave or fast track), "criterion" }]`. Every option that touches production has at least one criterion of its own.

## Critical events

- `event_readiness`: list of strings.
- `critical_events`: `[{ "name", "date" (YYYY-MM-DD or null), "source", "pending_question" (when date is null) }]`.
- `event_feasibility`: for each event with a date: `{ "event", "reference_date", "phase1_end_earliest", "phase1_end_latest", "classification": "fits" | "partially_fits" | "does_not_fit", "path", "reason", "summary_marker", "lead_times": { "licenciamento": { "weeks", "source" } or { "weeks": null, "pending_question" } } }`. With an unknown lead time the classification cannot be `fits`. The end dates are the reference date plus the sum of committed phase weeks, and the summary states them.

## Client text overrides

`document_text`: optional object with case-specific paragraphs for fixed template slots: `about_akamai`, `about_solution`, `partnership`, `coverage`, `readiness_intro`, `dimensioning_intro`, `heading_6`, `methodology_intro`, `knowledge_transfer`, `tests`, `schedule_intro`, `schedule_sequence`, `acceptance_intro`, `acceptance_optional_intro`, `warranty_intro`, `closing`, `callout_limits`, `callout_migration`, `callout_milestones`, `license_prefix`, `diagram_origins_title`, `diagram_origins`. Omitted keys fall back to generic wording.
