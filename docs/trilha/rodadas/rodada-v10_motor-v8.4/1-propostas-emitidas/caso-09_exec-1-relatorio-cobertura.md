# Relatório de cobertura — Lumina Seguros (PROP-LUMINA-BOTMANAGER-2026)

- Regras: v10
- Modo dos dados: test
- Engajamento: implementation

## Decisões

| Decisão | Valor | Aprovado por | Data | Modo |
|---|---|---|---|---|
| engagement_type | implementation | Vitor (Executivo de Contas, POPULOS) | 2026-09-24 | test |
| warranty | a POPULOS corrigirá defeitos diretamente atribuíveis aos serviços executados por 90 dias corridos após o aceite final | Vitor (Executivo de Contas, POPULOS) | 2026-09-24 | test |
| license_supply | a licença do Bot Manager será adicionada ao contrato direto entre a Lumina e a Akamai, por aditivo, com co-terminação em 31/03/2027 | Vitor (Executivo de Contas, POPULOS) | 2026-09-24 | test |
| sla | Tabela institucional de níveis de serviço do template POPULOS aprovado | None | None | None |
| effort_estimate | 4 a 5 semanas | Ana Ribeiro (Arquiteta, POPULOS) | 2026-09-24 | test |

## Cobertura do insumo

| Referência | Trecho | Status | Destino |
|---|---|---|---|
| registro interno - cliente desde 2024 | Cliente POPULOS desde 2024 | coberto | sumário |
| registro interno - produtos contratados | Produtos Akamai contratados hoje: Ion, App & API Protector e Edge DNS | coberto | sumário, escopo |
| registro interno - modelo contratual | Contrato Akamai atual firmado diretamente entre a Lumina e a Akamai; a POPULOS presta implantação e suporte | coberto | premissas, engajamento |
| registro interno - vigência | Vigência do contrato Akamai atual até 31/03/2027 | coberto | premissas |
| registro interno - propriedades Ion | Propriedades Ion em produção: www.lumina.com.br, cotacao.lumina.com.br, api.lumina.com.br | coberto | dimensionamento |
| registro interno - suporte | Contrato de sustentação POPULOS 8x5 até 31/03/2027 | coberto | escopo, premissas |
| transcrição 23/09/2026, Camila Reis, fala 1 | Simulador de cotação de seguro auto raspado por robôs, milhares de cotações por hora, aumento de custo com bureaus | coberto | REQ-01, sumário |
| transcrição 23/09/2026, Diego Martins, fala 1 | O WAF atual não pega os robôs; querem o Bot Manager | coberto | REQ-02 |
| transcrição 23/09/2026, Camila Reis, fala 2 | Logins suspeitos na área do cliente, nada confirmado | pendente | REQ-04 |
| transcrição 23/09/2026, Diego Martins, fala 2 | Lançamento do novo seguro auto em 15/01/2027 e congelamento de 15/12/2026 a 05/01/2027 | coberto | REQ-03, sumário |
| transcrição 23/09/2026, Camila Reis, fala 3 | Dois bureaus por cotação, cerca de 2,1 milhões de cotações no mês passado, ao menos metade de robôs | coberto | sumário, dimensionamento |
| e-mail Vitor 24/09/2026 09:40 | Aprovação de engajamento de implantação e garantia de 90 dias | coberto | engajamento |
| e-mail Ana Ribeiro 24/09/2026 10:15 | Aprovação da estimativa de esforço de 4 a 5 semanas | coberto | dimensionamento |
| e-mail Vitor 24/09/2026 16:20 | Licença do Bot Manager por aditivo ao contrato direto Lumina-Akamai, co-terminação 31/03/2027, provisionamento em até 10 dias úteis após a assinatura | coberto | premissas, sumário |

## Requisitos

| REQ | Requisito | Origem | Evidência no insumo | Falantes |
|---|---|---|---|---|
| REQ-01 | Detectar e mitigar robôs que realizam cotações em massa no simulador de cotação de seguro auto para copiar a tabela de preços | transcrição 23/09/2026, Camila Reis, fala 1 | Milhares de cotações por hora vindas de robôs que copiam a tabela de preços e elevam o custo com consultas aos bureaus de dados | client |
| REQ-02 | Identificar automação que se apresenta como navegador legítimo e que o WAF atual não detecta | transcrição 23/09/2026, Diego Martins, fala 1 | O WAF atual pega ataque, mas não pega esses robôs, que parecem navegador normal | client |
| REQ-03 | Bot Manager Premier em funcionamento antes do lançamento do novo seguro auto em 15/01/2027, sem mudanças durante o congelamento de 15/12/2026 a 05/01/2027 | transcrição 23/09/2026, Diego Martins, fala 2 | Lançamento em 15/01/2027 com campanha de mídia forte; congelamento de 15/12/2026 a 05/01/2027 | client |
| REQ-04 | Avaliar logins suspeitos na área do cliente, ainda não confirmados | transcrição 23/09/2026, Camila Reis, fala 2 | Alguns logins suspeitos na área do cliente, nada confirmado ainda | client |

## Números do cliente

- transcrição 23/09/2026, Camila Reis, fala 1: milhares de cotações por hora vindas de robôs → contexto_de_dor
- transcrição 23/09/2026, Camila Reis, fala 3: Cada cotação consulta dois bureaus → contexto_de_dor
- transcrição 23/09/2026, Camila Reis, fala 3: No mês passado foram cerca de 2,1 milhões de cotações → dimensionamento
- transcrição 23/09/2026, Camila Reis, fala 3: estimamos que pelo menos metade seja de robôs → contexto_de_dor
- transcrição 23/09/2026, Diego Martins, fala 2: Estamos lançando o novo seguro auto em 15/01/2027 → meta
- transcrição 23/09/2026, Diego Martins, fala 2: Nosso congelamento de fim de ano vai de 15/12/2026 a 05/01/2027 → meta

## Perguntas abertas

- Quais rotas e endpoints do simulador de cotação (cotacao.lumina.com.br e api.lumina.com.br) devem ser protegidos, e há aplicativo móvel consumindo a mesma API?
- Qual a data prevista para a assinatura do aditivo de licença do Bot Manager entre a Lumina e a Akamai?
- Os logins suspeitos na área do cliente foram confirmados como abuso de conta? Com que volume e em qual jornada (login, recuperação ou pós-login)?
- Há comparadores ou parceiros autorizados que consultam o simulador e devem ser tratados como automação permitida?
