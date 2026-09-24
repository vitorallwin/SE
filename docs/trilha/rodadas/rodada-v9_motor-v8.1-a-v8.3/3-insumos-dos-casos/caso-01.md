# Vértice Educação

## Material recebido

### E-mail recebido em 22/09/2026
**De:** Paulo Andrade — Coordenador de Infraestrutura, Vértice Educação
**Para:** comercial@populos
**Assunto:** Migração de DNS

Olá, tudo bem?

Somos uma rede de faculdades particulares com 14 unidades. Hoje o DNS dos nossos domínios fica no painel do registrador, e já tivemos dois episódios este ano em que o painel ficou fora do ar e não conseguimos alterar registros. Queremos migrar o DNS autoritativo para a Akamai (Edge DNS), com DNSSEC.

São 4 zonas: vertice.edu.br, vertice.com.br, portalaluno.vertice.edu.br e vestibularvertice.com.br. Juntas, somam cerca de 380 registros. Não usamos nenhum recurso exótico, só A, AAAA, CNAME, MX, TXT e alguns SRV do e-mail.

O período de matrículas começa em 11/01/2027, e a migração precisa estar concluída e estável antes disso. Não podemos ter indisponibilidade no portal do aluno.

O site principal e o portal do aluno rodam num único servidor em um provedor de hospedagem. No futuro talvez a gente pense em melhorar a segurança do site, mas não é o momento e não temos orçamento para isso agora.

Precisamos de uma proposta de implantação.

Abraço,
Paulo

## Decisões internas POPULOS fornecidas para este caso
| Campo | Registro | Aprovado por | Data | Onde foi aprovado |
|---|---|---|---|---|
| engagement_type | implementation | Vitor (dono comercial) | 24/09/2026 | E-mail interno de aprovação de 24/09/2026 |
| Garantia | A POPULOS corrigirá defeitos diretamente atribuíveis aos serviços executados por 30 dias corridos após o aceite final. | Vitor (dono comercial) | 24/09/2026 | E-mail interno de aprovação de 24/09/2026 |
| Licenciamento | As licenças Akamai serão adquiridas diretamente pela Vértice Educação junto à Akamai. | Vitor (dono comercial) | 24/09/2026 | E-mail interno de aprovação de 24/09/2026 |
| SLA | Tabela institucional do template POPULOS | populos_standard | — | Template POPULOS vigente |
| Estimativa de esforço | 3 a 4 semanas | Ana (arquiteta responsável) | 24/09/2026 | E-mail interno de aprovação de 24/09/2026 |
