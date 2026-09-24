# Solaris Energia

## Ata da reunião de 22/09/2026
**Presentes:** Beatriz Nogueira (Gerente de Canais Digitais, Solaris), Henrique Sato (Coordenador de Segurança, Solaris), Ana Ribeiro (Arquiteta, POPULOS), Vitor (Executivo, POPULOS).

**Beatriz:** A Solaris é distribuidora de energia em 3 estados, com 4,2 milhões de unidades consumidoras. O portal do cliente concentra segunda via de conta, pedido de religação e consulta de débitos. O app usa as mesmas APIs do portal.

**Henrique:** Em junho e em agosto o portal ficou fora do ar por cerca de 3 horas em cada episódio. Foi um ataque de negação de serviço na camada de aplicação: milhões de requisições na página de consulta de débitos. Não houve ataque volumétrico de rede.

**Henrique:** Também temos robôs testando números de CPF na consulta de débitos. Quando o CPF existe, a página devolve nome e endereço. É exposição de dado pessoal e já estamos tratando com o DPO.

**Beatriz:** Temos dois ambientes de origem: o datacenter próprio, que é o principal, e uma nuvem pública, que hoje só recebe tráfego manualmente quando o datacenter cai. Queremos que isso seja automático.

**Beatriz:** Em 01/03/2027 começa a campanha estadual de renegociação de dívidas. Na última campanha, o tráfego do portal triplicou. Precisamos estar protegidos e com o failover automático antes dessa data.

**Henrique:** Não temos congelamento formal de mudanças. As mudanças em produção só acontecem às terças, das 22h às 2h.

**Beatriz:** Queremos primeiro um assessment e desenho, e depois a implantação. Não queremos contratar a implantação às cegas.

**Ana (POPULOS):** Proposta em duas fases: Fase 1 de assessment e desenho, contratada agora; Fase 2 de implantação, apresentada como opção e contratada após o aceite do desenho.

**Henrique:** O DNS dos domínios fica no nosso provedor atual e está funcionando bem. Não é o foco.

## Aprovações internas POPULOS (e-mails de 24/09/2026)

> **De:** Vitor (Executivo de Contas, POPULOS) — 24/09/2026 09:14
> Aprovo para a Solaris Energia: engajamento em fases (phased), com Fase 1 de assessment e desenho contratada e Fase 2 de implantação opcional. Aprovo também: as licenças Akamai serão fornecidas pela POPULOS por meio de revenda autorizada. E aprovo a garantia: a POPULOS corrigirá defeitos diretamente atribuíveis aos serviços executados por 90 dias corridos após o aceite de cada fase.

> **De:** Vitor (Executivo de Contas, POPULOS) — 24/09/2026 09:20
> Sobre o SLA da Solaris Energia, aprovo: a tabela institucional de SLA da POPULOS se aplica somente à Fase 2 (implantação). A Fase 1 não tem SLA de atendimento a incidentes.

> **De:** Ana Ribeiro (Arquiteta, POPULOS) — 24/09/2026 10:02
> Aprovo as estimativas de esforço da Solaris Energia: Fase 1 de 3 a 4 semanas; Fase 2 de 6 a 8 semanas.

> **De:** Vitor (Executivo de Contas, POPULOS) — 24/09/2026 11:30
> Confirmei com a Akamai: o provisionamento das licenças para a Solaris Energia leva até 2 semanas após a assinatura do pedido.
