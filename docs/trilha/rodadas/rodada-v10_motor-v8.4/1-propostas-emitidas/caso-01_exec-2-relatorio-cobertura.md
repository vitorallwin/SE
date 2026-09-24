# Relatório de cobertura — Vértice Educação (POPULOS-VERTICE-EDGE-DNS-2026)

- Regras: v10
- Modo dos dados: test
- Engajamento: implementation

## Decisões

| Decisão | Valor | Aprovado por | Data | Modo |
|---|---|---|---|---|
| engagement_type | implementation | Vitor (dono comercial) | 2026-09-24 | test |
| warranty | A POPULOS corrigirá defeitos diretamente atribuíveis aos serviços executados por 30 dias corridos após o aceite final. | Vitor (dono comercial) | 2026-09-24 | test |
| license_supply | As licenças Akamai serão adquiridas diretamente pela Vértice Educação junto à Akamai. | Vitor (dono comercial) | 2026-09-24 | test |
| sla | Tabela institucional do template POPULOS | None | None | None |
| effort_estimate | 3 a 4 semanas | Ana (arquiteta responsável) | 2026-09-24 | test |

## Cobertura do insumo

| Referência | Trecho | Status | Destino |
|---|---|---|---|
| E-mail de 22/09/2026, §1 | Rede de faculdades particulares com 14 unidades. | descartado | Contexto institucional; o número de unidades não altera o dimensionamento do DNS. |
| E-mail de 22/09/2026, §1 | O DNS fica no painel do registrador, que ficou fora do ar em dois episódios este ano, impedindo alterações de registros. | coberto | REQ-05, sumário |
| E-mail de 22/09/2026, §2 | Migrar o DNS autoritativo para a Akamai (Edge DNS), com DNSSEC. | coberto | REQ-01, REQ-02, escopo |
| E-mail de 22/09/2026, §3 | 4 zonas: vertice.edu.br, vertice.com.br, portalaluno.vertice.edu.br e vestibularvertice.com.br, com cerca de 380 registros. | coberto | REQ-01, dimensionamento |
| E-mail de 22/09/2026, §3 | Apenas registros A, AAAA, CNAME, MX, TXT e alguns SRV do e-mail. | coberto | REQ-01, dimensionamento, premissas |
| E-mail de 22/09/2026, §4 | Matrículas começam em 11/01/2027; a migração precisa estar concluída e estável antes. | coberto | REQ-03, sumário |
| E-mail de 22/09/2026, §4 | Não pode haver indisponibilidade no portal do aluno. | coberto | REQ-04, escopo |
| E-mail de 22/09/2026, §5 | O site principal e o portal do aluno rodam num único servidor em um provedor de hospedagem. | coberto | premissas, exclusões |
| E-mail de 22/09/2026, §5 | Melhoria de segurança do site pode ser pensada no futuro, mas não é o momento e não há orçamento. | coberto | exclusões |
| E-mail de 22/09/2026, §6 | Precisamos de uma proposta de implantação. | coberto | engajamento |

## Requisitos

| REQ | Requisito | Origem | Evidência no insumo | Falantes |
|---|---|---|---|---|
| REQ-01 | Migrar o DNS autoritativo das zonas vertice.edu.br, vertice.com.br, portalaluno.vertice.edu.br e vestibularvertice.com.br (cerca de 380 registros dos tipos A, AAAA, CNAME, MX, TXT e SRV) para o Edge DNS. | E-mail de 22/09/2026, §2 e §3 | "Queremos migrar o DNS autoritativo para a Akamai (Edge DNS), com DNSSEC." / "São 4 zonas [...] cerca de 380 registros." | client |
| REQ-02 | Ativar DNSSEC nas 4 zonas. | E-mail de 22/09/2026, §2 | "Queremos migrar o DNS autoritativo para a Akamai (Edge DNS), com DNSSEC." | client |
| REQ-03 | Concluir a migração, com operação estável, antes de 11/01/2027. | E-mail de 22/09/2026, §4 | "O período de matrículas começa em 11/01/2027, e a migração precisa estar concluída e estável antes disso." | client |
| REQ-04 | Não haver indisponibilidade de resolução do portal do aluno durante a migração. | E-mail de 22/09/2026, §4 | "Não podemos ter indisponibilidade no portal do aluno." | client |
| REQ-05 | Poder alterar registros DNS sem depender do painel do registrador. | E-mail de 22/09/2026, §1 | "já tivemos dois episódios este ano em que o painel ficou fora do ar e não conseguimos alterar registros." | client |

## Números do cliente

- E-mail de 22/09/2026, §1: 14 unidades → descartado_com_motivo
- E-mail de 22/09/2026, §1: dois episódios este ano → contexto_de_dor
- E-mail de 22/09/2026, §3: 4 zonas → dimensionamento
- E-mail de 22/09/2026, §3: cerca de 380 registros → dimensionamento
- E-mail de 22/09/2026, §4: 11/01/2027 → meta
- Cabeçalho do e-mail: 22/09/2026 → descartado_com_motivo

## Perguntas abertas

- Qual o prazo, informado pela Akamai, entre a compra e a ativação das licenças do Edge DNS? As licenças precisam estar ativas até 14/12/2026 para que a migração termine antes de 11/01/2027.
- Qual a data de início do congelamento de mudanças da Vértice antes das matrículas? A troca de delegação e a ativação do DNSSEC precisam terminar antes dela.
- Quem na Vértice tem acesso ao registrador (registro.br) para alterar os servidores de nomes e publicar os registros DS?
- Quais janelas de mudança a Vértice autoriza para a troca de delegação de cada zona?
