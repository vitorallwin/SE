# Relatório de cobertura — Lumina Seguros (LUMINA-BOT-2026-09)

- Regras: v10
- Modo dos dados: test
- Engajamento: implementation

## Decisões

| Decisão | Valor | Aprovado por | Data | Modo |
|---|---|---|---|---|
| engagement_type | implementation | Vitor (Executivo de Contas, POPULOS) | 2026-09-24 | test |
| warranty | A POPULOS corrigirá defeitos diretamente atribuíveis aos serviços executados por 90 dias corridos após o aceite final. | Vitor (Executivo de Contas, POPULOS) | 2026-09-24 | test |
| license_supply | a licença do Bot Manager será adicionada ao contrato direto entre a Lumina e a Akamai, por aditivo, com co-terminação em 31/03/2027. A POPULOS presta apenas os serviços. | Vitor (Executivo de Contas, POPULOS) | 2026-09-24 | test |
| sla | Tabela de SLA institucional do template POPULOS aprovado | None | None | None |
| effort_estimate | 4 a 5 semanas | Ana Ribeiro (Arquiteta, POPULOS) | 2026-09-24 | test |

## Cobertura do insumo

| Referência | Trecho | Status | Destino |
|---|---|---|---|
| registro interno POPULOS: contexto da conta | Cliente POPULOS desde 2024, com Ion, App & API Protector e Edge DNS contratados diretamente com a Akamai até 31/03/2027. | coberto | sumário, engajamento |
| registro interno POPULOS: propriedades Ion | Propriedades Ion em produção: www.lumina.com.br, cotacao.lumina.com.br, api.lumina.com.br. | coberto | dimensionamento, premissas |
| registro interno POPULOS: suporte | Contrato de sustentação 8x5 da POPULOS vigente até 31/03/2027. | coberto | exclusões |
| transcrição 23/09/2026 (Camila Reis) | O simulador de cotação de seguro auto está sendo raspado por robôs que copiam a tabela de preços. | coberto | REQ-01, sumário |
| transcrição 23/09/2026 (Camila Reis) | A raspagem aumenta o custo com consultas a bureaus de dados. | coberto | REQ-03, sumário |
| transcrição 23/09/2026 (Diego Martins) | O WAF atual pega ataque, mas não pega esses robôs, que parecem navegador normal. | coberto | REQ-01 |
| transcrição 23/09/2026 (Diego Martins) | Queremos o Bot Manager. | coberto | REQ-01, escopo |
| transcrição 23/09/2026 (Camila Reis) | Logins suspeitos na área do cliente, nada confirmado ainda. | pendente | premissas |
| transcrição 23/09/2026 (Diego Martins) | Lançamento do novo seguro auto em 15/01/2027 com campanha de mídia forte; Bot Manager funcionando antes disso. | coberto | REQ-02, sumário |
| transcrição 23/09/2026 (Diego Martins) | Congelamento de fim de ano de 15/12/2026 a 05/01/2027. | coberto | REQ-02, premissas |
| transcrição 23/09/2026 (Camila Reis) | Cada cotação consulta dois bureaus, pagos por consulta; cerca de 2,1 milhões de cotações no mês passado, pelo menos metade de robôs. | coberto | REQ-03, dimensionamento, sumário |
| e-mails de aprovação interna POPULOS de 24/09/2026 | Engajamento de implantação, garantia de 90 dias, estimativa de 4 a 5 semanas e licenciamento direto por aditivo com provisionamento em até 10 dias úteis. | coberto | engajamento, escopo, premissas |

## Requisitos

| REQ | Requisito | Origem | Evidência no insumo | Falantes |
|---|---|---|---|---|
| REQ-01 | Detectar e mitigar robôs que imitam navegadores e raspam o simulador de cotação de seguro auto. | transcrição 23/09/2026 (Camila Reis; Diego Martins) | Milhares de cotações por hora vindas de robôs; o WAF atual não identifica esses robôs. | client |
| REQ-02 | Colocar a proteção contra robôs em produção antes de 15/01/2027, respeitando o congelamento de 15/12/2026 a 05/01/2027. | transcrição 23/09/2026 (Diego Martins) | Lançamento do novo seguro auto em 15/01/2027 com campanha de mídia; congelamento de 15/12/2026 a 05/01/2027. | client |
| REQ-03 | Dar visibilidade do volume de cotações automatizadas para apoiar a análise de custo com consultas a bureaus. | transcrição 23/09/2026 (Camila Reis) | Cada cotação consulta dois bureaus pagos por consulta; cerca de 2,1 milhões de cotações no mês, com estimativa de pelo menos metade de robôs. | client |

## Números do cliente

- transcrição 23/09/2026 (Camila Reis): milhares de cotações por hora vindas de robôs → contexto_de_dor
- transcrição 23/09/2026 (Camila Reis): Cada cotação consulta dois bureaus → contexto_de_dor
- transcrição 23/09/2026 (Camila Reis): cerca de 2,1 milhões de cotações → dimensionamento
- transcrição 23/09/2026 (Camila Reis): pelo menos metade seja de robôs → contexto_de_dor
- transcrição 23/09/2026 (Diego Martins): lançando o novo seguro auto em 15/01/2027 → meta
- transcrição 23/09/2026 (Diego Martins): congelamento de fim de ano vai de 15/12/2026 a 05/01/2027 → meta

## Perguntas abertas

- Quais hosts e endpoints compõem o fluxo do simulador de cotação de seguro auto (por exemplo, cotacao.lumina.com.br e chamadas em api.lumina.com.br)?
- Qual a data prevista para assinatura do aditivo de licenciamento do Bot Manager Premier com a Akamai?
- Os logins suspeitos na área do cliente foram confirmados? Há volume, período ou evidência que justifique avaliar o Account Protector?
