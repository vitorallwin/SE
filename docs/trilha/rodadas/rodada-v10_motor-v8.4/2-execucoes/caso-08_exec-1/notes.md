# Notas — Pregão 112/2026, Rio Claro do Sul (caso-08)

- Status: BLOQUEADO (2 submissões; única violação restante: `decisão interna aberta: sla_severity_levels`).
- Motivo do bloqueio: os itens 7.2 e 7.3 do TR exigem prazos por severidade (alta: resposta 1 h / resolução 4 h; média: 2 h / 8 h).
  O material aprova apenas o regime 8x5 por 12 meses (item 7.1). Não há aprovação POPULOS desses prazos nem confirmação de que
  a tabela institucional de SLA os atende. Por isso a decisão ficou como `populos_internal_decision` e não foi forçada.
- Para destravar: a POPULOS (Executivo de Contas) precisa aprovar por escrito os prazos dos itens 7.2/7.3 (ou declarar que a
  tabela institucional os atende), com aprovador, data e registro.
- Resolvido com aprovação registrada: engajamento (implementation), garantia de 12 meses após o TAD, licenças por revenda
  autorizada, suporte 8x5, qualificação (3 certificados Akamai) e estimativa de 5 a 6 semanas (Ana Ribeiro, arquiteta).
- Produtos recomendados: Edge DNS e App & API Protector. Todos os demais foram excluídos por falta de evidência (L7 apenas, sem uploads,
  sem múltiplas origens, sem caso de bots ou contas).
- Premissas a validar: formato syslog do coletor da SMTI, aceitação de tráfego da borda pelas origens, disponibilidade das janelas.
- Prazo: 5 a 6 semanas (até 42 dias), compatível com os 45 dias corridos do item 5.2.
