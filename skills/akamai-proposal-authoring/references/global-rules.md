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

## Client-facing language

Never expose pipeline or drafting language. The single source for forbidden and untranslated terms is `lexicon.json`, consumed by code. Rewrite internal terms as proposal language such as `levantamento`, `premissa de dimensionamento`, `condição de contratação`, or a named requirement.
