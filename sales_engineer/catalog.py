from __future__ import annotations

from typing import Any

PRODUCTS = {
    "edge_dns": {
        "name": "Edge DNS",
        "template_heading": "Sobre o Edge DNS",
        "summary": "DNS autoritativo global, resiliente e distribuído na borda.",
        "capabilities": ["DNS autoritativo", "Anycast", "DNSSEC", "zonas primárias e secundárias", "API de gestão"],
    },
    "app_api_protector": {
        "name": "App & API Protector",
        "template_heading": "Sobre o AAP Advanced Delivery",
        "summary": "Proteção de aplicações e APIs com WAF adaptativo e mitigação de DDoS na borda.",
        "capabilities": ["WAF", "proteção de APIs", "Adaptive Security Engine", "DDoS L7", "integração SIEM"],
    },
    "malware_protection": {
        "name": "Malware Protection",
        "template_heading": "Malware Protection",
        "summary": "Inspeção de uploads para reduzir risco de malware em aplicações web.",
        "capabilities": ["análise de arquivos", "políticas por aplicação", "quarentena", "telemetria"],
    },
    "alb": {
        "name": "Application Load Balancer",
        "template_heading": "Application Load Balancer - ALB",
        "summary": "Balanceamento global entre origens com saúde, prioridade e continuidade.",
        "capabilities": ["balanceamento global", "health checks", "failover", "multi-cloud"],
    },
    "gtm": {
        "name": "Global Traffic Management",
        "template_heading": "Global Traffic Management",
        "summary": "Decisão DNS dinâmica para continuidade, distribuição de tráfego e otimização multi-cloud.",
        "capabilities": ["políticas de tráfego", "liveness tests", "failover entre provedores", "balanceamento ponderado", "roteamento por desempenho"],
    },
    "ion": {
        "name": "Ion",
        "template_heading": "Ion",
        "summary": "Entrega e otimização de aplicações web e conteúdo dinâmico na borda.",
        "capabilities": ["aceleração dinâmica", "otimização de protocolo", "offload de origem", "HTTP/3", "integração com medição de experiência"],
    },
    "prolexic": {
        "name": "Prolexic",
        "template_heading": "Prolexic",
        "summary": "Proteção DDoS de infraestrutura para ambientes cloud, on-premises e híbridos.",
        "capabilities": ["mitigação DDoS L3/L4", "scrubbing distribuído", "modelos always-on ou on-demand", "runbooks de resposta", "proteção de origens"],
    },
    "account_protector": {
        "name": "Account Protector",
        "template_heading": "Account Protector",
        "summary": "Detecção de risco e abuso ao longo do ciclo de vida da conta.",
        "capabilities": ["proteção de criação de conta", "risco de login", "perfil comportamental", "detecção de abuso", "sinais de confiança"],
    },
    "ip_accelerator": {
        "name": "IP Accelerator",
        "template_heading": "IP Accelerator",
        "summary": "Aceleração e disponibilidade para aplicações baseadas em TCP/UDP.",
        "capabilities": ["aceleração TCP", "roteamento otimizado", "alta disponibilidade", "origem protegida"],
    },
    "bot_manager": {
        "name": "Bot Manager Premier",
        "template_heading": "BOT Manager Premier - OPCIONAL",
        "summary": "Detecção e resposta a automação maliciosa com controles por objetivo de negócio.",
        "capabilities": ["detecção de bots", "resposta adaptativa", "segmentação", "telemetria"],
    },
}


def product_rows(selected: list[str]) -> list[dict]:
    return [{"id": key, **PRODUCTS[key]} for key in selected if key in PRODUCTS]


PRODUCT_GATING: dict[str, dict[str, list[str]]] = {
    "edge_dns": {
        "include_when": ["DNS autoritativo está no escopo", "resiliência de DNS é um requisito", "DNSSEC ou gestão de zonas é necessária"],
        "exclude_when": ["o cliente apenas possui domínio público", "DNS permanece explicitamente fora do escopo"],
    },
    "app_api_protector": {
        "include_when": ["aplicações web ou APIs públicas precisam de proteção", "há requisito de WAF, segurança de API ou DDoS de aplicação"],
        "exclude_when": ["o escopo não possui aplicação ou API publicada", "o pedido menciona apenas segurança genérica"],
    },
    "bot_manager": {
        "include_when": ["credential stuffing, scraping, criação automatizada de contas ou abuso transacional foi evidenciado"],
        "exclude_when": ["há somente tráfego malicioso genérico", "não existe caso de uso de automação"],
    },
    "malware_protection": {
        "include_when": ["usuários enviam arquivos", "há requisito de inspeção ou bloqueio de malware em uploads"],
        "exclude_when": ["a aplicação apenas entrega conteúdo", "não existe fluxo de upload"],
    },
    "alb": {
        "include_when": ["há múltiplas origens", "roteamento por saúde, active-active, active-passive ou failover é necessário"],
        "exclude_when": ["existe somente uma origem", "alta disponibilidade foi mencionada sem distribuição entre origens"],
    },
    "gtm": {
        "include_when": ["há múltiplos data centers ou provedores", "failover DNS ou continuidade multi-cloud é requisito", "roteamento por saúde ou desempenho é necessário"],
        "exclude_when": ["há uma única origem", "a decisão precisa ocorrer somente após a requisição atingir a borda HTTP"],
    },
    "ion": {
        "include_when": ["há meta de experiência ou latência web", "conteúdo dinâmico ou checkout precisa de otimização", "offload de origem é relevante"],
        "exclude_when": ["não há aplicação web no escopo", "performance não foi ligada a uma jornada mensurável"],
    },
    "prolexic": {
        "include_when": ["há requisito de DDoS volumétrico L3/L4", "links ou IPs de origem precisam de proteção", "continuidade da infraestrutura exposta é requisito"],
        "exclude_when": ["o requisito limita-se a ataques de aplicação L7", "não há ativos de rede ou origens diretamente expostos"],
    },
    "account_protector": {
        "include_when": ["há fraude ou abuso em criação, login, recuperação ou pós-login", "risco por usuário ou conta precisa ser avaliado"],
        "exclude_when": ["o caso se limita a bots sem identidade de conta", "não há jornada autenticada no escopo"],
    },
    "ip_accelerator": {
        "include_when": ["uma aplicação TCP ou UDP não cacheável precisa de otimização ou disponibilidade"],
        "exclude_when": ["o caso se limita a APIs HTTPS", "não há protocolo ou requisito de transporte compatível identificado"],
    },
}

for _product_id, _rules in PRODUCT_GATING.items():
    PRODUCTS[_product_id].update(_rules)


def recommended_product_ids(decisions: list[dict[str, Any]]) -> list[str]:
    return [
        str(item.get("product_id"))
        for item in decisions
        if item.get("status") == "recommended" and item.get("product_id") in PRODUCTS
    ]
