# Solution gating

The catalog is the union of the vendor packages in `packages/<id>/` (`package.json` holds the products; `gating.md` holds when to include each one). Choose products only from packages whose technology the client asked for. When the request needs a vendor with no package, use `catalog_fit` `no_catalog`: never map it onto unrelated products of another vendor.

- Evaluate every product of the packages involved against explicit evidence from the source material.
- For each recommended product, require at least one matching requirement and a rationale specific to the client.
- Mark uncertain fits as `needs_information`. Keep `optional` decisions (including a competing alternative the client asked to compare) outside the base scope, with an explicit trigger.
- Never rotate requirements across products merely to obtain complete catalog coverage.
- A package with `"status": "draft"` has not been validated by POPULOS: the engine emits it only with `data_mode` `test`.
- A product with `requires_decision` (e.g. `support_terms` for continuous services) is emitted only when that governance decision is a `commitment` approved in the source material: hours, coverage and response times of the service. Never reuse the institutional implementation SLA for it.

## Critical-event trigger

When discovery names a seasonal or business-critical peak such as Black Friday or Pix Day, require an event-readiness block proportional to the scope: change freeze, monitoring and rollback always; load testing, capacity review and a POPULOS-led war room only when a recommended product sits in the application traffic path. Akamai participation may be stated only when the contracted support tier and escalation plan authorize it.
