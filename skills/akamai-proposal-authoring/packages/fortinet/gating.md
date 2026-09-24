# Fortinet package — solution gating

| Product | Include when | Do not infer from |
|---|---|---|
| FortiEDR | endpoints or servers need EDR with automated response, especially in a Fortinet Security Fabric environment | the mere presence of FortiGate firewalls |
| FortiClient com EMS | endpoints need centrally managed protection, web filtering, vulnerability management or a VPN/ZTNA agent | remote access alone, when the client did not ask for endpoint protection |

Firewall support (FortiGate) is a POPULOS service (`populos_services`), not a Fortinet license in this package.
