# Relatório de cobertura — Lumina Seguros (LUMINA-BOT-2026)

- Regras: v10
- Modo dos dados: test
- Engajamento: implementation

## Decisões

| Decisão | Valor | Aprovado por | Data | Modo |
|---|---|---|---|---|
| engagement_type | implementation | Vitor (Executivo de Contas, POPULOS) | 2026-09-24 | test |
| warranty | A POPULOS corrigirá defeitos diretamente atribuíveis aos serviços executados por 90 dias corridos após o aceite final. | Vitor (Executivo de Contas, POPULOS) | 2026-09-24 | test |
| license_supply | A licença do Bot Manager será adicionada ao contrato direto entre a Lumina e a Akamai, por aditivo, com co-terminação em 31/03/2027. A POPULOS presta apenas os serviços. | Vitor (Executivo de Contas, POPULOS) | 2026-09-24 | test |
| effort_estimate | 4 a 5 semanas | Ana Ribeiro (Arquiteta, POPULOS) | 2026-09-24 | test |
| sla | Tabela de SLA institucional do template neutro POPULOS aprovado | None | None | None |

## Cobertura do insumo

| Referência | Trecho | Status | Destino |
|---|---|---|---|
| material.md — Contexto da conta, item 1 | Cliente POPULOS desde 2024. | coberto | sumário |
| material.md — Contexto da conta, item 2 | Produtos Akamai contratados hoje: Ion, App & API Protector e Edge DNS. | coberto | sumário, escopo |
| material.md — Contexto da conta, item 3 | Contrato Akamai atual firmado diretamente entre a Lumina e a Akamai; a POPULOS presta implantação e suporte. | coberto | premissas |
| material.md — Contexto da conta, item 4 | Vigência do contrato Akamai atual até 31/03/2027. | coberto | premissas |
| material.md — Contexto da conta, item 5 | Propriedades Ion em produção: www.lumina.com.br, cotacao.lumina.com.br, api.lumina.com.br. | coberto | dimensionamento |
| material.md — Contexto da conta, item 6 | Suporte POPULOS em vigor: sustentação 8x5 até 31/03/2027. | coberto | exclusões |
| transcrição 23/09/2026 — Camila Reis (1) | Simulador de cotação raspado por robôs, milhares de cotações por hora, cópia da tabela de preços. | coberto | REQ-01 |
| transcrição 23/09/2026 — Camila Reis (1) | Aumento de custo com consultas aos bureaus a cada cotação. | coberto | REQ-02 |
| transcrição 23/09/2026 — Diego Martins (1) | O WAF atual não identifica os robôs, que parecem navegador normal; a Lumina quer o Bot Manager. | coberto | REQ-01 |
| transcrição 23/09/2026 — Camila Reis (2) | Logins suspeitos na área do cliente, nada confirmado. | pendente | REQ-04 |
| transcrição 23/09/2026 — Diego Martins (2) | Lançamento do novo seguro auto em 15/01/2027 com campanha de mídia; Bot Manager funcionando antes disso; congelamento de 15/12/2026 a 05/01/2027. | coberto | REQ-03 |
| transcrição 23/09/2026 — Camila Reis (3) | Cada cotação consulta dois bureaus pagos por consulta; cerca de 2,1 milhões de cotações no mês passado; pelo menos metade estimada como robôs. | coberto | REQ-02, dimensionamento |
| e-mail Vitor 24/09/2026 09:40 | Engajamento de implantação e garantia de 90 dias corridos após o aceite final aprovados. | coberto | engajamento, escopo |
| e-mail Ana Ribeiro 24/09/2026 10:15 | Estimativa de esforço de 4 a 5 semanas aprovada. | coberto | dimensionamento |
| e-mail Vitor 24/09/2026 16:20 | Licença do Bot Manager por aditivo ao contrato direto Lumina–Akamai, co-terminação em 31/03/2027; provisionamento em até 10 dias úteis após a assinatura. | coberto | premissas |

## Requisitos

| REQ | Requisito | Origem | Evidência no insumo | Falantes |
|---|---|---|---|---|
| REQ-01 | Detectar e mitigar robôs que raspam o simulador de cotação de seguro auto e se apresentam como navegador comum. | transcrição 23/09/2026 — Camila Reis e Diego Martins | Milhares de cotações por hora vindas de robôs que copiam a tabela de preços; o WAF atual não identifica esses robôs. | client |
| REQ-02 | Reduzir as cotações automatizadas que disparam consultas pagas a dois bureaus de dados por cotação. | transcrição 23/09/2026 — Camila Reis | Cerca de 2,1 milhões de cotações no mês anterior, com estimativa da Lumina de pelo menos metade automatizada; cada cotação consulta dois bureaus pagos por consulta. | client |
| REQ-03 | Ter a proteção contra automação em produção antes do lançamento do novo seguro auto em 15/01/2027, respeitando o congelamento de 15/12/2026 a 05/01/2027. | transcrição 23/09/2026 — Diego Martins | Lançamento com campanha de mídia forte em 15/01/2027 e congelamento de fim de ano informado pela Lumina. | client |
| REQ-04 | Avaliar logins suspeitos na área do cliente, ainda não confirmados. | transcrição 23/09/2026 — Camila Reis | Relato de logins suspeitos na área do cliente, sem confirmação. | client |

## Números do cliente

- transcrição 23/09/2026 — Camila Reis (1): milhares de cotações por hora vindas de robôs → contexto_de_dor
- transcrição 23/09/2026 — Camila Reis (3): No mês passado foram cerca de 2,1 milhões de cotações → contexto_de_dor
- transcrição 23/09/2026 — Camila Reis (3): estimamos que pelo menos metade seja de robôs → contexto_de_dor
- transcrição 23/09/2026 — Camila Reis (3): Cada cotação consulta dois bureaus → contexto_de_dor
- transcrição 23/09/2026 — Diego Martins (2): Estamos lançando o novo seguro auto em 15/01/2027 → meta
- transcrição 23/09/2026 — Diego Martins (2): Nosso congelamento de fim de ano vai de 15/12/2026 a 05/01/2027 → meta

## Perguntas abertas

- Quais endpoints e fluxos do simulador de cotação (host, caminhos e chamadas de API) devem ser protegidos?
- Qual a data prevista para assinatura do aditivo de licença do Bot Manager Premier com a Akamai?
- A Lumina confirmará se há abuso de login na área do cliente, para avaliar a necessidade do Account Protector?
- O Bot Manager Premier passará a integrar o contrato de sustentação 8x5 vigente após o aceite?
