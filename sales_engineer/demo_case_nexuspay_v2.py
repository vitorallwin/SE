from __future__ import annotations

from copy import deepcopy
from typing import Any


def build_nexuspay_v2(source: dict[str, Any]) -> dict[str, Any]:
    """Upgrade the AI-created NexusPay case with a competitive, source-classified proposal state."""
    proposal = deepcopy(source)
    proposal["code"] = "PT-2609-NXP2"
    proposal["opportunity"] = "Resiliência e proteção da plataforma de pagamentos"
    proposal["source_policy"] = {
        "client_fact": ["reunião simulada", "requisitos registrados"],
        "populos_standard": ["template neutro POPULOS", "tabela institucional de SLA"],
        "bounded_estimate": ["cronograma de 8 a 12 semanas", "faixas iniciais de dimensionamento"],
        "pending": ["RPS de pico", "inventário final de APIs", "blocos IP e modelo de roteamento Prolexic"],
    }
    proposal["governance"] = {
        "warranty": {"state": "populos_internal_decision", "value": None, "source": "placeholder do template"},
        "license_supply": {"state": "populos_internal_decision", "value": None, "source": "decisão comercial da oportunidade"},
        "sla": {"state": "commitment", "value": "tabela institucional do template POPULOS", "source": "populos_standard"},
    }
    proposal["solution_decisions"] = [
        {"product_id": "edge_dns", "status": "recommended", "requirement_ids": ["REQ-01"], "rationale": "Mantém a camada DNS autoritativa distribuída e resiliente para os domínios críticos.", "confidence": 0.92, "capabilities": ["DNS autoritativo", "Anycast", "DNSSEC", "API de gestão"]},
        {"product_id": "gtm", "status": "recommended", "requirement_ids": ["REQ-01", "REQ-04"], "rationale": "Executa decisão DNS dinâmica entre as origens multi-cloud com testes de saúde, políticas de prioridade e roteamento por desempenho.", "confidence": 0.92, "capabilities": ["liveness tests", "failover entre provedores", "balanceamento ponderado", "roteamento por desempenho"]},
        {"product_id": "alb", "status": "optional", "requirement_ids": ["REQ-01", "REQ-04"], "rationale": "Complementa o GTM quando a decisão precisa ocorrer por requisição HTTP na borda, com stickiness e roteamento entre origens da propriedade.", "confidence": 0.78, "capabilities": ["liveness tests", "roteamento HTTP", "session stickiness", "origens condicionais"]},
        {"product_id": "ion", "status": "recommended", "requirement_ids": ["REQ-04"], "rationale": "Atua sobre a jornada web de checkout com aceleração dinâmica, otimizações de protocolo e offload de origem, medidos contra a linha de base.", "confidence": 0.84, "capabilities": ["aceleração dinâmica", "otimização de protocolo", "offload de origem", "HTTP/3"]},
        {"product_id": "app_api_protector", "status": "recommended", "requirement_ids": ["REQ-02", "REQ-03", "REQ-05", "REQ-06"], "rationale": "Protege aplicações e APIs contra ameaças OWASP, abuso de APIs e DDoS de camada 7, com descoberta de APIs, rate controls e integração ao SIEM.", "confidence": 0.94, "capabilities": ["WAF adaptativo", "API discovery", "proteção de dados sensíveis", "DDoS L7", "rate controls", "integração SIEM"]},
        {"product_id": "prolexic", "status": "recommended", "requirement_ids": ["REQ-03"], "rationale": "Fecha a cobertura de DDoS de infraestrutura e tráfego L3/L4 que não é atendida apenas pela proteção de aplicação na borda.", "implementation_status": "modality_pending", "implementation_condition": "Definir Routed GRE, IP Protect ou outro modelo aprovado após validar blocos IP, ASN, roteamento e operação.", "confidence": 0.78, "capabilities": ["mitigação DDoS L3/L4", "scrubbing distribuído", "runbooks", "proteção de origens"]},
        {"product_id": "bot_manager", "status": "recommended", "requirement_ids": ["REQ-02"], "rationale": "Classifica automações em cadastro e login e aplica respostas graduais para credential stuffing e raspagem de dados.", "confidence": 0.91, "capabilities": ["detecção de bots", "resposta adaptativa", "segmentação por jornada", "telemetria"]},
        {"product_id": "account_protector", "status": "optional", "requirement_ids": ["REQ-02"], "rationale": "Adiciona risco por identidade para criação, login, recuperação e atividade pós-login; deve ser ativado após validar identificadores e eventos disponíveis.", "confidence": 0.76, "capabilities": ["risco de criação de conta", "perfil comportamental", "sinais de confiança", "proteção pós-login"]},
        {"product_id": "malware_protection", "status": "excluded", "requirement_ids": [], "rationale": "Não foi identificado fluxo de upload de arquivos nesta etapa.", "confidence": 0.95, "capabilities": []},
        {"product_id": "ip_accelerator", "status": "excluded", "requirement_ids": [], "rationale": "As jornadas priorizadas utilizam HTTP e HTTPS; não foi registrado requisito de aceleração TCP ou UDP fora da entrega web.", "confidence": 0.95, "capabilities": []},
    ]
    proposal["products"] = ["edge_dns", "gtm", "ion", "app_api_protector", "prolexic", "bot_manager"]
    proposal["architecture"] = {
        "summary": "A arquitetura proposta protege e acelera as jornadas de checkout e cadastro na borda, automatiza a continuidade entre três ambientes de origem e separa claramente a defesa de aplicação da proteção DDoS de infraestrutura.",
        "flow": ["Clientes e lojistas", "Ion e controles de segurança", "Edge DNS e GTM", "Origens multi-cloud"],
        "implementation_waves": [
            {"name": "Assessment", "duration": "1 a 2 semanas"},
            {"name": "Design", "duration": "1 a 2 semanas"},
            {"name": "Implementação e homologação", "duration": "4 a 6 semanas"},
            {"name": "Produção e estabilização", "duration": "2 semanas"},
        ],
    }
    proposal["discovery"]["business_goals"] = [
        "Preservar disponibilidade e capacidade de resposta nos picos de Black Friday e Pix Day (OBJ-01; REQ-01 e REQ-03)",
        "Reduzir abuso nas jornadas de cadastro, login e pagamento sem ampliar exposição de dados (OBJ-02; REQ-02 e REQ-05)",
        "Melhorar a experiência regional e acelerar detecção e investigação operacional (OBJ-03; REQ-04 e REQ-06)",
    ]
    proposal["sections"] = [{
        "title": "Resumo executivo",
        "paragraphs": [
            "A NexusPay precisa eliminar o failover manual, proteger as APIs de pagamento e conter automações maliciosas nas jornadas de cadastro e autenticação. A indisponibilidade em períodos de pico interrompe receita e conversão; o abuso de contas amplia chargebacks e investigação; e lacunas de evidência aumentam o esforço de conformidade.",
            "A POPULOS propõe uma arquitetura Akamai em três frentes: continuidade e desempenho multi-cloud; proteção de aplicações, APIs e infraestrutura; e controle de bots e abuso de contas. A implantação está estimada entre oito e doze semanas, com passagem por homologação, produção controlada e estabilização assistida.",
        ],
    }]
    proposal["dimensioning"] = [
        ("Zonas DNS e domínios críticos", "3 a 8", "Faixa para planejamento; validar inventário", "Estimativa"),
        ("Aplicações e APIs prioritárias", "5 a 15", "Checkout, cadastro, login e APIs associadas", "Estimativa"),
        ("Origens multi-cloud", "3", "Duas nuvens públicas e um datacenter", "Confirmado"),
    ]
    proposal["traceability"] = [
        {"requirement_id": "REQ-01", "requirement": "Alta disponibilidade e failover multi-cloud", "solution": "Edge DNS + GTM; ALB opcional", "evidence": "Teste controlado de indisponibilidade e relatório de decisão de tráfego."},
        {"requirement_id": "REQ-02", "requirement": "Proteção de APIs, cadastro e login contra abuso", "solution": "AAP + Bot Manager; Account Protector opcional", "evidence": "Suíte de ataques e automações com registros de ação por jornada."},
        {"requirement_id": "REQ-03", "requirement": "DDoS de aplicação e infraestrutura", "solution": "AAP + Prolexic", "evidence": "Teste L7, revisão do runbook e exercício de prontidão L3/L4."},
        {"requirement_id": "REQ-04", "requirement": "Latência de checkout e experiência regional", "solution": "Ion + GTM", "evidence": "Comparativo de linha de base e teste da jornada sob carga acordada."},
        {"requirement_id": "REQ-05", "requirement": "Proteção de dados e apoio à conformidade", "solution": "AAP", "evidence": "Inventário de APIs, regras de dados sensíveis e relatório de configuração."},
        {"requirement_id": "REQ-06", "requirement": "Visibilidade para o SOC", "solution": "AAP + Bot Manager", "evidence": "Eventos recebidos e pesquisáveis no SIEM com campos acordados."},
        {"requirement_id": "REQ-07", "requirement": "Prontidão para Black Friday e Pix Day", "solution": "Plano de evento e implantação em duas ondas", "evidence": "Teste de carga, checklist de freeze, runbook e ata do exercício de war room."},
    ]
    proposal["scope"] = {
        "included": [
            "Levantamento de zonas, aplicações, APIs, origens, fluxos e integrações de observabilidade",
            "Desenho de Edge DNS, GTM e opção de ALB para continuidade multi-cloud",
            "Configuração de propriedades Ion para checkout e portal de lojistas",
            "Onboarding de aplicações e APIs no App & API Protector, incluindo descoberta, WAF, rate controls e proteção de dados sensíveis",
            "Políticas de Bot Manager para cadastro, login, credential stuffing e raspagem",
            "Desenho e prontidão operacional do Prolexic, condicionados à validação de blocos IP, BGP/GRE ou alternativa IP Protect",
            "Integração de eventos de segurança e automação com o SIEM da NexusPay",
            "Preparação para Black Friday e Pix Day com teste de carga, revisão de capacidade, congelamento de mudanças, runbook e war room liderado pela POPULOS",
            "Apoio à NexusPay na obtenção, junto à Akamai, da atestação PCI DSS vigente e da matriz de responsabilidades dos serviços em escopo",
        ],
        "deliverables": ["HLD, runbooks, matriz de rastreabilidade e plano de testes", "As-built, evidências de homologação e plano de reversão"],
        "excluded": ["Alterações no código-fonte do gateway e das aplicações", "Operação continuada, NOC 24x7 e equipe residente", "Homologação jurídica ou certificação formal de LGPD e PCI DSS"],
    }
    proposal["delivery"] = {
        "phases": [
            {"name": "Assessment", "objective": "Inventariar jornadas, ativos, linha de base, dependências e confirmar a data de freeze.", "duration": "1 sem.", "dependency": "Acessos e documentação", "outputs": ["inventário", "linha de base"]},
            {"name": "Design", "objective": "Fechar arquitetura, políticas, testes, reversão e composição das ondas.", "duration": "1 sem.", "dependency": "Assessment aprovado", "outputs": ["HLD", "plano de testes"]},
            {"name": "Onda 1 — pré-evento", "objective": "Colocar AAP e Bot Manager em produção antes do freeze; concluir a prontidão Prolexic sem prometer onboarding enquanto roteamento e conectividade não forem aprovados.", "duration": "3 a 4 sem.", "dependency": "Licenças, acessos e gate de prontidão", "outputs": ["produção prioritária", "runbook de evento"]},
            {"name": "Onda 2 — pós-evento", "objective": "Implantar GTM, Ion e demais componentes aprovados, estabilizar e concluir o aceite.", "duration": "4 a 6 sem.", "dependency": "Fim do freeze e janela aprovada", "outputs": ["as-built", "aceite"]},
        ],
        "responsibilities": [
            {"party": "Infraestrutura NexusPay", "responsibility": "Disponibilizar DNS, origens, conectividade, blocos IP e janelas de mudança."},
            {"party": "Segurança e SOC NexusPay", "responsibility": "Aprovar políticas, dados sensíveis, casos de teste e integração SIEM."},
            {"party": "Aplicações NexusPay", "responsibility": "Validar jornadas, APIs, comportamento funcional e métricas de experiência."},
        ],
    }
    proposal["assumptions"] = [
        "A NexusPay disponibilizará acessos administrativos e documentação no início de cada fase",
        "As licenças e subscrições fornecidas pela POPULOS estarão ativas antes da configuração",
        "Haverá ambiente de homologação e janela de produção aprovada",
        "Os times de infraestrutura, segurança, aplicações e SOC participarão dos testes e aceites",
    ]
    proposal["risks"] = [
        {"risk": "Inventário incompleto de APIs e origens", "impact": "Cobertura parcial ou retrabalho", "mitigation": "Descoberta de APIs, validação por responsáveis e congelamento do inventário por onda."},
        {"risk": "Acesso tardio a DNS, SIEM ou clouds", "impact": "Deslocamento do cronograma", "mitigation": "Checklist de prontidão e gate de entrada em cada fase."},
        {"risk": "Mudança sem janela ou plano de reversão", "impact": "Risco operacional em produção", "mitigation": "Ensaio em homologação, aprovação CAB e reversão testada."},
        {"risk": "Origem exposta fora da borda", "impact": "Bypass dos controles e DDoS direto", "mitigation": "Restrição de origem e validação do desenho Prolexic."},
    ]
    proposal["event_readiness"] = [
        "Resultado de planejamento: cabe parcialmente antes do freeze; AAP e Bot Manager compõem a onda prioritária, enquanto Prolexic permanece em prontidão até a aprovação do modelo de conectividade e roteamento",
        "Executar teste de carga pré-evento com cenários aprovados e decomposição das métricas de borda, origem e jornada",
        "Revisar capacidade, alarmes, contatos e caminhos de escalonamento antes do congelamento de mudanças",
        "Aplicar change freeze e registrar exceções por aprovação executiva",
        "Manter runbook de degradação controlada, reversão e comunicação",
        "Conduzir war room liderado pela POPULOS; participação da Akamai somente conforme suporte contratado e plano de escalonamento",
    ]
    proposal["acceptance_criteria"] = [
        {"requirement_id": "REQ-01", "criterion": "Failover entre origens concluído em até 90 segundos após a confirmação de falha pelos testes de saúde, respeitando TTL e cache DNS configurados.", "evidence": "Relatório do teste controlado com linha do tempo e destino selecionado.", "owner": "Infraestrutura NexusPay"},
        {"requirement_id": "REQ-02", "criterion": "Cem por cento das rotas prioritárias de cadastro, login e APIs de pagamento cadastradas nas políticas aprovadas, com casos benignos e maliciosos executados.", "evidence": "Plano de testes, logs de ação e aprovação funcional.", "owner": "Segurança e Aplicações"},
        {"requirement_id": "REQ-03", "criterion": "Proteção L7 validada por teste controlado e prontidão L3/L4 validada por runbook, conectividade e exercício de mesa do fluxo de mitigação.", "evidence": "Relatório de segurança e ata do exercício operacional.", "owner": "SOC e Infraestrutura"},
        {"requirement_id": "REQ-04", "criterion": "A linha de base será decomposta entre DNS, conexão e TLS, processamento de borda, tempo de origem e jornada fim a fim sob a mesma carga e geografia. A meta de melhoria será aprovada até o gate de saída do Assessment; se o gate não aprovar uma meta, o aceite desta frente será a entrega do relatório decomposto e do plano de otimização.", "evidence": "Relatório comparativo, critérios do gate de Assessment e registro da decisão sobre a meta.", "owner": "Aplicações NexusPay e POPULOS"},
        {"requirement_id": "REQ-06", "criterion": "Eventos de WAF, API e bots disponíveis no SIEM em até cinco minutos, contendo identificador da política, ação, endpoint e correlação temporal.", "evidence": "Consulta salva no SIEM e amostra de eventos correlacionados.", "owner": "SOC NexusPay"},
        {"requirement_id": "REQ-07", "criterion": "O plano do evento será aprovado antes do freeze, contendo cenários de carga, contatos, critérios de escalonamento, runbook de degradação e decisão registrada sobre o risco residual do Prolexic.", "evidence": "Plano aprovado, resultado do teste de carga e ata do exercício de war room.", "owner": "PMO POPULOS e NexusPay"},
    ]
    proposal["open_questions"] = [
        "Confirmar RPS médio e de pico por jornada",
        "Confirmar inventário de APIs e domínios por onda",
        "Confirmar blocos IP, capacidade BGP/GRE e modelo operacional do Prolexic",
        "Confirmar identificadores de conta disponíveis para avaliar Account Protector",
    ]
    proposal["quality_score"] = 86
    return proposal
