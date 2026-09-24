# Notas da execução — Solaris Energia (caso-07)

- Resultado: proposta emitida na 3ª submissão (execucao/final/POP-SOLARIS-2026-09.docx).
- Produtos recomendados: App & API Protector (REQ-01), Bot Manager Premier (REQ-02) e Global Traffic Management (REQ-03). Todos os outros produtos do catálogo foram excluídos: o DNS fica fora do escopo, não houve ataque volumétrico, não há upload nem meta de latência, e o caso não tem conta autenticada.
- Engajamento em fases: a Fase 1 (assessment e desenho, 3 a 4 semanas) é contratada e não muda nada em produção. A Fase 2 (implantação, 6 a 8 semanas) é opcional e depende do aceite do desenho.
- Garantia (90 dias após o aceite de cada fase), revenda das licenças, estimativas e prazo de licenças (até 2 semanas): todos têm aprovação escrita nos e-mails de 24/09/2026.
- Aplicação do SLA: Vitor aprovou em e-mail que a tabela institucional vale só na Fase 2. Registrei a aprovação com o valor ["phased"]; a restrição de que a Fase 1 não tem SLA ficou no texto. Convém revisar se o compositor restringe a tabela à Fase 2 no DOCX.
- Campanha de 01/03/2027: prazo classificado como "fits". A Fase 1 termina entre 15/10 e 22/10/2026 e, no cenário mais longo, tudo termina em 31/12/2026. Isso depende do aceite rápido do desenho e da assinatura do pedido.
- Pendências do cliente: volume base de tráfego e pico da campanha; inventário de hostnames e APIs; tempo aceitável de failover e critérios de saúde; capacidade da nuvem pública para o pico.
- Fora do escopo: a resposta da aplicação que expõe nome e endereço por CPF. A Solaris corrige isso com o DPO; é um risco residual declarado.
