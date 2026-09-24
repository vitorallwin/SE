# Relatório de cobertura — Lumina Seguros (LUMINA-BOT-2026)

- Regras: v11
- Modo dos dados: test
- Engajamento: implementation

## Decisões

| Decisão | Valor | Aprovado por | Data | Modo |
|---|---|---|---|---|
| engagement_type | implementation | Vitor | 2026-09-24 | test |
| warranty | a POPULOS corrigirá defeitos diretamente atribuíveis aos serviços executados por 90 dias corridos após o aceite final. | Vitor | 2026-09-24 | test |
| license_supply | a licença do Bot Manager será adicionada ao contrato direto entre a Lumina e a Akamai, por aditivo, com co-terminação em 31/03/2027. A POPULOS presta apenas os serviços. | Vitor | 2026-09-24 | test |
| sla | Tabela institucional de SLA POPULOS (ALTA, MÉDIA, BAIXA) | None | None | None |
| effort_estimate | 4 a 5 semanas | Ana Ribeiro | 2026-09-24 | test |

## Cobertura do insumo

| Referência | Trecho | Status | Destino |
|---|---|---|---|
| registro interno POPULOS (contexto da conta) | Cliente POPULOS desde 2024 | coberto | sumário |
| registro interno POPULOS (contexto da conta) | Produtos contratados: Ion, App & API Protector e Edge DNS | coberto | sumário, escopo |
| registro interno POPULOS (contexto da conta) | Contrato Akamai firmado diretamente entre a Lumina e a Akamai; POPULOS presta implantação e suporte | coberto | premissas, engajamento |
| registro interno POPULOS (contexto da conta) | Vigência do contrato Akamai atual até 31/03/2027 | coberto | premissas |
| registro interno POPULOS (contexto da conta) | Propriedades Ion em produção: www, cotacao e api | coberto | dimensionamento |
| registro interno POPULOS (contexto da conta) | Sustentação POPULOS 8x5 até 31/03/2027 | coberto | exclusões |
| transcrição 23/09/2026 — Camila Reis | Simulador de cotação raspado por robôs, milhares de cotações por hora | coberto | REQ-01, sumário |
| transcrição 23/09/2026 — Camila Reis | Aumento de custo com consultas aos bureaus a cada cotação | coberto | REQ-02, sumário |
| transcrição 23/09/2026 — Diego Martins | WAF atual não pega os robôs; querem o Bot Manager | coberto | REQ-01 |
| transcrição 23/09/2026 — Camila Reis | Logins suspeitos na área do cliente, não confirmados | pendente | premissas |
| transcrição 23/09/2026 — Diego Martins | Lançamento do novo seguro auto em 15/01/2027 com campanha de mídia | coberto | REQ-03 |
| transcrição 23/09/2026 — Diego Martins | Congelamento de fim de ano de 15/12/2026 a 05/01/2027 | coberto | REQ-03 |
| transcrição 23/09/2026 — Camila Reis | Dois bureaus por cotação, cerca de 2,1 milhões de cotações no mês passado, ao menos metade de robôs | coberto | REQ-02, dimensionamento, sumário |
| e-mail de Vitor (Executivo de Contas, POPULOS) de 24/09/2026 09:40 | Engajamento de implantação e garantia de 90 dias aprovados | coberto | engajamento |
| e-mail de Ana Ribeiro (Arquiteta, POPULOS) de 24/09/2026 10:15 | Estimativa de esforço de 4 a 5 semanas | coberto | dimensionamento |
| e-mail de Vitor (Executivo de Contas, POPULOS) de 24/09/2026 16:20 | Licença por aditivo ao contrato direto, provisionamento em até 10 dias úteis | coberto | premissas |

## Requisitos

| REQ | Requisito | Origem | Evidência no insumo | Falantes |
|---|---|---|---|---|
| REQ-01 | Detectar e mitigar robôs que raspam o simulador de cotação e se passam por navegador comum | transcrição 23/09/2026 — Camila Reis e Diego Martins | Milhares de cotações por hora vindas de robôs; o WAF atual não identifica esses robôs | client |
| REQ-02 | Reduzir as cotações automatizadas que geram consultas pagas aos bureaus de dados | transcrição 23/09/2026 — Camila Reis | Cada cotação consulta dois bureaus, pagos por consulta; estimativa da Lumina de ao menos metade das cotações vindas de robôs | client |
| REQ-03 | Bot Manager Premier em operação antes de 15/01/2027, fora do congelamento de 15/12/2026 a 05/01/2027 | transcrição 23/09/2026 — Diego Martins | Lançamento do novo seguro auto com campanha de mídia | client |

## Números do cliente

- transcrição 23/09/2026 — Camila Reis: milhares de cotações por hora → contexto_de_dor
- transcrição 23/09/2026 — Camila Reis: Cada cotação consulta dois bureaus → contexto_de_dor
- transcrição 23/09/2026 — Camila Reis: cerca de 2,1 milhões de cotações → dimensionamento
- transcrição 23/09/2026 — Camila Reis: pelo menos metade seja de robôs → contexto_de_dor
- transcrição 23/09/2026 — Diego Martins: 15/01/2027 → meta
- transcrição 23/09/2026 — Diego Martins: 15/12/2026 a 05/01/2027 → dimensionamento

## Perguntas abertas

- Em que data a Lumina prevê assinar o aditivo do Bot Manager Premier com a Akamai? O provisionamento leva até 10 dias úteis após a assinatura.
- Quais hosts e caminhos compõem o simulador de cotação de seguro auto a proteger?
- Os logins suspeitos na área do cliente foram confirmados? Há registros de tentativas, contas afetadas ou recuperação de senha envolvidas?
- Existem robôs legítimos (parceiros, comparadores contratados, monitoramento) que precisem ser permitidos no simulador?
