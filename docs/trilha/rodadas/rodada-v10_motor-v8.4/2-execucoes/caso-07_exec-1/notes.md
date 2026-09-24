# Notas da execução — Solaris Energia

- Resultado: emitido na 3ª submissão (final/POPULOS-SOLARIS-PORTAL-2026.docx).
- Recomendados: App & API Protector (DDoS L7), Bot Manager Premier (robôs de CPF), GTM (failover datacenter/nuvem). Os demais foram excluídos (Edge DNS: o DNS fica fora do escopo; Prolexic: não houve ataque volumétrico).
- Governança: engajamento em fases, revenda das licenças, garantia de 90 dias e estimativas (3-4 / 6-8 sem.), todos aprovados por e-mail em 24/09/2026.
- SLA: a tabela institucional não estava prevista para 'phased'. Registrei sla_applicability=["phased"] com base no e-mail de Vitor (09:20), que restringe o SLA à Fase 2. A restrição aparece nas premissas. A POPULOS deve confirmar essa leitura.
- Prazo: a Fase 1 termina entre 15/10 e 22/10/2026; a Fase 2 e as licenças precisam ser assinadas até 21/12/2026 para terminar antes de 01/03/2027.
- Pendências do cliente: volume de requisições (pico da campanha), inventário de hostnames/APIs, delegação por CNAME no provedor DNS atual.
- Risco residual: a consulta de débitos devolve nome e endereço. A correção cabe à aplicação (cliente/DPO) e está fora do escopo.
- Violações corrigidas: faixa de 6 a 8 semanas no texto ao cliente, mode ausente, citações sem o nome do aprovador, valor aprovado ausente da citação.
