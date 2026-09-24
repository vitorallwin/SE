from __future__ import annotations

import hashlib
import re
from copy import deepcopy
from datetime import UTC, datetime
from typing import Any

from .ai import GeminiClient
from .catalog import PRODUCTS, product_rows

STAGES = [
    ("discovery", "Discovery"),
    ("architecture", "Arquitetura"),
    ("technical_qa", "QA técnico"),
    ("writing", "Redação"),
    ("commercial_qa", "QA comercial"),
    ("repair", "Reparo"),
    ("document", "Documento"),
]


def now_iso() -> str:
    return datetime.now(UTC).isoformat()


def make_id(client: str) -> str:
    stamp = datetime.now().strftime("%Y%m%d")
    digest = hashlib.sha1(f"{client}-{now_iso()}".encode()).hexdigest()[:7]
    return f"{stamp}-{digest}"


def new_proposal(data: dict[str, Any]) -> dict[str, Any]:
    client = str(data.get("client_name", "")).strip()
    if not client:
        raise ValueError("Nome do cliente é obrigatório")
    created = now_iso()
    selected = [key for key in data.get("products", []) if key in PRODUCTS]
    proposal_id = make_id(client)
    return {
        "id": proposal_id,
        "code": f"PT-{datetime.now().strftime('%y%m')}-{proposal_id[-4:].upper()}",
        "client_name": client,
        "opportunity": str(data.get("opportunity", "Projeto Akamai")).strip() or "Projeto Akamai",
        "owner": str(data.get("owner", "Sales Engineering")).strip() or "Sales Engineering",
        "due_date": data.get("due_date") or "",
        "products": selected,
        "transcript": str(data.get("transcript", "")).strip(),
        "requirements_input": str(data.get("requirements", "")).strip(),
        "scope_input": str(data.get("scope", "")).strip(),
        "assumptions_input": str(data.get("assumptions", "")).strip(),
        "status": "draft",
        "current_stage": "input",
        "progress": 0,
        "quality_score": None,
        "created_at": created,
        "updated_at": created,
        "stages": [
            {"id": key, "label": label, "status": "pending", "started_at": None, "finished_at": None}
            for key, label in STAGES
        ],
        "discovery": {},
        "architecture": {},
        "solution_decisions": [],
        "traceability": [],
        "sections": [],
        "scope": {"included": [], "deliverables": [], "excluded": []},
        "delivery": {"phases": [], "responsibilities": []},
        "assumptions": [],
        "risks": [],
        "acceptance_criteria": [],
        "governance": {
            "warranty": {
                "state": "populos_internal_decision",
                "value": None,
                "source": "placeholder do template [[ N dias a partir do TAD ]]",
            },
            "license_supply": {
                "state": "populos_internal_decision",
                "value": None,
                "source": "decisão comercial da oportunidade",
            },
            "sla": {
                "state": "commitment",
                "value": "tabela institucional do template POPULOS",
                "source": "populos_standard",
            },
        },
        "event_readiness": [],
        "qa": {"technical": [], "commercial": []},
        "open_questions": [],
        "events": [{"at": created, "type": "created", "message": "Proposta criada"}],
        "document": None,
    }


def _sentences(text: str) -> list[str]:
    return [part.strip(" -•\t") for part in re.split(r"[\n\r;]+|(?<=[.!?])\s+", text) if len(part.strip()) > 5]


def _requirement_candidates(proposal: dict[str, Any]) -> list[str]:
    raw = proposal.get("requirements_input", "") or proposal.get("transcript", "")
    rows = _sentences(raw)
    if not rows:
        rows = [
            "Proteger aplicações e APIs publicadas na internet",
            "Aumentar disponibilidade e resiliência do serviço",
            "Dar visibilidade operacional e integrar eventos de segurança",
        ]
    return rows[:12]


def _mark_stage(proposal: dict[str, Any], stage_id: str, status: str) -> None:
    for stage in proposal["stages"]:
        if stage["id"] == stage_id:
            stage["status"] = status
            if status == "running":
                stage["started_at"] = now_iso()
            if status in {"done", "warning", "blocked"}:
                stage["finished_at"] = now_iso()
            break


