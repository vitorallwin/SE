from __future__ import annotations

from typing import Any

from .demo_case_nexuspay_v5 import build_nexuspay_v5


# Quem falou cada trecho da transcrição do material-fonte.
SPEAKERS = {
    "[00:00:42]": "client",   # Marina, CTO NexusPay
    "[00:01:10]": "client",   # Roberto, CISO NexusPay
    "[00:02:05]": "client",   # Marina, CTO NexusPay
    "[00:02:35]": "client",   # Roberto, CISO NexusPay
    "[00:03:10]": "vendor",   # Carlos, consultor Akamai (resumo da reunião)
}


def _speakers(source: str) -> list[str]:
    roles = {role for ref, role in SPEAKERS.items() if ref[1:-1] in source}
    if "requisito original" in source or "escopo informado" in source:
        roles.add("input_document")
    return sorted(roles)


def build_nexuspay_v6(source: dict[str, Any]) -> dict[str, Any]:
    """NexusPay V6: V5 plus approval-bound decisions, speaker provenance, Black Friday 2026
    feasibility computed now, and an optional fast track that treats edge onboarding as a production change."""
    proposal = build_nexuspay_v5(source)
    proposal["rules_version"] = 6
    proposal["code"] = "PT-2609-NXP6"

    proposal["client_scope"]["forbidden_in_committed"] = ["sob carga", "testável", "teste de carga", "em produção"]
    # Decisões voltam a abertas: cada uma precisa de aprovador e do engajamento em que foi tomada.
    proposal["governance"]["sla"] = {"state": "populos_internal_decision", "value": None, "source": "aplicabilidade do SLA institucional ao engajamento"}

    for item in proposal["traceability"]:
        item["speakers"] = _speakers(item["source"])
        if item["requirement_id"] == "REQ-03":
            item["source"] = "requisito original 3 (DDoS volumétrico e de aplicação); transcrição [00:00:42] e [00:03:10]"
            item["speakers"] = _speakers(item["source"])

    for decision in proposal["solution_decisions"]:
        if decision["product_id"] == "account_protector":
            decision["trigger"] = "incluído se o Assessment confirmar contas comprometidas ou fraude após o login, além do credential stuffing já relatado, e se houver identificadores de conta e eventos de login disponíveis para avaliação de risco por identidade."

    # Fase 1 revista para 6 a 8 semanas após o crescimento do escopo.
    phases = proposal["delivery"]["phases"]
    phases[0].update({"weeks": [3, 4], "duration": "3 a 4 sem."})
    phases[1].update({"weeks": [3, 4], "duration": "3 a 4 sem."})
    proposal["estimates"] = [{"item": "Duração da Fase 1", "value": "6 a 8 semanas", "owner": None}]

    scope = proposal["scope"]["included"]
    scope[4] = "Linha de base de latência do checkout decomposta entre DNS, conexão e TLS, borda, origem e jornada, a partir de dados de RUM e de monitoramento sintético existentes ou de medição em homologação, com avaliação do Ion e proposta de meta"

    for criterion in proposal["acceptance_criteria"]:
        if criterion["phase"] == "committed" and criterion["requirement_id"] == "REQ-01":
            criterion["criterion"] = "Plano de migração DNS aprovado, com redução prévia de TTL, validação da zona, coexistência, janela de delegação e reversão especificada e revisada."
        if criterion["phase"] == "committed" and criterion["requirement_id"] == "REQ-04":
            criterion["criterion"] = "Linha de base de latência do checkout entregue, decomposta entre DNS, conexão e TLS, borda, origem e jornada, obtida de dados de RUM e sintéticos existentes ou de medição em homologação, com proposta de meta de melhoria para a Fase 2."

    proposal["critical_events"] = [
        {"name": "Black Friday 2026", "date": "2026-11-27", "source": "calendário público: sexta-feira após a quarta quinta-feira de novembro; evento citado na transcrição [00:00:42]"},
        {"name": "Pix Day", "date": None, "source": "transcrição [00:00:42]", "pending_question": "Confirmar a data do Pix Day e o período de congelamento de mudanças associado."},
    ]
    proposal["event_feasibility"] = [{
        "event": "Black Friday 2026",
        "reference_date": "2026-09-24",
        "phase1_end_earliest": "2026-11-05",
        "phase1_end_latest": "2026-11-19",
        "classification": "does_not_fit",
        "path": "Fase 2",
        "reason": "Mesmo com início na data da proposta, a Fase 1 termina entre 05/11 e 19/11, a 8 a 22 dias do evento e antes de qualquer contratação, licenciamento e onboarding da Fase 2, e antes de um congelamento de mudanças que costuma anteceder o evento.",
        "summary_marker": "Black Friday de 2026",
    }]

    summary = proposal["sections"][0]["paragraphs"]
    summary[1] = "A POPULOS propõe um projeto em duas fases. A Fase 1, objeto desta proposta, realiza o assessment e o desenho da solução Akamai em três frentes, em seis a oito semanas. Ela entrega a linha de base do checkout, o plano de migração DNS sem impacto ao SLA, o plano de evento e o desenho de implantação. A Fase 2, apresentada como opção, implanta a solução em duas ondas."
    summary.append("Para a Black Friday de 2026 (27/11), mesmo com início imediato, a Fase 1 termina entre 05/11 e 19/11, antes de qualquer implantação. Pela Fase 2, a proteção não fica pronta para esse evento. A proposta oferece por isso uma trilha rápida opcional (seção 6.4), que só será executada se couber antes do congelamento de mudanças da NexusPay, e declara o risco residual caso não caiba.")

    proposal["fast_track"] = {
        "title": "Trilha rápida opcional — Black Friday de 2026",
        "components": ["app_api_protector", "bot_manager"],
        "production_change": True,
        "controls": ["janela", "reversão", "aprovação"],
        "deadline_reference": "freeze",
        "first_question": "Algum hostname da NexusPay já trafega pela Akamai?",
        "paragraphs": [
            "A trilha rápida é uma opção separada da Fase 1, contratada somente com aprovação da NexusPay. Ela coloca as APIs de pagamento, o cadastro e o login atrás do App & API Protector e do Bot Manager Premier em paralelo ao Assessment.",
            "Entrar na borda Akamai já é uma mudança em produção, mesmo em modo de monitoramento: exige apontar os hostnames para a Akamai, provisionar certificados e ajustar a origem. Por isso a trilha tem janela, reversão e aprovação próprias, e não altera o limite da Fase 1.",
            "A trilha só é executada se couber antes do congelamento de mudanças da NexusPay, e não apenas antes do evento. Se não couber, ela não é executada, e o risco residual para a Black Friday de 2026 fica declarado no plano de evento.",
        ],
        "items": [
            "Pergunta inicial: algum hostname da NexusPay já trafega pela Akamai? Se sim, a trilha parte dessa configuração e o risco da mudança cai",
            "Pré-requisitos: data de congelamento informada pela NexusPay, emissão e validação dos certificados, restrição de origem e janela aprovada",
            "Operação em modo de monitoramento; bloqueio apenas para regras de alta confiança aprovadas pela NexusPay",
            "Prolexic fica fora da trilha rápida, porque depende da validação dos pré-requisitos de rede",
            "Marco de aceite próprio; garantia e condições comerciais definidas na contratação da trilha",
        ],
        "schedule_row": ["Trilha rápida (opcional)", "App & API Protector e Bot Manager Premier em modo de monitoramento, em paralelo ao Assessment.", "Aprovação da NexusPay e data de congelamento", "Até o congelamento", "aceite da trilha"],
    }

    proposal["optional_phase"]["conditions"][0] = "Para a Black Friday de 2026, a Onda 1 não fica pronta antes do evento (seção 2); a resposta para esse evento é a trilha rápida da seção 6.4. Para os eventos seguintes, incluindo o Pix Day, a viabilidade da Onda 1 será classificada no Assessment como cabe, cabe parcialmente ou não cabe, com os componentes cobertos, os itens adiados e o risco residual."
    proposal["assumptions"][4] = "Na Fase 2 e na trilha rápida, as licenças e subscrições Akamai fornecidas pela POPULOS estarão ativas antes da configuração"
    for risk in proposal["risks"]:
        if risk["risk"].startswith("Datas de início"):
            risk.update({"risk": "Congelamento de mudanças anterior à conclusão da trilha rápida", "mitigation": "Viabilidade declarada nesta proposta, trilha rápida condicionada ao congelamento e risco residual registrado no plano de evento."})
        if risk["risk"].startswith("Migração DNS"):
            risk["mitigation"] = "Redução prévia de TTL, coexistência, janela aprovada e reversão especificada e ensaiada em homologação."
    proposal["event_readiness"][1] = "Confirmar as datas de congelamento de mudanças e do Pix Day e reavaliar a viabilidade da trilha rápida e da Onda 1"
    proposal["open_questions"] += [
        "Informar a data de início do congelamento de mudanças para a Black Friday de 2026",
        "Informar se algum hostname da NexusPay já trafega pela Akamai",
        "Confirmar a autoria da lista de requisitos originais (cliente ou consultoria)",
    ]
    proposal["restrictions"][3] = "A faixa de seis a oito semanas refere-se somente à Fase 1; o prazo da Fase 2 será definido no Desenho."

    text = proposal["document_text"]
    text["schedule_intro"] = "A Fase 1 está estimada entre seis e oito semanas, contadas a partir da reunião de início e condicionadas à liberação de acessos, documentação e participantes."
    text["license_prefix"] = "A Fase 1 é exclusivamente de serviços e não requer licenças Akamai. Para a Fase 2 e a trilha rápida:"
    text["callout_milestones"] = "Fase 1: aceite do relatório de Assessment e aceite do Desenho. Trilha rápida e Fase 2, se contratadas: aceite formal próprio da trilha e de cada onda antes da etapa seguinte."
    return proposal
