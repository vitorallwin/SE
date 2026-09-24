# Relatório de cobertura — Lumina Seguros (LUMINA-BOT-2026-09)

- Regras: v11
- Modo dos dados: test
- Engajamento: implementation

## Decisões

| Decisão | Valor | Aprovado por | Data | Modo |
|---|---|---|---|---|
| engagement_type | implementation | Vitor (Executivo de Contas, POPULOS) | 2026-09-24 | test |
| warranty | A POPULOS corrigirá defeitos diretamente atribuíveis aos serviços executados por 90 dias corridos após o aceite final. | Vitor (Executivo de Contas, POPULOS) | 2026-09-24 | test |
| license_supply | A licença do Bot Manager será adicionada ao contrato direto entre a Lumina e a Akamai, por aditivo, com co-terminação em 31/03/2027. A POPULOS presta apenas os serviços. | Vitor (Executivo de Contas, POPULOS) | 2026-09-24 | test |
| effort_estimate | 4 a 5 semanas | Ana Ribeiro (Arquiteta, POPULOS) | 2026-09-24 | test |
| sla | Tabela institucional de SLA POPULOS (ALTA, MÉDIA, BAIXA) | None | None | None |

## Cobertura do insumo

| Referência | Trecho | Status | Destino |
|---|---|---|---|
| Contexto da conta, item 1 | Cliente POPULOS desde 2024 | descartado | Informação de relacionamento sem efeito sobre escopo ou solução |
| Contexto da conta, item 2 | Produtos Akamai contratados: Ion, App & API Protector e Edge DNS | coberto | sumário, exclusões |
| Contexto da conta, item 3 | Contrato Akamai firmado diretamente entre Lumina e Akamai; POPULOS presta implantação e suporte | coberto | premissas, engajamento |
| Contexto da conta, item 4 | Vigência do contrato Akamai até 31/03/2027 | coberto | premissas |
| Contexto da conta, item 5 | Propriedades Ion em produção: www, cotacao e api | coberto | dimensionamento, escopo |
| Contexto da conta, item 6 | Contrato de sustentação 8x5 até 31/03/2027 | coberto | exclusões |
| Transcrição 23/09/2026, Camila Reis (fala 1) | Simulador de cotação raspado por robôs, aumentando custo com bureaus | coberto | REQ-01, REQ-03, sumário |
| Transcrição 23/09/2026, Diego Martins (fala 1) | WAF atual não pega os robôs; querem o Bot Manager | coberto | REQ-01, sumário |
| Transcrição 23/09/2026, Camila Reis (fala 2) | Logins suspeitos na área do cliente, nada confirmado | pendente | REQ-04 |
| Transcrição 23/09/2026, Diego Martins (fala 3) | Lançamento em 15/01/2027 e congelamento de 15/12/2026 a 05/01/2027 | coberto | REQ-02, sumário |
| Transcrição 23/09/2026, Camila Reis (fala 3) | Dois bureaus por cotação, 2,1 milhões de cotações no mês, metade estimada de robôs | coberto | REQ-03, dimensionamento, sumário |
| E-mail Vitor 24/09/2026 09:40 | Engajamento de implantação e garantia de 90 dias aprovados | coberto | engajamento |
| E-mail Ana Ribeiro 24/09/2026 10:15 | Estimativa de esforço de 4 a 5 semanas | coberto | dimensionamento |
| E-mail Vitor 24/09/2026 16:20 | Licença por aditivo ao contrato direto Lumina-Akamai; provisionamento em até 10 dias úteis | coberto | premissas, engajamento |

## Requisitos

| REQ | Requisito | Origem | Evidência no insumo | Falantes |
|---|---|---|---|---|
| REQ-01 | Detectar e mitigar robôs que imitam navegador e raspam o simulador de cotação de seguro auto | Transcrição 23/09/2026, Camila Reis (fala 1) e Diego Martins (fala 1) | Milhares de cotações por hora vindas de robôs que copiam a tabela de preços; o WAF atual não identifica esses robôs | client |
| REQ-02 | Bot Manager Premier em produção antes do lançamento de 15/01/2027, fora do congelamento de 15/12/2026 a 05/01/2027 | Transcrição 23/09/2026, Diego Martins (fala 3) | Lançamento com campanha de mídia forte e congelamento de fim de ano informados pelo cliente | client |
| REQ-03 | Dar visibilidade e reduzir as cotações automatizadas que geram consultas pagas a dois bureaus de dados | Transcrição 23/09/2026, Camila Reis (falas 1 e 3) | Cada cotação consulta dois bureaus pagos por consulta; cerca de 2,1 milhões de cotações no mês anterior, com estimativa do cliente de pelo menos metade vinda de robôs | client |
| REQ-04 | Avaliar os logins suspeitos na área do cliente | Transcrição 23/09/2026, Camila Reis (fala 2) | Logins suspeitos observados, sem confirmação | client |

## Números do cliente

- Transcrição 23/09/2026, Camila Reis (fala 1): milhares de cotações por hora → contexto_de_dor
- Transcrição 23/09/2026, Camila Reis (fala 3): Cada cotação consulta dois bureaus → contexto_de_dor
- Transcrição 23/09/2026, Camila Reis (fala 3): cerca de 2,1 milhões de cotações → dimensionamento
- Transcrição 23/09/2026, Camila Reis (fala 3): pelo menos metade seja de robôs → contexto_de_dor
- Transcrição 23/09/2026, Diego Martins (fala 3): 15/01/2027 → meta
- Transcrição 23/09/2026, Diego Martins (fala 3): 15/12/2026 a 05/01/2027 → dimensionamento

## Perguntas abertas

- Quais hostnames e caminhos compõem o simulador de cotação de seguro auto (por exemplo, cotacao.lumina.com.br e chamadas em api.lumina.com.br) e devem entrar na política do Bot Manager Premier?
- Qual a data prevista para a assinatura do aditivo de licença do Bot Manager Premier entre a Lumina e a Akamai?
- A Lumina confirma abuso nos logins suspeitos da área do cliente? Há volume, período e evidências para avaliar o Account Protector?
- Existem comparadores ou parceiros legítimos que consultam o simulador e devem ser tratados como automação permitida?
