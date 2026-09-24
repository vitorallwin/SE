from __future__ import annotations

from copy import deepcopy
from typing import Any

from .proposal_rules import RULES_VERSION


def build_nexuspay_v5(source: dict[str, Any]) -> dict[str, Any]:
    """NexusPay V5: Phase 1 (assessment and design) as the committed scope, implementation as an optional Phase 2.

    Every requirement points to the source material; every client number has a destination;
    case decisions (engagement, Phase 1 estimate, warranty, licenses) stay open until the case script resolves them.
    """
    proposal = deepcopy(source)
    proposal["rules_version"] = RULES_VERSION
    proposal["code"] = "PT-2609-NXP5"
    proposal["opportunity"] = "Resiliência e proteção da plataforma de pagamentos"
    proposal["opportunity_id"] = "nexuspay-2026-09"

    proposal["client_scope"] = {
        "type": "assessment",
        "excludes_implementation": True,
        "source": "escopo informado: excluída a \"implementação prática de infraestrutura nesta fase de descoberta\"; premissa original 2 cita \"sessões de desenho técnico subsequentes\"",
    }
    proposal["governance"] = {
        "engagement_type": {"state": "populos_internal_decision", "value": None, "source": "escopo do cliente é assessment; implantação só como fase opcional"},
        "phase1_estimate": {"state": "populos_internal_decision", "value": None, "source": "estimativa da Fase 1 exige responsável técnico"},
        "warranty": {"state": "populos_internal_decision", "value": None, "source": "placeholder do template"},
        "license_supply": {"state": "populos_internal_decision", "value": None, "source": "decisão comercial do caso"},
        "sla": {"state": "commitment", "value": "tabela institucional do template POPULOS", "source": "populos_standard"},
    }

    proposal["solution_decisions"] = [
        {"product_id": "edge_dns", "status": "recommended", "requirement_ids": ["REQ-01"], "rationale": "Zona autoritativa distribuída para os domínios críticos.", "client_summary": "Edge DNS mantém a zona autoritativa distribuída, com DNSSEC.", "capabilities": ["DNS autoritativo", "Anycast", "DNSSEC"]},
        {"product_id": "gtm", "status": "recommended", "requirement_ids": ["REQ-01", "REQ-04"], "rationale": "Substitui o failover manual por decisão automática entre as três origens.", "client_summary": "Global Traffic Management decide o destino entre as três origens com base em testes de saúde e políticas de prioridade.", "capabilities": ["testes de saúde", "failover entre provedores", "balanceamento ponderado"]},
        {"product_id": "ion", "status": "recommended", "requirement_ids": ["REQ-04"], "rationale": "Atua na jornada de checkout, onde o cliente relatou abandono acima de dois segundos.", "client_summary": "Ion otimiza a entrega do checkout e do portal de lojistas.", "capabilities": ["aceleração dinâmica", "otimização de protocolo", "redução de carga na origem"]},
        {"product_id": "app_api_protector", "status": "recommended", "requirement_ids": ["REQ-02", "REQ-03", "REQ-05", "REQ-06", "REQ-09"], "rationale": "Protege aplicações e APIs de pagamento contra ameaças web, abuso de API e DDoS de camada 7.", "client_summary": "App & API Protector aplica WAF adaptativo, descoberta de APIs, controle de taxa de requisições e mitigação DDoS de camada 7.", "capabilities": ["WAF adaptativo", "descoberta de APIs", "controle de taxa de requisições"]},
        {"product_id": "prolexic", "status": "recommended", "requirement_ids": ["REQ-03"], "rationale": "Cobre DDoS volumétrico de rede, que a proteção de aplicação não atende.", "implementation_status": "modality_pending", "client_summary": "Prolexic cobre ataques volumétricos de rede e a exposição direta das origens; o modelo de implantação é definido no Desenho.", "capabilities": ["mitigação DDoS L3/L4", "centros de limpeza de tráfego", "runbooks de mitigação"]},
        {"product_id": "bot_manager", "status": "recommended", "requirement_ids": ["REQ-02"], "rationale": "Credential stuffing e bots raspadores foram relatados na reunião.", "client_summary": "Bot Manager Premier classifica e responde à automação em cadastro, login e raspagem de tabelas de taxas.", "capabilities": ["detecção de bots", "resposta adaptativa", "segmentação por jornada"]},
        {"product_id": "alb", "status": "optional", "requirement_ids": ["REQ-01"], "rationale": "Roteamento por requisição entre origens.", "trigger": "incluído somente se o Desenho identificar necessidade de roteamento por requisição entre origens (caminho, cabeçalho ou cookie), além do failover por DNS."},
        {"product_id": "account_protector", "status": "optional", "requirement_ids": ["REQ-02"], "rationale": "Risco por identidade no cadastro de lojistas.", "trigger": "incluído somente se o Assessment confirmar identificadores de conta e eventos de login disponíveis para avaliação de risco por identidade no cadastro de lojistas."},
        {"product_id": "malware_protection", "status": "excluded", "requirement_ids": [], "rationale": "Não foi identificado fluxo de upload de arquivos.", "capabilities": []},
        {"product_id": "ip_accelerator", "status": "excluded", "requirement_ids": [], "rationale": "As jornadas priorizadas são HTTP e HTTPS.", "capabilities": []},
    ]
    proposal["products"] = ["edge_dns", "gtm", "ion", "app_api_protector", "prolexic", "bot_manager"]

    proposal["architecture"] = {
        "summary": "A arquitetura-alvo protege e acelera as jornadas de checkout e cadastro na borda, automatiza a continuidade entre as três origens e separa a defesa de aplicação da proteção DDoS de infraestrutura. Na Fase 1, cada frente é avaliada e detalhada no Desenho; a implantação ocorre na Fase 2.",
        "flow": ["Clientes e lojistas", "Borda Akamai", "Edge DNS e GTM", "Origens multi-cloud"],
    }

    proposal["sections"] = [{
        "title": "Resumo executivo",
        "paragraphs": [
            "Nas campanhas de Black Friday e Pix Day do ano passado, a NexusPay enfrentou gargalos no gateway e quedas parciais de API causadas por tráfego malicioso e credential stuffing. Cada atraso acima de dois segundos no checkout leva ao abandono de carrinho, e o failover manual entre as duas nuvens públicas e o datacenter próprio consome minutos preciosos a cada indisponibilidade. Somam-se bots que raspam tabelas de taxas e dados de novos lojistas, e a exigência regulatória de auditoria rigorosa, com dados de cartão e PII protegidos em logs e em trânsito.",
            "A POPULOS propõe um projeto em duas fases. A Fase 1, objeto desta proposta, realiza o assessment e o desenho da solução Akamai em três frentes, em quatro a seis semanas. Ela entrega a linha de base do checkout, o plano de migração DNS sem impacto ao SLA, o plano de evento e o desenho de implantação. A Fase 2, apresentada como opção, implanta a solução em duas ondas, com a proteção prioritária antes do congelamento de mudanças sempre que o calendário permitir.",
        ],
    }]
    proposal["discovery"]["business_goals"] = [
        "Preparar a plataforma para os picos de Black Friday e Pix Day, com viabilidade e risco residual declarados antes do evento (REQ-03 e REQ-07)",
        "Eliminar o failover manual entre as três origens sem impacto ao SLA (REQ-01)",
        "Reduzir o abuso automatizado em cadastro, login e APIs de pagamento (REQ-02)",
        "Medir e reduzir a latência do checkout a partir de uma linha de base decomposta (REQ-04)",
        "Manter dados de cartão e PII fora dos logs e protegidos em trânsito, com trilha de auditoria (REQ-05, REQ-08, REQ-09 e REQ-10)",
        "Dar ao SOC visibilidade em tempo real do tráfego legítimo e malicioso (REQ-06)",
    ]

    proposal["client_numbers"] = [
        {"quote": "atraso superior a dois segundos no checkout resulta em abandono de carrinho", "ref": "transcrição [00:01:10]", "destination": "contexto_de_dor", "summary_marker": "acima de dois segundos no checkout", "reason": "A POPULOS não controla o tempo total da jornada; o compromisso é medir contra a linha de base."},
        {"quote": "failover manual custa preciosos minutos", "ref": "transcrição [00:02:05]", "destination": "contexto_de_dor", "summary_marker": "consome minutos preciosos"},
        {"quote": "gargalos no gateway e quedas parciais de API no ano passado", "ref": "transcrição [00:00:42]", "destination": "contexto_de_dor", "summary_marker": "do ano passado"},
        {"quote": "dois provedores de nuvem pública e um datacenter próprio", "ref": "transcrição [00:02:05]", "destination": "dimensionamento"},
    ]

    proposal["dimensioning"] = [
        ("Origens", "3", "Duas nuvens públicas e um datacenter próprio", "Confirmado"),
        ("Jornadas críticas", "Checkout, cadastro, login e APIs de pagamento", "Informadas na reunião de levantamento", "Confirmado"),
        ("Zonas DNS, domínios e APIs", "A levantar", "Inventário no Assessment", "Pendente"),
    ]
    proposal["estimates"] = [
        {"item": "Duração da Fase 1", "value": "4 a 6 semanas", "owner": None},
    ]

    proposal["traceability"] = [
        {"requirement_id": "REQ-01", "requirement": "Failover automatizado entre as três origens, sem impacto ao SLA", "solution": "Edge DNS + GTM", "evidence": "Cenários de roteamento e plano de migração DNS aprovados.", "source": "requisito original 1; transcrição [00:02:05]"},
        {"requirement_id": "REQ-02", "requirement": "Proteção de APIs de pagamento e cadastro contra bots e fraude automatizada", "solution": "AAP + Bot Manager", "evidence": "Políticas-alvo por jornada e plano de testes aprovados.", "source": "requisito original 2; transcrição [00:00:42] e [00:01:10]"},
        {"requirement_id": "REQ-03", "requirement": "Mitigação de DDoS volumétrico e de aplicação", "solution": "AAP + Prolexic", "evidence": "Desenho de mitigação por camada e pré-requisitos de rede do Prolexic avaliados.", "source": "requisito original 3; transcrição [00:03:10]"},
        {"requirement_id": "REQ-04", "requirement": "Redução da latência do checkout", "solution": "Ion + GTM", "evidence": "Linha de base decomposta e meta de melhoria proposta.", "source": "requisito original 4; transcrição [00:01:10]"},
        {"requirement_id": "REQ-05", "requirement": "Conformidade com LGPD e PCI DSS", "solution": "AAP", "evidence": "Mapa de dados sensíveis por fluxo e matriz de responsabilidades.", "source": "requisito original 5; transcrição [00:02:35]"},
        {"requirement_id": "REQ-06", "requirement": "Visibilidade em tempo real do tráfego legítimo e malicioso para o SOC", "solution": "AAP + Bot Manager + SIEM", "evidence": "Especificação de eventos e casos de uso do SOC aprovados.", "source": "requisito original 6"},
        {"requirement_id": "REQ-07", "requirement": "Estabilidade nos picos de Black Friday e Pix Day", "solution": "Plano de evento", "evidence": "Cenários de pico dimensionados e viabilidade da Onda 1 registrada.", "source": "transcrição [00:00:42]; escopo informado (dimensionamento de cenários de pico)"},
        {"requirement_id": "REQ-08", "requirement": "Dados de cartão e PII fora dos logs", "solution": "Integração SIEM com mascaramento", "evidence": "Especificação de campos e regra de mascaramento aprovadas pelo SOC.", "source": "transcrição [00:02:35]"},
        {"requirement_id": "REQ-09", "requirement": "Proteção de dados sensíveis em trânsito", "solution": "Política TLS na borda e proteção de origem", "evidence": "Relatório de inspeção TLS, certificados e caminho borda–origem.", "source": "transcrição [00:02:35]; escopo informado (inspeção de conformidade em trânsito)"},
        {"requirement_id": "REQ-10", "requirement": "Trilha de auditoria exigida pela regulação do Banco Central", "solution": "Registros e retenção de evidências", "evidence": "Requisitos de trilha e retenção validados com a conformidade.", "source": "transcrição [00:01:10]"},
    ]

    proposal["assessment_items"] = [
        "Inventário de zonas DNS, domínios, aplicações, APIs e origens;",
        "Métricas de tráfego, latência, disponibilidade e segurança, inclusive dos picos anteriores;",
        "Fluxos de dados sensíveis em logs e em trânsito, requisitos de auditoria e dependências de integração.",
    ]
    proposal["scope"] = {
        "included": [
            "Análise da arquitetura de rede e DNS: zonas, registros, TTLs, delegações, origens e dependências entre as duas nuvens públicas e o datacenter",
            "Cenários de roteamento global de tráfego com Edge DNS e Global Traffic Management, incluindo política de failover automatizado e critérios de saúde das três origens",
            "Plano de migração da zona autoritativa sem impacto ao SLA: redução prévia de TTL, validação da zona, coexistência, janela de delegação e reversão",
            "Avaliação das estratégias de mitigação de ameaças web e de API com App & API Protector, Bot Manager Premier e Prolexic, incluindo os pré-requisitos de rede do Prolexic",
            "Linha de base de latência do checkout decomposta entre DNS, conexão e TLS, borda, origem e jornada, com avaliação do Ion e proposta de meta",
            "Inspeção da proteção de dados sensíveis em trânsito: política TLS na borda, inventário e ciclo de certificados e proteção do caminho entre a borda e as origens",
            "Especificação da integração de eventos com o SIEM, com mascaramento de dados de cartão e PII antes do envio",
            "Levantamento dos requisitos de trilha de auditoria e retenção de evidências com as áreas de segurança e conformidade da NexusPay",
            "Dimensionamento dos cenários de pico de Black Friday e Pix Day e classificação da viabilidade de proteção antes do congelamento de mudanças",
            "Orientação à NexusPay para obter, junto à Akamai, a atestação PCI DSS vigente e a matriz de responsabilidades dos serviços avaliados",
        ],
        "deliverables": [
            "Relatório de Assessment com diagnóstico, riscos, linha de base e recomendações justificadas",
            "Desenho de alto nível (HLD), matriz de rastreabilidade, plano de testes e plano de reversão da Fase 2",
            "Plano de migração DNS, plano de evento e plano de implantação em ondas da Fase 2",
        ],
        "excluded": [
            "Alterações diretas no código interno do gateway de pagamentos e das aplicações",
            "Implementação de infraestrutura e mudanças em produção na Fase 1; a implantação corresponde à Fase 2 opcional",
            "Homologação jurídica formal de contratos e certificação de LGPD ou PCI DSS",
            "Operação continuada, NOC 24x7 e equipe residente",
        ],
    }

    proposal["delivery"] = {
        "phases": [
            {"name": "Fase 1 — Assessment", "kind": "assessment", "weeks": [2, 3], "duration": "2 a 3 sem.", "objective": "Levantar ativos, jornadas, linha de base de latência, dados sensíveis em logs e em trânsito, requisitos de auditoria e as datas de pico e de congelamento.", "dependency": "Acessos e documentação", "outputs": ["relatório de Assessment", "linha de base"]},
            {"name": "Fase 1 — Desenho", "kind": "design", "weeks": [2, 3], "duration": "2 a 3 sem.", "objective": "Definir a arquitetura-alvo, as políticas por jornada, o plano de migração DNS, o plano de evento e a sequência de ondas da Fase 2.", "dependency": "Relatório de Assessment aceito", "outputs": ["HLD", "planos da Fase 2"]},
        ],
        "responsibilities": [
            {"party": "Infraestrutura NexusPay", "responsibility": "Disponibilizar acessos a DNS, nuvens, origens e documentação de arquitetura."},
            {"party": "Segurança e SOC NexusPay", "responsibility": "Validar dados sensíveis, requisitos de auditoria e eventos do SIEM."},
            {"party": "Aplicações NexusPay", "responsibility": "Fornecer métricas das jornadas e volumes dos picos anteriores."},
        ],
    }
    proposal["populos_roles"] = [
        ["Gerência do PMO", "Supervisão executiva e escalonamento do projeto.", "Sob demanda"],
        ["Executivo de Contas", "Gestão comercial, contratos e governança da conta.", "Sob demanda"],
        ["Gerente de Projeto POPULOS", "Planejamento, coordenação, riscos e reportes.", "Durante o projeto"],
        ["Arquiteto POPULOS", "Assessment, desenho da arquitetura Akamai e planos da Fase 2.", "Conforme cronograma"],
        ["Equipe Técnica POPULOS", "Levantamentos, análises, medições e documentação da Fase 1.", "Conforme cronograma"],
        ["Ponto focal do cliente", "Decisões, acessos e escalonamentos.", "Durante o projeto"],
    ]
    proposal["optional_phase"] = {
        "title": "Fase 2 opcional — implantação em ondas",
        "intro": "A implantação não integra o escopo desta proposta. A Fase 2 é apresentada como opção, e a contratação dela depende do aceite do Desenho e da aprovação da NexusPay. Duração, metas numéricas e condições comerciais serão definidas no Desenho.",
        "conditions": [
            "A viabilidade da Onda 1 antes do congelamento de mudanças será classificada no Assessment como cabe, cabe parcialmente ou não cabe, a partir das datas de início e de congelamento confirmadas pela NexusPay. A classificação declara os componentes cobertos, os itens adiados e o risco residual para o evento.",
            "Cada onda que entra em produção tem marco de aceite próprio. As condições de garantia da Fase 2, inclusive a contagem por onda e a cobertura da Onda 1 durante o intervalo entre as ondas, serão definidas na contratação dessa fase.",
        ],
        "waves": [
            {"name": "Onda 1 — proteção prioritária", "components": ["app_api_protector", "bot_manager", "prolexic"], "goes_to_production": True,
             "activities": "Onboarding das APIs de pagamento, do cadastro e do login no App & API Protector; políticas do Bot Manager Premier; integração com o SIEM com mascaramento de dados de cartão e PII; restrição de acesso às origens; onboarding do Prolexic no modelo definido no Desenho, somente após a aprovação dos pré-requisitos de rede.",
             "acceptance": "Marco formal de aceite próprio da Onda 1, com as evidências dos testes em produção. Nas classificações cabe e cabe parcialmente, esse aceite ocorre antes do congelamento de mudanças.",
             "milestone": "aceite da Onda 1"},
            {"name": "Onda 2 — continuidade e desempenho", "components": ["edge_dns", "gtm", "ion"], "goes_to_production": True,
             "activities": "Migração da zona autoritativa para o Edge DNS conforme o plano aprovado; políticas de Global Traffic Management entre as três origens; propriedades Ion para o checkout e o portal de lojistas.",
             "acceptance": "Aceite formal da Onda 2 após os testes de failover e a medição contra a linha de base.",
             "milestone": "aceite da Onda 2"},
        ],
    }

    proposal["event_readiness"] = [
        "Dimensionar os cenários de pico de Black Friday e Pix Day a partir dos volumes históricos fornecidos pela NexusPay",
        "Confirmar as datas de início, de congelamento de mudanças e dos eventos, e classificar a viabilidade da Onda 1: cabe, cabe parcialmente ou não cabe",
        "Declarar, em cada classificação, os componentes cobertos, os itens adiados e o risco residual para o evento",
        "Especificar o plano de evento da Fase 2: teste de carga, revisão de capacidade, congelamento de mudanças, monitoramento, runbook de degradação e reversão",
        "Prever sala de crise liderada pela POPULOS durante o evento, com acionamento da Akamai conforme o nível de suporte contratado",
    ]

    proposal["assumptions"] = [
        "A NexusPay possui acesso administrativo aos provedores de DNS e de nuvem e o disponibilizará no início do Assessment",
        "A equipe técnica da NexusPay participará das sessões de desenho técnico",
        "Os ambientes de homologação e produção possuem documentação de arquitetura atualizada disponível para análise",
        "A NexusPay fornecerá os volumes históricos de Black Friday e Pix Day e as datas de congelamento de mudanças",
        "Na Fase 2, as licenças e subscrições Akamai fornecidas pela POPULOS estarão ativas antes da configuração",
    ]
    proposal["restrictions"] = [
        "O prazo da Fase 1 depende da disponibilização de acessos, documentação e participantes no início de cada etapa;",
        "Mudanças em requisitos, volumetria ou integrações poderão exigir revisão de prazo e escopo;",
        "A proposta não constitui homologação jurídica nem certificação de conformidade regulatória;",
        "A faixa de quatro a seis semanas refere-se somente à Fase 1; o prazo da Fase 2 será definido no Desenho.",
    ]
    proposal["risks"] = [
        {"risk": "Inventário incompleto de zonas, APIs e origens", "impact": "Cobertura parcial do desenho", "mitigation": "Descoberta de APIs e validação por responsáveis durante o Assessment."},
        {"risk": "Datas de início e de congelamento incompatíveis com a Onda 1", "impact": "Proteção prioritária ausente no evento", "mitigation": "Classificação de viabilidade no Assessment e risco residual declarado no plano de evento."},
        {"risk": "Migração DNS com TTL alto ou delegação mal coordenada", "impact": "Indisponibilidade parcial e impacto ao SLA", "mitigation": "Redução prévia de TTL, coexistência, janela aprovada e reversão testada."},
        {"risk": "Eventos de segurança com dados de cartão ou PII", "impact": "Exposição de dados sensíveis no SIEM", "mitigation": "Mascaramento especificado e aprovado antes de qualquer envio de eventos."},
        {"risk": "Origem acessível fora da borda", "impact": "Desvio dos controles e DDoS direto", "mitigation": "Restrição e autenticação de origem previstas no Desenho."},
    ]

    proposal["acceptance_criteria"] = [
        {"requirement_id": "REQ-01", "phase": "committed", "criterion": "Plano de migração DNS aprovado, com redução prévia de TTL, validação da zona, coexistência, janela de delegação e reversão testável."},
        {"requirement_id": "REQ-04", "phase": "committed", "criterion": "Linha de base de latência do checkout entregue, decomposta entre DNS, conexão e TLS, borda, origem e jornada, sob carga e geografia definidas, com proposta de meta de melhoria para a Fase 2."},
        {"requirement_id": "REQ-02", "phase": "committed", "criterion": "Desenho de mitigação aprovado por camada (aplicação, APIs, automações e infraestrutura), com o modelo de implantação do Prolexic definido ou o risco residual registrado."},
        {"requirement_id": "REQ-08", "phase": "committed", "criterion": "Especificação de eventos do SIEM aprovada pelo SOC, com a lista de campos de cartão e PII e a regra de mascaramento de cada fonte."},
        {"requirement_id": "REQ-09", "phase": "committed", "criterion": "Relatório de inspeção de dados em trânsito entregue, cobrindo protocolos e cifras TLS, certificados e proteção do caminho entre a borda e as origens dos domínios avaliados."},
        {"requirement_id": "REQ-10", "phase": "committed", "criterion": "Requisitos de trilha de auditoria e retenção de evidências validados com a área de conformidade da NexusPay."},
        {"requirement_id": "REQ-07", "phase": "committed", "criterion": "Cenários de pico dimensionados e viabilidade da Onda 1 classificada, com componentes cobertos, itens adiados e risco residual."},
        {"requirement_id": "REQ-01", "phase": "optional", "criterion": "Failover automatizado entre as três origens validado em teste controlado, dentro do tempo-alvo aprovado no Desenho."},
        {"requirement_id": "REQ-08", "phase": "optional", "criterion": "Nenhum número de cartão ou PII em claro nos eventos entregues ao SIEM, verificado por amostragem."},
        {"requirement_id": "REQ-02", "phase": "optional", "criterion": "Rotas prioritárias de cadastro, login e APIs de pagamento cobertas pelas políticas aprovadas, com casos benignos e maliciosos executados."},
        {"requirement_id": "REQ-04", "phase": "optional", "criterion": "Melhoria de latência medida contra a linha de base, sob a mesma carga e geografia, conforme a meta aprovada no Desenho."},
    ]

    proposal["open_questions"] = [
        "Confirmar datas de início, de congelamento de mudanças e dos eventos de pico",
        "Confirmar RPS médio e de pico por jornada",
        "Confirmar inventário de zonas, domínios e APIs",
        "Confirmar blocos IP, capacidade BGP/GRE e modelo operacional do Prolexic",
        "Confirmar identificadores de conta disponíveis para avaliar o Account Protector",
    ]

    proposal["source_coverage"] = [
        {"ref": "transcrição [00:00:42]", "statement": "Estabilidade em Black Friday e Pix Day", "status": "coberto", "targets": ["REQ-07"]},
        {"ref": "transcrição [00:00:42]", "statement": "Gargalos no gateway e quedas parciais de API por tráfego malicioso e credential stuffing", "status": "coberto", "targets": ["REQ-02", "REQ-03", "sumário"]},
        {"ref": "transcrição [00:01:10]", "statement": "Regulação do Banco Central exige auditoria rigorosa", "status": "coberto", "targets": ["REQ-10"]},
        {"ref": "transcrição [00:01:10]", "statement": "Baixa latência; atraso acima de dois segundos causa abandono", "status": "coberto", "targets": ["REQ-04", "sumário"]},
        {"ref": "transcrição [00:01:10]", "statement": "Bots raspadores de tabelas de taxas e de dados de lojistas no cadastro", "status": "coberto", "targets": ["REQ-02"]},
        {"ref": "transcrição [00:02:05]", "statement": "Duas nuvens públicas e um datacenter próprio", "status": "coberto", "targets": ["dimensionamento"]},
        {"ref": "transcrição [00:02:05]", "statement": "DNS tradicional com failover manual", "status": "coberto", "targets": ["REQ-01", "sumário"]},
        {"ref": "transcrição [00:02:05]", "statement": "Automatizar a resiliência sem impactar o SLA", "status": "coberto", "targets": ["REQ-01", "escopo"]},
        {"ref": "transcrição [00:02:35]", "statement": "Dados de cartão e PII não podem ficar expostos em logs", "status": "coberto", "targets": ["REQ-08"]},
        {"ref": "transcrição [00:02:35]", "statement": "Dados sensíveis não podem ser interceptados no trânsito", "status": "coberto", "targets": ["REQ-09"]},
        {"ref": "transcrição [00:02:35]", "statement": "Conformidade com LGPD e PCI DSS", "status": "coberto", "targets": ["REQ-05"]},
        {"ref": "transcrição [00:03:10]", "statement": "Aceleração de APIs transacionais", "status": "coberto", "targets": ["REQ-04"]},
        {"ref": "requisitos originais 1 a 6", "statement": "Seis requisitos registrados", "status": "coberto", "targets": ["REQ-01", "REQ-02", "REQ-03", "REQ-04", "REQ-05", "REQ-06"]},
        {"ref": "escopo informado — incluso", "statement": "Rede e DNS; ameaças web e API; roteamento global; dados sensíveis em trânsito; cenários de pico", "status": "coberto", "targets": ["escopo"]},
        {"ref": "escopo informado — excluído", "statement": "Código do gateway; implementação nesta fase; homologação jurídica", "status": "coberto", "targets": ["exclusões", "engajamento"]},
        {"ref": "premissas originais 1 a 3", "statement": "Acesso administrativo; sessões de desenho; documentação atualizada", "status": "coberto", "targets": ["premissas"]},
        {"ref": "transcrição [00:00:15]", "statement": "Crescimento acelerado e planos de expansão", "status": "descartado", "reason": "Contexto sem requisito verificável; será confirmado no Assessment se alterar a volumetria."},
    ]

    proposal["document_text"] = {
        "about_akamai": "A Akamai oferece serviços distribuídos de entrega, desempenho, proteção e observabilidade para aplicações, APIs e infraestrutura exposta à internet. A arquitetura desta proposta combina apenas as capacidades ligadas às jornadas e aos riscos relatados pela NexusPay.",
        "about_solution": "Para a NexusPay Brasil, a solução integra continuidade multi-cloud, proteção de aplicações, APIs e infraestrutura, defesa contra abuso automatizado e otimização do checkout. Cada frente possui requisito, entregável da Fase 1 e critério de aceite definidos.",
        "partnership": "Esta proposta dá sequência à reunião de levantamento conduzida pela Akamai com as lideranças de tecnologia e segurança da NexusPay. A POPULOS responde pelo assessment e pelo desenho da arquitetura e, se contratada a Fase 2, pela implantação, testes e documentação. As credenciais nominais da equipe serão apresentadas na mobilização.",
        "coverage": "Abrangência: checkout, APIs de pagamento, cadastro e autenticação de lojistas, zonas DNS e as três origens distribuídas entre duas nuvens públicas e o datacenter próprio.",
        "diagram_origins_title": "Origens NexusPay",
        "readiness_intro": "Na Fase 1, a prontidão para os eventos críticos é tratada como dimensionamento e planejamento. A execução do plano de evento corresponde à Fase 2.",
        "dimensioning_intro": "Os quantitativos abaixo separam o que foi confirmado na reunião de levantamento do que será levantado no Assessment. A quantidade contratual de zonas, propriedades, APIs e capacidade de proteção será definida no Desenho.",
        "heading_6": "6.  Serviços POPULOS — Metodologia",
        "methodology_intro": "A POPULOS disponibilizará equipe técnica e gestão de projeto para conduzir a Fase 1 — Assessment e Desenho. A implantação corresponde à Fase 2 opcional, descrita na seção 6.3.",
        "knowledge_transfer": "A passagem de conhecimento abrangerá a arquitetura proposta, as decisões de desenho, os planos da Fase 2 e a documentação prevista no escopo.",
        "tests": "Na Fase 1, a validação consiste na revisão técnica conjunta dos entregáveis, conforme os critérios da seção 10. Os testes de implantação correspondem à Fase 2.",
        "schedule_intro": "A Fase 1 está estimada entre quatro e seis semanas, contadas a partir da reunião de início e condicionadas à liberação de acessos, documentação e participantes.",
        "schedule_sequence": "A Fase 2, se contratada, será executada em duas ondas separadas pelo período de congelamento de mudanças. A duração dela em calendário depende das datas de congelamento confirmadas no Assessment e será definida no Desenho.",
        "acceptance_intro": "A aceitação da Fase 1 seguirá os critérios abaixo, vinculados à matriz de rastreabilidade:",
        "acceptance_optional_intro": "Critérios de referência da Fase 2, aplicáveis somente se contratada. As metas numéricas serão fixadas no Desenho:",
        "warranty_intro": "A garantia técnica cobre a correção de defeitos diretamente atribuíveis aos serviços executados pela POPULOS. O prazo consta do quadro Garantia e vigência.",
        "closing": "A Fase 1 encerra-se com o aceite do Desenho. Operação continuada, suporte gerenciado, NOC 24x7 e equipe residente exigem contratação específica.",
        "callout_limits": "A Fase 1 não realiza mudanças em produção. Alterações no código das aplicações e serviços de terceiros permanecem fora do escopo.",
        "callout_migration": "A Fase 1 entrega o plano de migração. Na Fase 2, a zona autoritativa migra para o Edge DNS com redução prévia de TTL, coexistência, janela aprovada e reversão, sem interrupção das jornadas.",
        "callout_milestones": "Fase 1: aceite do relatório de Assessment e aceite do Desenho. Fase 2, se contratada: aceite formal de cada onda antes da etapa seguinte.",
    }
    proposal["quality_score"] = None
    return proposal
