# Grupo Mariá Varejo

## Material recebido (colado pelo executivo de contas, sem edição)

### E-mail 1 — 15/09/2026
**De:** Rodrigo Tanaka — Gerente de TI
Oi pessoal, conforme falamos, nosso e-commerce tá sofrendo com lentidão nos horários de pico e com uns bots que ficam consultando preço o dia inteiro. A gente tem umas 500 mil visitas por dia no site. Parte dos nossos domínios já passa pela Cloudflare (o blog e o site institucional), o e-commerce não. Queremos entender o que a Akamai faria. Ah, e tem o app também, que conversa com as mesmas APIs do site.

### E-mail 2 — 17/09/2026
**De:** Fernanda Lopes — CISO
Complementando o Rodrigo: o problema de segurança é mais sério do que lentidão. Tivemos um incidente de credential stuffing em julho, cerca de 1.200 contas de clientes foram acessadas indevidamente e tivemos que resetar senhas em massa. Precisamos de WAF e proteção contra bots urgente. Our audit team also flagged that we have no visibility of API traffic at all. Não quero solução paliativa.

### E-mail 3 — 18/09/2026
**De:** Marcelo Brito — CFO
Pessoal, só lembrando que o orçamento deste ano está praticamente fechado. Se for fazer alguma coisa agora, que seja o mínimo necessário para atravessar a Black Friday. O resto a gente discute no orçamento de 2027, que fecha em fevereiro.

### Notas de WhatsApp do executivo de contas (19/09/2026)
- falei c/ rodrigo, ele disse q na vdd são uns 5 milhões de acessos/dia no pico de campanha
- fernanda perguntou se "vocês garantem 100% de bloqueio de bot"
- eles têm 2 data centers, acho q ativo-passivo? confirmar
- black friday deles começa na quarta 25/11, a campanha vai até domingo 29/11
- o app é o canal q mais cresce, 40% das vendas (rodrigo)

### Notas da call de 20/09/2026 (parciais)
- presentes: Rodrigo, Fernanda, executivo POPULOS; Marcelo não entrou
- Fernanda: quer tudo configurado em modo bloqueio antes da BF
- Rodrigo: time dele congela mudanças a partir de 01/11
- Rodrigo: "se for pra mexer no DNS do e-commerce agora eu prefiro não"
- ninguém falou de prazo de contratação / compras
- [áudio cortou a partir daqui]

## Decisões internas POPULOS fornecidas para este caso
Nenhuma.
