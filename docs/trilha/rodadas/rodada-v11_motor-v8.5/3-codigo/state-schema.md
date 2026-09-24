# Proposal state schema (rules v11)

The author produces one JSON object. The validator (`scripts/validate_attempt.py`) checks the rules; the compositor maps the fields below into fixed slots of the approved template. Text fields are client-facing Portuguese unless noted. Values in angle brackets are placeholders, not examples to copy.

## Identity and mode

| Field | Type | Notes |
|---|---|---|
| `rules_version` | int | Must be `11`. |
| `proposal_date` | YYYY-MM-DD | The proposal date given in `request.json`. |
| `data_mode` | `"test"` or `"production"` | Marks where the data comes from. It never relaxes a check. |
| `client_name`, `opportunity`, `code`, `opportunity_id` | string | `code` names the output file. |

## Formal shape

`state.schema.json` (same folder) is the formal JSON Schema of this state. The validator checks it before any rule; a shape error comes back as `formato (<path>): <message>`.

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
  - An institutional standard is not approved per case. Only `sla` is an institutional decision; every other decision belongs to the case, even when it repeats an existing contract. For `sla`: use `{ "state": "commitment", "basis": "populos_standard", "value", "source", "template_version": <current template version> }`, without approver fields. The values of the institutional SLA table are in `institutional-standards.json`; compare client demands with them before classifying a conflict.
  - The engine decides where the institutional SLA table applies. For an engagement type outside that list, the case needs an approved decision `sla_applicability` (a commitment whose `value` lists the engagement types). Without it, emission blocks as an internal decision; do not create it without an explicit approval in the source material.

## Discovery and provenance

- `discovery.business_goals`: list of strings, verb first, ending with the REQ ids in parentheses.
- `traceability`: `[{ "requirement_id": "REQ-nn", "requirement", "solution", "evidence", "source": <reference into the source material>, "speakers": ["client" | "vendor" | "input_document"], "hypothesis": bool }]`. A requirement supported only by a vendor statement sets `hypothesis: true`.
- `source_coverage`: every relevant statement of the source material: `{ "ref", "statement", "status": "coberto" | "pendente" | "descartado", "targets": [REQ ids or "sumário", "escopo", "exclusões", "premissas", "dimensionamento", "engajamento"], "reason" (when discarded) }`.
- `client_numbers`: every number the client said: `{ "quote", "ref", "destination": "meta" | "contexto_de_dor" | "dimensionamento" | "descartado_com_motivo", "summary_marker" (pain context: a phrase that appears in the executive summary), "reason" }`.
- `open_questions`: list of strings.
- `standard_conflicts`: `[{ "category": "sla" | "warranty" | "qualification" | "deadline", "requirement_id", "status": "conflict" | "compatible" | "client_clarification", "decision_key" (conflict), "reason" (compatible), "clarification_question" (client_clarification) }]`. When the client's own documents contradict each other (e.g. two different deadlines in the same TR), the status is `client_clarification`: it is not a POPULOS decision, and the clarification question also goes to `open_questions`. Every client requirement about service levels, warranty, qualification or certification, or delivery deadlines is classified here. A `conflict` with a POPULOS standard points to a governance decision (`decision_key`), which stays `populos_internal_decision` unless the source material approves it. The code only detects these four categories; recognizing any other conflict with a POPULOS standard remains the author's responsibility.

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
- `team_competencies`: 1 to 3 strings, the POPULOS team competencies this project needs (section 1).
- `scope`: `{ "included": [...], "deliverables": [...], "excluded": [...] }`.
- `delivery.phases`: committed phases, at most 4: `{ "name", "kind", "weeks": [min, max], "duration", "objective", "dependency", "outputs": [...] }`. A week range written in client text must equal the sum of these phases, or the range of one phase.
- `delivery.responsibilities`: client-side parties, as `[{ "party", "responsibility" }]`; `populos_roles`: optional list of `[role, responsibility, commitment]` rows (table capacity 12 rows in total).
- `optional_phase` (optional): `{ "title", "intro", "conditions": [...], "waves": [{ "id", "name", "components": [product ids], "weeks": [min, max], "goes_to_production": bool, "activities", "acceptance", "milestone" }] }`. A wave's range (and the sum of the waves) may be written in client text exactly as approved. Each recommended product appears in exactly one wave.
- `fast_track` (optional): `{ "id", "title", "components", "production_change": bool, "controls": ["janela", "reversão", "aprovação"], "deadline_reference": "freeze", "first_question", "paragraphs", "items", "schedule_row", "lead_times": { "licenciamento": { "weeks", "source" } } }`. When the license lead time is unknown, use `{ "weeks": null, "pending_question": <question> }` instead of estimating.
- `assumptions` (up to 8), `restrictions` (exactly 4, required), `risks`: `[{ "risk", "impact", "mitigation" }]`.
- `acceptance_criteria`: `[{ "requirement_id", "phase": "committed" | "optional", "option_id" (for optional: the id of the wave or fast track), "criterion" }]`. Every option that touches production has at least one criterion of its own.

## Critical events and dates

Do not compute dates. You declare the inputs; the engine computes every window, deadline and classification and writes the feasibility paragraph into the executive summary.

- `critical_events`: `[{ "name", "kind": "event" | "freeze", "date" (YYYY-MM-DD or null), "source", "pending_question" (when date is null) }]`. A change freeze is its own entry with `kind: "freeze"`.
- `event_feasibility`: for each dated event: `{ "event", "freeze": <freeze name or null>, "path": [ordered steps before the event], "lead_times": { "<key>": { "label", "weeks": [min, max] or null, "source", "pending_question" } } }`. Each step of `path` is a committed phase name, an optional wave id or a key of `lead_times` (for example `licenciamento`). Every declared lead time is on the path. An unknown lead time has `weeks: null` and a pending question; the engine turns it into the date by which that step must be done.
- Stabilization before an event exists only as an approved case decision `governance.stabilization_buffer` (e.g. value "5 dias úteis"). There is no default: without it, the engine states that no buffer was considered.
- `event_readiness`: `[{ "text", "phase" }]`, where `phase` is a committed phase name, an optional wave id or the fast-track id. Proportional to the scope: war room, load test and capacity review only when a recommended product sits in the application traffic path.
- Any date written in client text must appear in the source material or come from the engine's calculation; a date computed by hand blocks.
- For an engagement type outside the institutional SLA scope, the approved `sla_applicability` lists the phases or options it covers in `applies_to_phases`; the document then states that the table applies only to them.

## Client text

`document_text`: case-specific paragraphs for fixed template slots. The compositor has no default text for these slots, so each one is required: `about_akamai`, `about_solution`, `partnership`, `coverage`, `dimensioning_intro`, `assessment_outcome` (what the survey of section 5 delivers), `methodology_intro`, `knowledge_transfer`, `tests`, `schedule_intro`, `schedule_sequence`, `closing`, `callout_qualifications`, `callout_limits`, `callout_migration`, `callout_milestones`, `diagram_users` and `diagram_users_detail`, `diagram_origins_title` and `diagram_origins`, and `front_titles` (an object with one title for each front present: `continuity` for Edge DNS, GTM, ALB and Ion; `protection` for App & API Protector and Prolexic; `automation` for Bot Manager and Account Protector). Optional keys: `readiness_intro`, `dimensioning_note`, `heading_6`, `acceptance_intro`, `acceptance_optional_intro`, `warranty_intro`, `license_prefix`. `sections` must contain the `Resumo executivo`. No client-facing text may mention a capability, product or deliverable outside the decisions of this state, and products are always named by their commercial name, never by the catalog id.
