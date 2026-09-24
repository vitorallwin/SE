# Notas — Hospital São Lucas do Vale (caso-05)

Status: BLOQUEADO pelo gate `sem_catalogo` (resultado correto). 2 submissões.

- Insumo suficiente: cliente identificado e necessidade concreta (≈1.100 estações Windows 10 -> desktops virtuais Citrix, prontuário eletrônico, thin clients, 24x7, LGPD).
- Bloqueio: o pedido (VDI/Citrix, assessment + desenho + estimativa de implantação) não é coberto pelo catálogo fornecido (apenas produtos Akamai de borda). Nenhum produto foi forçado para o caso.
- Submissão 1: recusada por falta de requisitos rastreados do cliente; corrigido com REQ-01 a REQ-04 em `traceability`.
- Submissão 2: gate sem_catalogo — requer pacote do fabricante (Citrix/VDI).
- Pendente (POPULOS): decidir se há oferta aprovada de VDI/Citrix fora deste catálogo, ou declinar/encaminhar o caso.
- Pendente (cliente): informar se há componentes publicados na internet (portal Citrix, prontuário, APIs) que justifiquem proposta separada com o catálogo atual.
- A decisão engagement_type = phased (Vitor, 24/09/2026) foi registrada no insumo, mas não chegou a ser usada por causa do bloqueio.
