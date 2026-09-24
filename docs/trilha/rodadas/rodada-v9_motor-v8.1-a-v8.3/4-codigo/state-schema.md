# Proposal state schema (rules v9)

The author produces one JSON object. The validator (`scripts/validate_attempt.py`) checks the rules; the compositor maps the fields below into fixed slots of the approved template. Text fields are client-facing Portuguese unless noted. Values in angle brackets are placeholders, not examples to copy.

## Identity and mode

| Field | Type | Notes |
|---|---|---|
| `rules_version` | int | Must be `9`. |
| `data_mode` | `"test"` or `"production"` | Marks where the data comes from. It never relaxes a check. |
| `client_name`, `opportunity`, `code`, `opportunity_id` | string | `code` names the output file. |

## Before the proposal: input and catalog

Both fields are required and are checked before any other rule.

- `input_assessment`: `{ "status": "sufficient" | "insufficient", "missing": [<what is missing>], "reason" }`. Use `insufficient` when the material does not identify the client or does not state at least one concrete need about identifiable assets. Then write only `input_assessment` and `open_questions` (1 to 8 essential qualification questions): no products, sections or scope. The validator returns the gate `insumo_insuficiente`, which is the correct outcome.
- `catalog_fit`: `{ "status": "fits" | "no_catalog", "requested": <what the client asked for>, "reason" }`. Use `no_catalog` when the request is for a technology or vendor that the supplied catalog does not cover. Do not map it onto unrelated catalog products. The validator returns the gate `sem_catalogo`.

## Client scope and governance

- `client_scope`: `{ "type": <engagement the client asked for>, "excludes_implementation": bool, "source": <quote/reference from the source material>, "forbidden_in_committed": [<terms the committed phase may not require, e.g. production-only actions>] }`.
- `governance`: object keyed by decision. Required keys: `engagement_type` (`assessment`, `design`, `implementation`, `phased`), `warranty`, `license_supply`, `sla`. Estimate decisions use a key ending in `_estimate`.
- Each decision: `{ "state": "commitment" | "populos_internal_decision", "value", "approved_value", "source", "approved_by", "approved_at" (YYYY-MM-DD), "approval_record", "mode", "engagement_ref", "approver_role" (estimates), "approval_quote" }`.
  - A decision is `commitment` only when the source material contains an explicit approval: who, when, and where it is recorded (`approval_record`). Otherwise keep `populos_internal_decision` with `value: null`; emission then blocks, which is the correct outcome.
  - `approved_value` equals `value`. `engagement_ref` equals the current `engagement_type` value.
  - `approval_quote` is a verbatim excerpt of the source material that records the approval: it names the decision, the approver and the approved value (for a table, the whole row). The validator looks for it in the source material; an approval that is not written there does not exist.
  - An institutional standard is not approved per case. Only `sla` is an institutional decision; every other decision belongs to the case, even when it repeats an existing contract. For `sla`: use `{ "state": "commitment", "basis": "populos_standard", "value", "source", "template_version": <current template version> }`, without approver fields.
  - The engine decides where the institutional SLA table applies. For an engagement type outside that list, the case needs an approved decision `sla_applicability` (a commitment whose `value` lists the engagement types). Without it, emission blocks as an internal decision; do not create it without an explicit approval in the source material.

## Discovery and provenance

- `discovery.business_goals`: list of strings, verb first, ending with the REQ ids in parentheses.
- `traceability`: `[{ "requirement_id": "REQ-nn", "requirement", "solution", "evidence", "source": <reference into the source material>, "speakers": ["client" | "vendor" | "input_document"], "hypothesis": bool }]`. A requirement supported only by a vendor statement sets `hypothesis: true`.
- `source_coverage`: every relevant statement of the source material: `{ "ref", "statement", "status": "coberto" | "pendente" | "descartado", "targets": [REQ ids or "sumário", "escopo", "exclusões", "premissas", "dimensionamento", "engajamento"], "reason" (when discarded) }`.
- `client_numbers`: every number the client said: `{ "quote", "ref", "destination": "meta" | "contexto_de_dor" | "dimensionamento" | "descartado_com_motivo", "summary_marker" (pain context: a phrase that appears in the executive summary), "reason" }`.
- `open_questions`: list of strings.

## Solution

