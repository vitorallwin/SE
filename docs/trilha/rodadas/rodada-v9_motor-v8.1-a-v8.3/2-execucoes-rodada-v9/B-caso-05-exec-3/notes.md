# Notas — Hospital São Lucas do Vale (caso-05)

- Resultado: BLOQUEADO pelo gate `sem_catalogo` (resultado correto). Nenhuma proposta emitida.
- Motivo: o pedido é assessment/desenho/estimativa de desktops virtuais Citrix (~1.100 estações, thin clients,
  prontuário eletrônico). O catálogo fornecido cobre apenas produtos Akamai de borda (DNS, GTM, ALB, WAF, DDoS, bots etc.);
  nenhum cobre VDI/Citrix. Produtos do catálogo não foram adaptados ao pedido.
- Insumo: suficiente (cliente e necessidade concreta identificados; REQ-01 a REQ-05 com fonte no e-mail de 21/09/2026).
- engagement_type `phased` tem aprovação registrada (Vitor, 24/09/2026), mas não foi usado, pois não há produto aplicável.
- Pendente (POPULOS): existe pacote do fabricante/oferta Citrix aprovada para compor esta proposta?
- Pendente (cliente): há publicação web, APIs públicas ou acesso externo ao prontuário que justifique avaliar o catálogo Akamai?
- Não decididos (irrelevantes enquanto houver bloqueio): garantia, modelo de fornecimento de licenças, aplicabilidade do SLA.
- Submissões: 2 de 3.
