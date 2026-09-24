# Solution gating

## Coverage dimensions

- Multi-cloud DNS continuity: prefer Global Traffic Management with Edge DNS; use Application Load Balancer as a complementary HTTP-edge origin-routing control when its request-level behavior is required.
- Application-layer DDoS and API threats: App & API Protector.
- Network and infrastructure DDoS: Prolexic, subject to routing, address-space, connectivity, and operating-model validation. Keep product recommendation separate from deployment modality (`Routed GRE`, `IP Protect`, or another approved model).
- Digital performance: Ion when a named web or mobile journey has a measurable experience or latency objective.
- Automated abuse: Bot Manager for automation; Account Protector when risk is tied to account creation, login, recovery, or post-login behavior.

Do not claim that one layer covers another. If a requirement spans layers, recommend the required controls or state the residual risk explicitly.

## Critical-event trigger

When discovery names a seasonal or business-critical peak such as Black Friday or Pix Day, require an event-readiness block with load testing, capacity review, change freeze, monitoring, rollback/degradation runbook, and a POPULOS-led war room. Akamai participation may be stated only when the contracted support tier and escalation plan authorize it.

Evaluate products against explicit evidence from the discovery.

| Product | Include when | Do not infer from |
|---|---|---|
| Edge DNS | authoritative DNS, DNS resilience, DNSSEC, zone management, apex mapping, or DNS attack resilience is in scope | the client merely owns a public domain |
| App and API Protector | public web applications or APIs require WAF, API security, adaptive protection, or application-layer DDoS mitigation | generic security improvement language |
| Bot Manager Premier | automated abuse such as credential stuffing, scraping, account creation, inventory abuse, or transaction automation is evidenced | ordinary malicious traffic without a bot use case |
| Malware Protection | files are uploaded and require inspection, blocking, or quarantine at the edge | the application only downloads static content |
| Global Traffic Management | multiple origins, DNS-level failover, health-based or performance-based routing between data centers or clouds | a single origin |
| Application Load Balancer | per-request routing between origins is required (path, header, cookie, session affinity) | multi-origin failover alone, which is the GTM trigger |
| Prolexic | volumetric L3/L4 DDoS or direct exposure of origins or IP ranges is evidenced | application-layer attacks alone |
| Ion | a named web journey has a latency, conversion, or experience objective | generic "performance" language |
| Account Protector | risk is tied to account creation, login, recovery, or post-login identity signals | automation that Bot Manager already addresses |
| IP Accelerator | non-cacheable TCP or UDP applications require route optimization, performance, or availability | ordinary HTTPS APIs that are already addressed by edge web delivery |

For each recommended product, require at least one matching requirement and a rationale specific to the client. Mark uncertain fits as `needs_information`. Keep `optional` decisions outside the base scope. Never rotate requirements across products merely to obtain complete catalog coverage.
