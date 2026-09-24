# Global rules

- Every material statement carries one governance state: `commitment`, `assumption`, `client_pending`, or `populos_internal_decision`.
- `commitment` requires an approved client fact, POPULOS standard, contract, or explicit internal approval.
- `assumption` is visible, bounded, testable, and names its validation gate.
- `client_pending` identifies information or approval owed by the client and may appear in the proposal when its consequence is clear.
- `populos_internal_decision` identifies a POPULOS commercial or contractual choice. It blocks emission and never appears in a client-facing document.
- Evidence classification remains `client_fact`, `populos_standard`, or `bounded_estimate` for committed and assumed statements.
- `client_fact` requires a meeting, TR, questionnaire, or client-provided evidence.
- `populos_standard` requires an approved institutional template, policy, catalog, or contractual clause.
- `bounded_estimate` must state its range, assumptions, dependencies, and validation gate.
- Assumptions are labeled and never presented as confirmed facts.
- Client pending information remains visible and blocks commitments that depend on it.
- Product status is one of `recommended`, `optional`, `needs_information`, or `excluded`.
- Commercial or contractual terms require an approved source. Template placeholders are not institutional standards.
- The fixed SLA table in the approved POPULOS template is institutional. Do not weaken it with language saying that definitive levels will be established later.
- Warranty duration and license supply model are internal POPULOS decisions unless an approved opportunity-specific source resolves them.
- The approved neutral DOCX is the layout and section authority; the structured proposal state is the content authority.
- Human gates occur after discovery normalization and after architecture/product selection.

The global state separates client facts, requirements, decisions, scope, commercial conditions, QA findings, and document-manifest data. Each agent receives only the slice needed for its task.

## Fidelity to the source material (rules v5)

- `engagement_type` (`assessment`, `design`, `implementation`, `phased`) is a client fact or a registered POPULOS decision. Never infer it. When the client scope excludes implementation, committed phases carry no production change.
- A contradiction between the client scope and the template, or between sections, is resolved by asking, never by expanding scope.
- Every requirement and every `client_fact` carries a source reference such as `transcrição [00:01:10]` or `requisito original 3`. Without a reference it is not a fact.
- Reverse coverage: every relevant statement of the source material ends as covered (REQ, scope, assumption, dimensioning, summary), pending, or discarded with a reason.
- Every number said by the client has a declared destination: `meta`, `contexto_de_dor`, `dimensionamento`, or `descartado_com_motivo`. Pain context may quote the number; a commitment may not.
- A `bounded_estimate` needs an identified owner. Without one it becomes `client_pending` or is removed.
- Any integration that exports data (SIEM, logs, analytics) carries a sensitive-data control when a privacy requirement exists.
- A wave is a contractual unit: every wave that reaches production has its own acceptance milestone, and every recommended product is named in exactly one wave.
- When a schedule depends on an external date (freeze, event, client window), the calendar duration is stated as conditional. Declared week ranges must equal the sum of the phases.
- Case decisions (warranty, license supply, engagement, estimates) are scoped to one opportunity id and are never reused as few-shot examples.

## Decisions, provenance and feasibility (rules v6 and v7)

- A decision is committed only with an explicit approval written in the source material: approver, ISO date, a record of where the approval happened, and a verbatim quote of it. Moving on without objecting is not approval. The approved text is kept verbatim; context goes outside it.
- A decision is bound to the engagement type it was made for. When the engagement changes, dependent decisions reopen. An institutional block (such as the SLA table) is emitted only where the institution declares it applicable, or where an approved case decision extends it.
- `data_mode: test` marks the origin of the data. It never disables a check.
- An institutional standard is versioned with the approved template and is not approved per case.
- An effort estimate has a technical owner (architect, engineering, delivery, or technical presales).
- Provenance records who said it: client, vendor, or input document. A requirement supported only by the vendor is a hypothesis to validate.
- Committed deliverables and acceptance criteria never require an action that the scope boundary forbids.
- For a critical event with a known date, feasibility is computed in the proposal from the proposal date, including the license lead time, and stated in the executive summary. An unknown lead time is an open question, never an estimate, and rules out a `fits` classification. A dateless event becomes an open question.
- Every option that touches production (a wave, a fast track) declares it, has its own window, rollback, approval, and acceptance criteria, and must fit before the change freeze, not only before the event.

## Before writing a proposal (rules v8)

- First decide whether a proposal can be written. When the material does not identify the client or a concrete need, the outcome is a short list of qualification questions, not a proposal.
- When the request is for a technology the supplied catalog does not cover, the outcome is the declared gap. Catalog products are never stretched to fit an unrelated request.
- Products the client already has belong to the current environment. They are not offered again and are not treated as exclusions.
- Every case-dependent paragraph comes from the state. The compositor holds no text from any previous case.

## Verification method

- Test parameters defined by POPULOS (number of resolvers, observation windows, measurement frequency) are verification method, not a promised result. State them as how acceptance is checked, never as a service level.

## Client-facing language

Never expose pipeline or drafting language. The single source for forbidden and untranslated terms is `lexicon.json`, consumed by code. Rewrite internal terms as proposal language such as `levantamento`, `premissa de dimensionamento`, `condição de contratação`, or a named requirement.
