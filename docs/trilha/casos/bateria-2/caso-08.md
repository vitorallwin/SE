# Prefeitura Municipal de Rio Claro do Sul — Pregão Eletrônico nº 112/2026

## TERMO DE REFERÊNCIA
**Órgão:** Secretaria Municipal de Tecnologia da Informação (SMTI)
**Sessão pública:** 28/10/2026

### 1. Objeto
1.1 Contratação de serviço de DNS autoritativo e de proteção de aplicações web em nuvem, com licenciamento por 12 (doze) meses, implantação, repasse de conhecimento e suporte técnico, para os serviços digitais do município.

### 2. Justificativa
2.1 O portal de serviços e o sistema de emissão de notas fiscais sofreram 4 (quatro) indisponibilidades em 2026, atribuídas a ataques na camada de aplicação.
2.2 O DNS dos domínios municipais é mantido em servidor próprio, sem redundância geográfica.

### 3. Abrangência
3.1 DNS autoritativo para 3 (três) zonas: rioclarodosul.sp.gov.br, notas.rioclarodosul.sp.gov.br e turismorcs.com.br, com cerca de 150 registros no total.
3.2 Proteção de aplicações para as 5 (cinco) aplicações do Anexo I.
3.3 Tráfego legítimo agregado estimado em 6 milhões de requisições por dia, com picos de 400 requisições por segundo.

### 4. Requisitos técnicos
4.1 DNS autoritativo distribuído, com suporte a DNSSEC.
4.2 Firewall de aplicação web (WAF) com proteção contra as categorias OWASP Top 10 e atualização automática de regras.
4.3 Mitigação de ataques de negação de serviço na camada de aplicação (camada 7).
4.4 Controle de taxa de requisições (rate limiting) configurável por aplicação.
4.5 Painel de eventos de segurança acessível pela equipe da SMTI.
4.6 Exportação de eventos de segurança em formato compatível com syslog.

### 5. Implantação
5.1 Migração das 3 zonas DNS e onboarding das 5 aplicações, com configuração de políticas e testes.
5.2 Prazo de implantação: 45 (quarenta e cinco) dias corridos a partir da Ordem de Serviço.
5.3 As mudanças em produção deverão ocorrer em janelas acordadas com a SMTI.

### 6. Qualificação técnica
6.1 A CONTRATADA deverá comprovar possuir ao menos 2 (dois) profissionais com certificação técnica emitida pelo fabricante da solução ofertada.

### 7. Suporte técnico
7.1 Suporte técnico em regime 8x5 durante a vigência de 12 meses.
7.2 Incidentes de severidade alta: resposta em até 1 hora e resolução em até 4 horas.
7.3 Incidentes de severidade média: resposta em até 2 horas e resolução em até 8 horas.

### 8. Garantia
8.1 Garantia dos serviços de implantação por 12 (doze) meses após o Termo de Aceite Definitivo.

### 9. Aceite
9.1 Termo de Aceite Provisório (TAP) após a conclusão da implantação e Termo de Aceite Definitivo (TAD) 10 dias após o TAP sem pendências.

### 10. Licenciamento
10.1 Licenças fornecidas pela CONTRATADA, com vigência de 12 meses a partir da ativação.

### 11. Proposta
11.1 A proposta técnica deverá responder a cada item deste Termo de Referência, indicando a forma de atendimento, e informar a marca e o nome comercial dos serviços ofertados.

## ANEXO I — Aplicações
| # | Aplicação | Tipo |
|---|---|---|
| 1 | Portal de Serviços ao Cidadão | Web |
| 2 | Emissão de Notas Fiscais de Serviço | Web + API |
| 3 | Agendamento de Saúde | Web |
| 4 | Portal do Contribuinte (IPTU) | Web |
| 5 | Portal de Turismo | Web |

## Aprovações internas POPULOS (e-mails de 24/09/2026)

> **De:** Vitor (Executivo de Contas, POPULOS) — 24/09/2026 14:05
> Aprovo para o Pregão 112/2026 de Rio Claro do Sul: engajamento de implantação (implementation). Aprovo que as licenças Akamai serão fornecidas pela POPULOS por meio de revenda autorizada, conforme o item 10.1 do TR. Aprovo a garantia: a POPULOS corrigirá defeitos diretamente atribuíveis aos serviços executados por 12 meses após o Termo de Aceite Definitivo. Aprovo o suporte técnico 8x5 durante a vigência de 12 meses, conforme o item 7.1 do TR.

> **De:** Vitor (Executivo de Contas, POPULOS) — 24/09/2026 14:40
> Confirmo para o Pregão 112/2026: a POPULOS possui 3 profissionais com certificação técnica Akamai vigente, e a documentação será apresentada na habilitação, atendendo ao item 6.1.

> **De:** Ana Ribeiro (Arquiteta, POPULOS) — 24/09/2026 15:10
> Aprovo a estimativa de esforço para o Pregão 112/2026: 5 a 6 semanas de implantação.
