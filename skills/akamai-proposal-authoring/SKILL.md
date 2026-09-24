---
name: akamai-proposal-authoring
description: Transform discovery notes into a client-specific Akamai technical proposal with evidence-based product selection, modular sections, traceability, and measurable acceptance criteria. Use for proposal planning, generation, audit, or repair; do not use as a fixed product brochure.
---

# Akamai Proposal Authoring

Create the smallest complete proposal that explains the client's problem, the recommended solution, how it will be delivered, and how acceptance will be demonstrated.

## Non-negotiable rules

- Treat the approved POPULOS neutral template as the structural and visual authority. Preserve its 13-section decision path, identity, headers, footers, tables, and callout language.
- The template is not a product checklist. Lines, rows, fronts, certifications, quantities, warranty terms, and product modules remain conditional. Fixed SLA text in the approved template is an institutional commitment; a warranty placeholder is not.
- Select a product only when at least one discovery requirement supports it. Record the requirement IDs, rationale, confidence, and status.
- Use `recommended`, `optional`, `needs_information`, or `excluded` consistently. Only recommended products belong in the primary architecture and scope.
- Do not reuse a product image merely because it exists in the source template. Include an asset only when it explains the selected architecture and its metadata is current.
- Do not invent capacity, traffic, price, duration, warranty, certification, topology, or contractual commitment. A missing client input becomes a client pending item; a missing POPULOS commercial choice becomes an internal decision and blocks emission.
- Keep client facts, assumptions, recommendations, and unresolved items distinguishable.
- Every must-have requirement must map to a solution decision and an acceptance criterion, or remain visibly open.
- Omit empty or irrelevant sections. A short relevant proposal is preferable to a long catalogue.
- Keep technical claims inside the approved catalog supplied to the model. Avoid undated scale statistics and generic marketing claims.

## Workflow

1. Normalize the meeting into goals, pain points, requirements, constraints, volumes, dependencies, stakeholders, and open questions.
2. Decide whether the material supports a proposal (`input_assessment`) and whether the catalog covers the request (`catalog_fit`). If not, stop with the questions or the declared gap.
3. Evaluate each catalog product independently. Do not begin with a preselected bundle.
4. Apply the product gating criteria in [solution gating](references/solution-gating.md).
5. Produce solution decisions and a requirement traceability matrix.
6. Map the decisions onto the sections in [section model](references/section-model.md).
7. Run a critic pass. Block unsupported products, absolute promises, hidden open questions, unmeasurable acceptance criteria, and unresolved internal POPULOS decisions.
8. Render through deterministic code over the approved DOCX. The LLM writes structured state and the compositor only maps it into authorized slots.

## Output contract

The structured result is the proposal state described in [state schema](references/state-schema.md), checked against [global rules](references/global-rules.md) by `scripts/validate_attempt.py`. Client-facing language follows `references/lexicon.json`.

The proposal must not describe excluded products. Optional products must be separated from the recommended solution and state the condition that would justify their inclusion.