class Pipeline:
    def __init__(self, ai: GeminiClient):
        self.ai = ai

    def run(self, source: dict[str, Any], through: str | None = None) -> dict[str, Any]:
        proposal = deepcopy(source)
        handlers = {
            "discovery": self.discovery,
            "architecture": self.architecture,
            "technical_qa": self.technical_qa,
            "writing": self.writing,
            "commercial_qa": self.commercial_qa,
            "repair": self.repair,
            "document": self.document_ready,
        }
        for stage_id, _ in STAGES:
            stage_state = next(item for item in proposal["stages"] if item["id"] == stage_id)
            if stage_state["status"] == "done" and stage_id != "document":
                if through == stage_id:
                    break
                continue
            _mark_stage(proposal, stage_id, "running")
            proposal["current_stage"] = stage_id
            try:
                proposal = handlers[stage_id](proposal)
                _mark_stage(proposal, stage_id, "done")
            except Exception as exc:
                _mark_stage(proposal, stage_id, "blocked")
                proposal["status"] = "blocked"
                proposal["events"].append({"at": now_iso(), "type": "error", "message": f"{stage_id}: {exc}"})
                proposal["updated_at"] = now_iso()
                raise
            done = sum(1 for item in proposal["stages"] if item["status"] == "done")
            proposal["progress"] = round(done / len(STAGES) * 100)
            proposal["events"].append({"at": now_iso(), "type": "stage", "message": f"Etapa {stage_id} concluída"})
            if through == stage_id:
                break
        proposal["updated_at"] = now_iso()
        if proposal["progress"] == 100 and proposal.get("status") != "blocked":
            proposal["status"] = "review"
            proposal["current_stage"] = "approval"
        return proposal

    def discovery(self, proposal: dict[str, Any]) -> dict[str, Any]:
        requirements = _requirement_candidates(proposal)
        proposal["discovery"] = {
            "business_goals": requirements[:3],
            "pain_points": _sentences(proposal.get("transcript", ""))[:4],
            "requirements": [
                {"id": f"REQ-{i:02d}", "text": text, "priority": "must", "source": "entrada do usuário"}
                for i, text in enumerate(requirements, 1)
            ],
            "constraints": _sentences(proposal.get("assumptions_input", ""))[:6],
            "confidence": 0.82 if proposal.get("transcript") else 0.67,
        }
        proposal["open_questions"] = []
        if not proposal.get("transcript"):
            proposal["open_questions"].append("Anexar ou colar a ata da reunião para elevar a confiança do Discovery.")
        if not proposal.get("due_date"):
            proposal["open_questions"].append("Confirmar a data desejada para entrega da proposta.")
        return proposal

    def architecture(self, proposal: dict[str, Any]) -> dict[str, Any]:
        selected = list(proposal.get("products", []))
        if not selected:
            source = " ".join(item["text"] for item in proposal["discovery"]["requirements"]).casefold()
            rules = {
                "edge_dns": ("dns", "dnssec", "zona autoritativa"),
                "app_api_protector": ("api", "waf", "ddos", "aplicação web"),
                "bot_manager": ("bot", "credential stuffing", "scraping", "automação"),
                "account_protector": ("fraude de conta", "account takeover", "login", "criação de conta", "onboarding"),
                "malware_protection": ("upload", "arquivo", "malware"),
                "alb": ("múltiplas origens", "multi-cloud", "failover", "balanceamento"),
                "gtm": ("multi-cloud", "failover", "continuidade", "roteamento global"),
                "ion": ("latência", "checkout", "performance", "experiência"),
                "prolexic": ("ddos volumétrico", "infraestrutura", "l3", "l4", "origem exposta"),
                "ip_accelerator": ("tcp", "udp", "ip accelerator", "não cacheável"),
            }
            selected = [key for key, terms in rules.items() if any(term in source for term in terms)]
        if not selected:
            raise ValueError("Nenhum produto pôde ser justificado pelos requisitos informados")
        proposal["products"] = selected
        products = product_rows(selected)
        proposal["solution_decisions"] = [
            {
                "product_id": product["id"],
                "status": "recommended",
                "requirement_ids": [item["id"] for item in proposal["discovery"]["requirements"]],
                "rationale": f"A capacidade {product['name']} foi relacionada aos requisitos fornecidos na entrada.",
                "confidence": 0.65,
                "capabilities": product["capabilities"],
            }
            for product in products
        ]
        proposal["architecture"] = {
            "summary": f"Arquitetura Akamai para {proposal['client_name']} combinando " + ", ".join(p["name"] for p in products) + ".",
            "products": products,
            "flow": ["Usuários", "Akamai Edge", "Aplicações e APIs", "Origens"],
            "principles": ["proteção na borda", "alta disponibilidade", "mudança controlada", "observabilidade e rastreabilidade"],
            "implementation_waves": [
                {"name": "Descoberta e desenho", "duration": "1 semana"},
                {"name": "Configuração e integração", "duration": "2 a 4 semanas"},
                {"name": "Homologação e entrada em produção", "duration": "1 a 2 semanas"},
            ],
        }
        trace = []
        for i, req in enumerate(proposal["discovery"]["requirements"]):
            product = products[i % len(products)]
            trace.append({
                "requirement_id": req["id"],
                "requirement": req["text"],
                "solution": product["name"],
                "evidence": product["summary"],
                "status": "covered",
            })
        proposal["traceability"] = trace
        proposal["acceptance_criteria"] = [
            {
                "requirement_id": item["requirement_id"],
                "criterion": f"Validar em homologação o atendimento de: {item['requirement']}",
                "evidence": "Registro de teste aprovado pelas partes",
                "owner": "POPULOS e Cliente",
            }
            for item in trace
        ]
        return proposal

    def technical_qa(self, proposal: dict[str, Any]) -> dict[str, Any]:
        issues = []
        if proposal["open_questions"]:
            issues.append({"severity": "warning", "message": f"{len(proposal['open_questions'])} pergunta(s) aberta(s) antes da aprovação final."})
        if not proposal["traceability"]:
            issues.append({"severity": "critical", "message": "Nenhum requisito foi rastreado até a solução."})
        requirement_ids = {item.get("id") for item in proposal.get("discovery", {}).get("requirements", [])}
        traced_ids = {item.get("requirement_id") for item in proposal.get("traceability", [])}
        accepted_ids = {item.get("requirement_id") for item in proposal.get("acceptance_criteria", [])}
        missing_trace = sorted(str(item) for item in requirement_ids - traced_ids if item)
        missing_acceptance = sorted(str(item) for item in requirement_ids - accepted_ids if item)
        if missing_trace:
            issues.append({"severity": "critical", "message": f"Requisitos sem rastreabilidade: {', '.join(missing_trace)}."})
        if missing_acceptance:
            issues.append({"severity": "critical", "message": f"Requisitos sem critério de aceite: {', '.join(missing_acceptance)}."})
        decisions = {item.get("product_id"): item for item in proposal.get("solution_decisions", [])}
        if "ddos volumétrico" in " ".join(str(x.get("text", "")) for x in proposal.get("discovery", {}).get("requirements", [])).casefold():
            if decisions.get("prolexic", {}).get("status") not in {"recommended", "optional", "needs_information"}:
                issues.append({"severity": "critical", "message": "DDoS volumétrico sem decisão explícita para proteção de infraestrutura."})
        seasonal = " ".join(
            str(x.get("text", "")) for x in proposal.get("discovery", {}).get("requirements", [])
        ).casefold()
        seasonal += " " + str(proposal.get("transcript", "")).casefold()
        if any(term in seasonal for term in ("black friday", "pix day", "evento crítico", "pico sazonal")):
            if not proposal.get("event_readiness"):
                issues.append({"severity": "critical", "message": "Dor sazonal crítica sem plano de prontidão para o evento."})
        for criterion in proposal.get("acceptance_criteria", []):
            text = str(criterion.get("criterion", "")).casefold()
            if "checkout" in text and re.search(r"\b(até|≤|menor que)\s*\d+\s*(s|segundo|minuto)", text):
                issues.append({"severity": "critical", "message": f"Critério {criterion.get('requirement_id', '')} mede tempo fim a fim fora do controle exclusivo da POPULOS."})
        if not issues:
            issues.append({"severity": "info", "message": "Todos os requisitos estão ligados a uma capacidade técnica."})
        proposal["qa"]["technical"] = issues
        return proposal

    def writing(self, proposal: dict[str, Any]) -> dict[str, Any]:
        if self.ai.configured:
            try:
                generated = self.ai.generate_json(
                    "Você é redator técnico sênior. Responda somente JSON com a chave sections, uma lista de objetos title e paragraphs (lista de strings). Não invente números, SLA ou compromissos. Escreva em português brasileiro, tom consultivo e objetivo.",
                    {
                        "client": proposal["client_name"],
                        "opportunity": proposal["opportunity"],
                        "discovery": proposal["discovery"],
                        "architecture": proposal["architecture"],
                        "scope": proposal.get("scope_input", ""),
                    },
                )
                sections = generated.get("sections", [])
                if isinstance(sections, list) and sections:
                    proposal["sections"] = sections[:10]
                    proposal["ai_used"] = True
                    return proposal
            except Exception as exc:
                proposal["events"].append({"at": now_iso(), "type": "ai_fallback", "message": str(exc)[:300]})

        product_names = ", ".join(item["name"] for item in proposal["architecture"]["products"])
        scope = proposal.get("scope_input") or "configuração, integração, homologação assistida e transferência de conhecimento"
        proposal["sections"] = [
            {
                "title": "Resumo executivo",
                "paragraphs": [
                    f"Esta proposta apresenta a abordagem técnica da POPULOS para apoiar a {proposal['client_name']} na adoção de capacidades Akamai.",
                    f"A solução recomendada combina {product_names}, com implantação controlada, rastreabilidade dos requisitos e validação antes da entrada em produção.",
                ],
            },
            {
                "title": "Objetivos e resultados esperados",
                "paragraphs": [item["text"] for item in proposal["discovery"]["requirements"][:5]],
            },
            {
                "title": "Arquitetura proposta",
                "paragraphs": [proposal["architecture"]["summary"]] + [f"{p['name']}: {p['summary']}" for p in proposal["architecture"]["products"]],
            },
            {
                "title": "Escopo de implementação",
                "paragraphs": [scope, "O detalhamento técnico será validado em reunião de kickoff e registrado no plano de implementação."],
            },
            {
                "title": "Abordagem de entrega",
                "paragraphs": [f"{wave['name']}: duração estimada de {wave['duration']}." for wave in proposal["architecture"]["implementation_waves"]],
            },
            {
                "title": "Premissas e responsabilidades",
                "paragraphs": _sentences(proposal.get("assumptions_input", "")) or ["A contratante fornecerá acessos, contatos técnicos e janelas de mudança necessários à execução.", "Mudanças em produção dependerão de aprovação formal da contratante."],
            },
            {
                "title": "Critérios de aceite",
                "paragraphs": ["Configurações previstas no escopo implantadas e documentadas.", "Testes de homologação executados com evidências registradas.", "Pendências remanescentes formalizadas com responsável e prazo."],
            },
        ]
        proposal["ai_used"] = False
        return proposal

    def commercial_qa(self, proposal: dict[str, Any]) -> dict[str, Any]:
        issues = []
        joined = " ".join(" ".join(section.get("paragraphs", [])) for section in proposal["sections"])
        if len(joined) < 600:
            issues.append({"severity": "warning", "message": "Texto curto; revisar nível de detalhe antes de enviar ao cliente."})
        if "garantimos" in joined.lower():
            issues.append({"severity": "critical", "message": "Remover promessa absoluta não sustentada."})
        forbidden = [term for term in ("ia", "inferido", "demonstrativo", "discovery", "placeholder", "preenchimento") if re.search(rf"\b{term}\b", joined.casefold())]
        if forbidden:
            issues.append({"severity": "critical", "message": f"Vocabulário interno no texto ao cliente: {', '.join(forbidden)}."})
        for key, decision in proposal.get("governance", {}).items():
            if decision.get("state") == "populos_internal_decision" and not decision.get("value"):
                issues.append({"severity": "critical", "message": f"Decisão interna POPULOS não resolvida: {key}."})
        if not issues:
            issues.append({"severity": "info", "message": "Tom, escopo e critérios de aceite estão consistentes."})
        proposal["qa"]["commercial"] = issues
        penalties = sum(18 if issue["severity"] == "critical" else 5 for issue in issues if issue["severity"] != "info")
        proposal["quality_score"] = max(0, 94 - penalties - len(proposal["open_questions"]) * 3)
        return proposal

    def repair(self, proposal: dict[str, Any]) -> dict[str, Any]:
        critical = [issue for group in proposal["qa"].values() for issue in group if issue["severity"] == "critical"]
        if critical:
            proposal["status"] = "blocked"
            proposal["open_questions"].extend(issue["message"] for issue in critical)
        return proposal

    def document_ready(self, proposal: dict[str, Any]) -> dict[str, Any]:
        status = "blocked" if proposal.get("status") == "blocked" else "ready_to_generate"
        proposal["document"] = {"status": status, "generated_at": None, "filename": None}
        return proposal
