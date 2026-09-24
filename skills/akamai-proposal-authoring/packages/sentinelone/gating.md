# SentinelOne package — solution gating

| Product | Include when | Do not infer from |
|---|---|---|
| Singularity Complete | endpoints or servers need antivirus replacement, EDR, automated response, device control or host firewall | generic "security" language without endpoints in scope |
| Singularity Ranger | the client asks for network inventory or discovery of unmanaged devices | an existing asset inventory that the client did not question |
| Singularity Mobile | corporate mobile devices must be protected | mobile devices mentioned only as access to e-mail |
| Purple AI | the client wants AI-assisted investigation or has a small team that must investigate alerts | a demo shown by POPULOS without a client requirement |
| Singularity Hyperautomation | the client asks for automated response workflows or integration with other tools | a demo shown by POPULOS without a client requirement |

A comparison the client requested between vendors (e.g. SentinelOne × Fortinet) keeps one as `recommended` and the other as `optional` with the trigger "if the client prefers …", never both as recommended.
