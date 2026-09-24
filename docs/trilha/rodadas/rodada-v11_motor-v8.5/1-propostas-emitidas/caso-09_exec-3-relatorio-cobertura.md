# Relatório de cobertura — Lumina Seguros (LUMINA-BOT-2026)

- Regras: v11
- Modo dos dados: test
- Engajamento: implementation

## Decisões

| Decisão | Valor | Aprovado por | Data | Modo |
|---|---|---|---|---|
| engagement_type | implementation | Vitor (Executivo de Contas, POPULOS) | 2026-09-24 | test |
| warranty | a POPULOS corrigirá defeitos diretamente atribuíveis aos serviços executados por 90 dias corridos após o aceite final | Vitor (Executivo de Contas, POPULOS) | 2026-09-24 | test |
| license_supply | a licença do Bot Manager será adicionada ao contrato direto entre a Lumina e a Akamai, por aditivo, com co-terminação em 31/03/2027. A POPULOS presta apenas os serviços. | Vitor (Executivo de Contas, POPULOS) | 2026-09-24 | test |
| effort_estimate | 4 a 5 semanas | Ana Ribeiro (Arquiteta, POPULOS) | 2026-09-24 | test |
| sla | Tabela institucional de SLA POPULOS (ALTA: resposta até 1 hora, solução até 4 horas; MÉDIA: resposta até 2 horas, solução até 8 horas; BAIXA: resposta até 16 horas, solução até 24 horas) | None | None | None |

## Cobertura do insumo

| Referência | Trecho | Status | Destino |
|---|---|---|---|
| registro interno — cliente desde 2024 | Cliente POPULOS desde 2024 | coberto | sumário |
| registro interno — produtos contratados | Produtos Akamai contratados hoje: Ion, App & API Protector e Edge DNS | coberto | sumário, escopo |
| registro interno — contrato direto | Contrato Akamai atual firmado diretamente entre a Lumina e a Akamai; POPULOS presta implantação e suporte | coberto | premissas |
| registro interno — vigência | Vigência do contrato Akamai atual até 31/03/2027 | coberto | premissas |
| registro interno — propriedades Ion | Propriedades Ion em produção: www.lumina.com.br, cotacao.lumina.com.br, api.lumina.com.br | coberto | dimensionamento |
| registro interno — sustentação | Suporte POPULOS em vigor: contrato de sustentação 8x5 até 31/03/2027 | coberto | exclusões |
| transcrição 23/09/2026 — Camila Reis (raspagem) | O simulador de cotação de seguro auto está sendo raspado por robôs que copiam a tabela de preços | coberto | REQ-01 |
| transcrição 23/09/2026 — Camila Reis (bureaus) | A raspagem aumenta o custo com consultas aos bureaus de dados | coberto | REQ-03 |
| transcrição 23/09/2026 — Diego Martins (WAF) | O WAF atual não detecta os robôs, que parecem navegador normal; o cliente quer o Bot Manager | coberto | REQ-02 |
| transcrição 23/09/2026 — Camila Reis (logins) | Logins suspeitos na área do cliente, nada confirmado | pendente | REQ-05 |
| transcrição 23/09/2026 — Diego Martins (lançamento) | Lançamento do novo seguro auto em 15/01/2027 com campanha de mídia; Bot Manager funcionando antes disso | coberto | REQ-04 |
| transcrição 23/09/2026 — Diego Martins (congelamento) | Congelamento de fim de ano de 15/12/2026 a 05/01/2027 | coberto | REQ-04 |
| transcrição 23/09/2026 — Camila Reis (volumes) | Cerca de 2,1 milhões de cotações no mês passado, pelo menos metade estimada como robôs; cada cotação consulta dois bureaus | coberto | dimensionamento, sumário |
| e-mail Vitor 24/09/2026 09:40 | Aprovação do engajamento de implantação e da garantia de 90 dias | coberto | engajamento |
| e-mail Ana Ribeiro 24/09/2026 10:15 | Aprovação da estimativa de esforço de 4 a 5 semanas | coberto | dimensionamento |
| e-mail Vitor 24/09/2026 16:20 | Licença do Bot Manager por aditivo ao contrato direto Lumina–Akamai, co-terminação em 31/03/2027; provisionamento em até 10 dias úteis após a assinatura | coberto | premissas |

## Requisitos

| REQ | Requisito | Origem | Evidência no insumo | Falantes |
|---|---|---|---|---|
| REQ-01 | Detectar e mitigar a raspagem automatizada do simulador de cotação de seguro auto, que copia a tabela de preços | transcrição 23/09/2026 — Camila Reis | Milhares de cotações por hora vindas de robôs, provavelmente de concorrentes e comparadores | client |
| REQ-02 | Identificar automação que se apresenta como navegador comum e não é detectada pelo WAF atual | transcrição 23/09/2026 — Diego Martins | O WAF atual pega ataque, mas não pega esses robôs, eles parecem navegador normal | client |
| REQ-03 | Reduzir as cotações automatizadas que disparam consultas pagas a dois bureaus de dados | transcrição 23/09/2026 — Camila Reis | Cada cotação consulta dois bureaus, e pagamos por consulta; estimativa do cliente de que pelo menos metade das cotações seja de robôs | client |
| REQ-04 | Ter o Bot Manager em operação antes do lançamento do novo seguro auto em 15/01/2027, respeitando o congelamento de 15/12/2026 a 05/01/2027 | transcrição 23/09/2026 — Diego Martins | Estamos lançando o novo seguro auto em 15/01/2027; congelamento de fim de ano de 15/12/2026 a 05/01/2027 | client |
| REQ-05 | Avaliar logins suspeitos na área do cliente, ainda não confirmados | transcrição 23/09/2026 — Camila Reis | Também vimos alguns logins suspeitos na área do cliente, mas nada confirmado ainda | client |

## Números do cliente

- transcrição 23/09/2026 — Camila Reis: milhares de cotações por hora vindas de robôs → contexto_de_dor
- transcrição 23/09/2026 — Camila Reis: Cada cotação consulta dois bureaus → contexto_de_dor
- transcrição 23/09/2026 — Camila Reis: No mês passado foram cerca de 2,1 milhões de cotações → dimensionamento
- transcrição 23/09/2026 — Camila Reis: estimamos que pelo menos metade seja de robôs → contexto_de_dor
- transcrição 23/09/2026 — Diego Martins: lançando o novo seguro auto em 15/01/2027 → meta
- transcrição 23/09/2026 — Diego Martins: congelamento de fim de ano vai de 15/12/2026 a 05/01/2027 → meta

## Perguntas abertas

- Quais endpoints e fluxos do simulador de cotação (hostnames, caminhos e chamadas de API) devem receber a política de proteção contra automação?
- Qual a data prevista para a assinatura do aditivo de licenciamento do Bot Manager entre a Lumina e a Akamai?
- A Lumina pode compartilhar evidências dos logins suspeitos na área do cliente (volume, período, padrão) para avaliar a necessidade de proteção de contas?
- Existem comparadores ou parceiros autorizados que consultam o simulador de forma automatizada e devem ser mantidos em lista de permissão?
