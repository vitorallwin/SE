# Sales Engineer AI V2

Aplicação local para transformar atas, requisitos e escopo em propostas técnicas Akamai auditáveis e gerar um DOCX baseado no template POPULOS fornecido.

## O que está pronto

- Dashboard de propostas com busca, filtros e indicadores.
- Wizard para criar uma proposta em quatro etapas.
- Pipeline com Discovery, Arquitetura, QA técnico, Redação, QA comercial, Reparo e Documento.
- Operação em modo de demonstração sem LLM.
- Integração opcional com Gemini via `GEMINI_API_KEY` no ambiente.
- Matriz requisito → solução → evidência → status.
- Portões humanos para pendências e aprovação final.
- Governança em quatro estados: compromisso, premissa, pendência do cliente e decisão interna POPULOS. O último estado bloqueia a emissão e nunca aparece no DOCX.
- Geração de DOCX sobre o template neutro POPULOS aprovado, preservando sua estrutura de 13 seções, identidade visual, tabelas, caixas e paginação.
- Triagem condicional de linhas, frentes, quantitativos, cronograma, garantia e SLA. A tabela fixa de SLA é institucional; garantia e modelo de fornecimento exigem decisão comercial da oportunidade.
- Skill local de autoria com regras globais, contratos por agente, seleção de produtos, rastreabilidade e critérios de aceite.
- Manifesto de documento que decide quais blocos e opções entram em cada proposta.
- Persistência local em JSON, pronta para ser substituída por Supabase.
- Endpoint de saúde e testes automatizados do fluxo principal.

## Executar

No PowerShell:

```powershell
$env:GEMINI_API_KEY="sua-chave"
$env:GEMINI_MODEL="gemini-3.5-flash-lite"
.\run.ps1
```

Abra `http://localhost:8010`.

Sem `GEMINI_API_KEY`, o sistema usa o motor determinístico de demonstração. Ele permite testar todo o fluxo e gerar o documento sem chamadas externas.

## Segurança da chave

A chave nunca é devolvida pela API, gravada em proposta, escrita em logs ou salva no navegador. Ela existe somente no ambiente do processo do servidor.

## Estrutura

```text
app.py                 servidor HTTP e API
sales_engineer/        domínio, pipeline, Gemini e DOCX
web/                   interface SPA
assets/                template neutro aprovado e ativos locais
skills/                constituição, contratos dos agentes e regras compartilhadas
data/                  persistência local e documentos gerados
tests/                 testes de unidade e integração
```

## Testes

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

## Próxima evolução para produção

Trocar o `JsonStore` por Supabase/PostgreSQL, adicionar autenticação, fila de execução, RAG técnico com fontes oficiais e armazenamento de artefatos. Os contratos do pipeline já isolam essas substituições.
