# Notas - Solaris Energia (caso-07)

- Status: emitido na 3a submissão (DOCX em final/SOLARIS-2026-AAP-GTM.docx).
- Recomendados: App & API Protector (REQ-01), Bot Manager Premier (REQ-02), Global Traffic Management (REQ-03). Os demais foram excluídos: Edge DNS (o DNS fica no provedor atual), ALB, Prolexic (sem ataque volumétrico), Account Protector, Ion, IP Accelerator, Malware Protection.
- Engajamento em fases: a Fase 1 (Assessment e desenho, 3 a 4 semanas) está contratada; a Fase 2 (implantação, 6 a 8 semanas, 2 ondas) é opcional.
- Aprovações usadas (e-mails de 24/09/2026): engajamento, revenda das licenças, garantia de 90 dias, estimativas (Ana Ribeiro) e prazo de 2 semanas para as licenças.
- SLA: no envio 2 o validador bloqueou sla_applicability, porque a tabela de SLA não está prevista para engajamentos 'phased'. Na correção, sla_applicability passou a ['phased'] com base na aprovação de Vitor de 24/09/2026 09:20. Essa aprovação limita a tabela à Fase 2; o texto do callout diz isso, mas o valor do campo não carrega esse limite. A POPULOS deve confirmar se é essa a leitura certa.
- Viabilidade da campanha de 01/03/2027 classificada como "fits": a Fase 1 termina entre 15/10 e 22/10/2026; no pior caso a Fase 2 termina em 31/12/2026, se for contratada logo após o aceite do desenho.
- Pendências do cliente: hostnames e APIs no escopo, volume habitual e de pico do tráfego, delegação de subdomínio no provedor DNS atual para o GTM.
- Privacidade: a exposição de CPF fica com o DPO da Solaris; não há integração que exporte dados (SIEM) no escopo.
