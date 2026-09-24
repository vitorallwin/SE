# Lumina Seguros (cliente existente)

## Contexto da conta (registro interno POPULOS)
- Cliente POPULOS desde 2024.
- Produtos Akamai contratados hoje: Ion, App & API Protector e Edge DNS.
- O contrato Akamai atual foi firmado **diretamente entre a Lumina e a Akamai**. A POPULOS presta os serviços de implantação e suporte.
- Vigência do contrato Akamai atual: até 31/03/2027.
- Propriedades Ion em produção: www.lumina.com.br, cotacao.lumina.com.br, api.lumina.com.br.
- Suporte POPULOS em vigor: contrato de sustentação 8x5 até 31/03/2027.

## Transcrição da reunião de 23/09/2026 (resumida)
**Camila Reis (Head de Canais Digitais):** O simulador de cotação de seguro auto está sendo raspado. Vemos milhares de cotações por hora vindas de robôs, provavelmente de concorrentes e comparadores, que copiam nossa tabela de preços. Isso também aumenta o custo com as consultas que fazemos aos bureaus de dados a cada cotação.

**Diego Martins (Arquiteto de Soluções da Lumina):** O WAF atual pega ataque, mas não pega esses robôs, eles parecem navegador normal. Queremos o Bot Manager.

**Camila:** Também vimos alguns logins suspeitos na área do cliente, mas nada confirmado ainda.

**Diego:** Estamos lançando o novo seguro auto em 15/01/2027, com campanha de mídia forte. Queremos o Bot Manager funcionando antes disso. Nosso congelamento de fim de ano vai de 15/12/2026 a 05/01/2027.

**Camila:** Cada cotação consulta dois bureaus, e pagamos por consulta. No mês passado foram cerca de 2,1 milhões de cotações, e estimamos que pelo menos metade seja de robôs.

## Aprovações internas POPULOS (e-mails de 24/09/2026)

> **De:** Vitor (Executivo de Contas, POPULOS) — 24/09/2026 09:40
> Aprovo para a Lumina Seguros: engajamento de implantação (implementation). Aprovo a garantia: a POPULOS corrigirá defeitos diretamente atribuíveis aos serviços executados por 90 dias corridos após o aceite final.

> **De:** Ana Ribeiro (Arquiteta, POPULOS) — 24/09/2026 10:15
> Aprovo a estimativa de esforço da Lumina Seguros: 4 a 5 semanas.

> **De:** Vitor (Executivo de Contas, POPULOS) — 24/09/2026 16:20
> Aprovo o licenciamento da Lumina Seguros: a licença do Bot Manager será adicionada ao contrato direto entre a Lumina e a Akamai, por aditivo, com co-terminação em 31/03/2027. A POPULOS presta apenas os serviços. A Akamai informou que o provisionamento leva até 10 dias úteis após a assinatura do aditivo.
