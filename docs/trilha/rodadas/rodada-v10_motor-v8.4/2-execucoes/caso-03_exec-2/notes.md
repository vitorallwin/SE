# Notas — Grupo Mariá Varejo (caso-03)

Status: BLOQUEADO na submissão 1/3 por decisões que só a POPULOS ou o cliente podem tomar. Não há violações de conteúdo.
Bloqueios:
- engagement_type: o material não define o tipo de engajamento. Há três leituras possíveis: implantação mínima para a Black Friday (pedido do CFO), tudo em modo bloqueio (pedido da CISO) ou faseado com o orçamento de 2027. Não foi inferido.
- sla_applicability: depende do engagement_type e fica aberto até ele ser definido.
- warranty e license_supply: o caso tem "Decisões internas POPULOS: Nenhuma".
Pendências do cliente, visíveis na proposta:
- Prazo de liberação das licenças e de compras. A viabilidade para a Black Friday é parcial: as licenças precisam estar ativas até 21/10 e as fases terminam entre 22/10 e 29/10, antes do congelamento de 01/11.
- Aceite de apontar os hostnames do e-commerce para a Akamai. Rodrigo prefere não mexer no DNS agora.
- Lista de hostnames e APIs; volume real (500 mil/dia ou 5 milhões/dia no pico); topologia dos 2 data centers.
- A pergunta sobre "100% de bloqueio de bot" foi tratada como premissa, sem promessa absoluta.
Solução: App & API Protector e Bot Manager Premier recomendados; Account Protector opcional (2027); Ion e GTM aguardam informação; demais excluídos.