- `solution_decisions`: one entry per catalog product evaluated: `{ "product_id" (catalog id), "status": "recommended" | "optional" | "needs_information" | "excluded" | "already_contracted", "requirement_ids", "rationale", "client_summary", "capabilities" (up to 3 shown), "implementation_status" ("modality_pending" when applicable), "trigger" (optional products: business reason and prerequisite), "contract_ref" (already_contracted: the current contract it belongs to) }`. A product the client already has is `already_contracted`: it is shown as the current environment and is never offered again in `products` or in a wave.
- `products`: ids of recommended products.
- `architecture.summary`: one paragraph.
- `sections`: `[{ "title": "Resumo executivo", "paragraphs": [...] }]`.

## Sizing, scope and delivery

- `dimensioning`: 1 to 3 rows (required) `[item, quantity, planning basis, classification]`; classification `Confirmado`, `Pendente` or `Estimativa`. An `Estimativa` row needs an entry in `estimates` whose `item` is the same text as the row's item, with a technical owner.
- `estimates`: `[{ "item", "value", "owner", "owner_role": "arquiteto" | "engenharia" | "delivery" | "pré-vendas técnica" }]`.
- `assessment_items`: exactly 3 strings (section 5).
- `client_roles`: 1 to 4 strings, the client-side roles this project needs (section 8.2).
- `scope`: `{ "included": [...], "deliverables": [...], "excluded": [...] }`.
- `delivery.phases`: committed phases, at most 4: `{ "name", "kind", "weeks": [min, max], "duration", "objective", "dependency", "outputs": [...] }`. A week range written in client text must equal the sum of these phases, or the range of one phase.
- `delivery.responsibilities`: client-side parties, as `[{ "party", "responsibility" }]`; `populos_roles`: optional list of `[role, responsibility, commitment]` rows (table capacity 12 rows in total).
- `optional_phase` (optional): `{ "title", "intro", "conditions": [...], "waves": [{ "id", "name", "components": [product ids], "goes_to_production": bool, "activities", "acceptance", "milestone" }] }`. Each recommended product appears in exactly one wave.
- `fast_track` (optional): `{ "id", "title", "components", "production_change": bool, "controls": ["janela", "reversão", "aprovação"], "deadline_reference": "freeze", "first_question", "paragraphs", "items", "schedule_row", "lead_times": { "licenciamento": { "weeks", "source" } } }`. When the license lead time is unknown, use `{ "weeks": null, "pending_question": <question> }` instead of estimating.
- `assumptions` (up to 8), `restrictions` (exactly 4, required), `risks`: `[{ "risk", "impact", "mitigation" }]`.
- `acceptance_criteria`: `[{ "requirement_id", "phase": "committed" | "optional", "option_id" (for optional: the id of the wave or fast track), "criterion" }]`. Every option that touches production has at least one criterion of its own.

## Critical events

- `event_readiness`: list of strings.
- `critical_events`: `[{ "name", "date" (YYYY-MM-DD or null), "source", "pending_question" (when date is null) }]`.
- `event_feasibility`: for each event with a date: `{ "event", "reference_date", "phase1_end_earliest", "phase1_end_latest", "classification": "fits" | "partially_fits" | "does_not_fit", "path", "reason", "summary_marker", "lead_times": { "licenciamento": { "weeks", "source" } or { "weeks": null, "pending_question" } } }`. With an unknown lead time the classification cannot be `fits`. The end dates are the reference date plus the sum of committed phase weeks, and the summary states them.

## Client text

`document_text`: case-specific paragraphs for fixed template slots. The compositor has no default text for these slots, so each one is required: `about_solution`, `coverage`, `dimensioning_intro`, `methodology_intro`, `tests`, `schedule_intro`, `schedule_sequence`, `closing`, `callout_migration`, `callout_milestones`, `diagram_users` and `diagram_users_detail` (who uses the service and through what), `diagram_origins_title` and `diagram_origins` (where the client's applications run). Optional keys: `about_akamai`, `partnership`, `readiness_intro`, `dimensioning_note`, `heading_6`, `knowledge_transfer`, `acceptance_intro`, `acceptance_optional_intro`, `warranty_intro`, `callout_limits`, `license_prefix`; omitted optional keys use neutral wording. `sections` must contain the `Resumo executivo`.
