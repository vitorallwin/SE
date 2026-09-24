from __future__ import annotations

from pathlib import Path
from typing import Any

from .ai import GeminiClient
from .catalog import PRODUCTS, recommended_product_ids
from .manifest import build_document_manifest
from .neutral_template_builder import build_neutral_template_docx
from .pipeline import Pipeline, STAGES, new_proposal, now_iso
from .skill_loader import load_authoring_skill
from .store import JsonStore


class ProposalService:
    def __init__(self, root: Path):
        self.root = root
        self.store = JsonStore(root / "data" / "proposals")
        self.generated = root / "data" / "generated"
        self.template = root / "assets" / "proposal_neutral_template.docx"
        self.authoring_skill = load_authoring_skill(root)
        self.ai = GeminiClient()
        self.pipeline = Pipeline(self.ai)

    def list(self) -> list[dict[str, Any]]:
        return self.store.list()

    def get(self, proposal_id: str) -> dict[str, Any] | None:
        return self.store.get(proposal_id)

    def create(self, payload: dict[str, Any]) -> dict[str, Any]:
        proposal = new_proposal(payload)
        return self.store.save(proposal)

    def create_ai_demo(self) -> dict[str, Any]:
        if not self.ai.configured:
            raise ValueError("GEMINI_API_KEY não configurada no servidor")

        scenario = self.ai.generate_json(
            """Você é um Sales Engineer sênior especializado em Akamai. Crie um caso de uso empresarial fictício, realista e internamente consistente para demonstrar uma proposta técnica personalizada. Simule uma reunião de discovery completa em português brasileiro, com falas identificadas de cliente e consultoria. Não escolha produtos nesta etapa. Não use empresas reais, dados pessoais reais, preços ou promessas absolutas. Inclua detalhes suficientes para que uma etapa posterior decida quais soluções são necessárias e quais devem ficar de fora. Responda somente JSON com estas chaves: client_name, opportunity, transcript, requirements, scope, assumptions. requirements deve ser uma string com requisitos separados por ponto e vírgula.""",
            {"purpose": "demonstração local sem Supabase e sem infraestrutura cloud", "vendor": "Akamai", "language": "pt-BR"},
        )
        required_scenario = {"client_name", "opportunity", "transcript", "requirements", "scope", "assumptions"}
        if not required_scenario.issubset(scenario):
            raise RuntimeError("A IA não retornou todos os campos do cenário demonstrativo")
        scenario["products"] = []
        scenario["owner"] = "Sales Engineer AI"

        proposal = new_proposal(scenario)
        schema = """{
  "discovery": {"business_goals": [string], "pain_points": [string], "requirements": [{"id":"REQ-01","text":string,"priority":"must|should|could","source":string}], "constraints":[string], "confidence": number},
  "solution_decisions": [{"product_id":string,"status":"recommended|optional|needs_information|excluded","requirement_ids":[string],"rationale":string,"confidence":number,"capabilities":[string]}],
  "architecture": {"summary":string,"flow":[string],"implementation_waves":[{"name":string,"duration":string}]},
  "traceability": [{"requirement_id":string,"requirement":string,"solution":string,"evidence":string,"status":"covered|partial|open"}],
  "sections": [{"title":"Resumo executivo|Operação e suporte","paragraphs":[string]}],
  "scope": {"included":[string],"deliverables":[string],"excluded":[string]},
  "delivery": {"phases":[{"name":string,"objective":string,"outputs":[string],"exit_criteria":string}],"responsibilities":[{"party":string,"responsibility":string}]},
  "assumptions":[string],
  "risks":[{"risk":string,"impact":string,"mitigation":string}],
  "acceptance_criteria":[{"requirement_id":string,"criterion":string,"evidence":string,"owner":string}],
  "qa": {"technical":[{"severity":"info|warning|critical","message":string}],"commercial":[{"severity":"info|warning|critical","message":string}]},
  "open_questions":[string],
  "quality_score": integer,
  "event_readiness": [string]
}"""
        author_prompt = f"""Você é o conjunto de agentes Discovery, Arquiteto de Soluções e Redator Técnico. Gere uma proposta integralmente personalizada sem intervenção humana. Obedeça ao skill abaixo como regra obrigatória. O catálogo é o único universo de produtos permitido. Avalie todos os produtos, mas recomende apenas os sustentados por requisitos; normalmente uma solução conterá um subconjunto do catálogo. Não invente preço, SLA, capacidade, certificação, duração ou garantia. Registre informação ausente em open_questions. Escreva em português brasileiro claro, consultivo e específico para o cliente.

SKILL OBRIGATÓRIO:
{self.authoring_skill}

Responda somente um objeto JSON com a estrutura:
{schema}

Inclua uma decisão para cada produto do catálogo. Somente `recommended` compõe a arquitetura principal. Produza critérios de aceite objetivos e uma rastreabilidade para todos os requisitos. `sections` deve conter Resumo executivo e só deve conter Operação e suporte se suporte fizer parte do escopo."""
        generated = self.ai.generate_json(
            author_prompt,
            {
                "meeting": scenario,
                "catalog": PRODUCTS,
                "document_principle": "o template controla a identidade visual; o manifesto controla quais blocos existem",
            },
        )

        critic_prompt = f"""Você é o agente crítico final de uma proposta Akamai. Audite o rascunho contra o skill e o catálogo. Corrija seleção de produtos sem evidência, rastreabilidade incompleta, escopo genérico, perguntas escondidas, promessas sem fonte e critérios de aceite não mensuráveis. Retorne o objeto completo corrigido, exatamente no mesmo schema. Não acrescente produto apenas para demonstrar o catálogo. É proibido criar percentuais, tempos, QPS, capacidades ou metas numéricas que não estejam literalmente na reunião. Quando não houver baseline, escreva o critério como comparação documentada contra o baseline a ser levantado, sem prometer melhoria mínima. Confidence deve ser decimal entre 0 e 1. Quality score nunca pode ser 100 se houver perguntas abertas ou avisos.

SKILL OBRIGATÓRIO:
{self.authoring_skill}

SCHEMA:
{schema}"""
        generated = self.ai.generate_json(
            critic_prompt,
            {"meeting": scenario, "catalog": PRODUCTS, "draft": generated},
        )

        required_generated = {"discovery", "solution_decisions", "architecture", "traceability", "sections", "scope", "delivery", "assumptions", "risks", "acceptance_criteria", "qa", "open_questions", "quality_score", "event_readiness"}
        if not required_generated.issubset(generated):
            raise RuntimeError("A IA não retornou todos os blocos da proposta")
        decisions = generated.get("solution_decisions", [])
        invalid = [item.get("product_id") for item in decisions if item.get("product_id") not in PRODUCTS]
        if invalid:
            raise RuntimeError(f"A IA selecionou produtos fora do catálogo: {invalid}")
        product_ids = recommended_product_ids(decisions)
        if not product_ids:
            raise RuntimeError("A IA não recomendou nenhuma solução sustentada pelo discovery")
        for item in decisions:
            if item.get("status") == "recommended" and not item.get("requirement_ids"):
                raise RuntimeError(f"Produto recomendado sem requisito: {item.get('product_id')}")
            confidence = float(item.get("confidence", 0))
            item["confidence"] = min(1.0, confidence / 5 if confidence > 1 else confidence)
        if not generated.get("traceability") or len(generated["traceability"]) < len(generated["discovery"].get("requirements", [])):
            raise RuntimeError("A matriz da IA não cobre todos os requisitos")

        proposal.update({key: generated[key] for key in required_generated})
        warning_count = sum(
            1
            for group in proposal.get("qa", {}).values()
            for issue in group
            if issue.get("severity") in {"warning", "critical"}
        )
        proposal["quality_score"] = min(
            int(proposal.get("quality_score", 0)),
            max(0, 95 - len(proposal.get("open_questions", [])) * 4 - warning_count * 3),
        )
        proposal["products"] = product_ids
        proposal["document_manifest"] = build_document_manifest(proposal)
        proposal["ai_used"] = True
        proposal["ai_generation"] = {
            "model": self.ai.model,
            "scenario_generated_by_ai": True,
            "proposal_generated_by_ai": True,
            "critic_generated_by_ai": True,
            "human_content_edits": 0,
            "generated_at": now_iso(),
        }
        finished = now_iso()
        proposal["stages"] = [
            {"id": key, "label": label, "status": "done", "started_at": finished, "finished_at": finished}
            for key, label in STAGES
        ]
        proposal["progress"] = 100
        unresolved_internal = [
            key
            for key, decision in proposal.get("governance", {}).items()
            if decision.get("state") == "populos_internal_decision" and not decision.get("value")
        ]
        if unresolved_internal:
            proposal.setdefault("qa", {}).setdefault("commercial", []).extend(
                {"severity": "critical", "message": f"Decisão interna POPULOS não resolvida: {key}."}
                for key in unresolved_internal
            )
            proposal["status"] = "blocked"
            proposal["current_stage"] = "internal_approval"
            proposal["document"] = {"status": "blocked", "generated_at": None, "filename": None}
        else:
            proposal["status"] = "review"
            proposal["current_stage"] = "approval"
            proposal["document"] = {"status": "ready_to_generate", "generated_at": None, "filename": None}
        proposal["events"].append({"at": finished, "type": "ai_demo", "message": f"Cenário, solução, crítica e manifesto gerados integralmente por {self.ai.model}"})
        proposal["updated_at"] = finished
        return self.store.save(proposal)

    def run(self, proposal_id: str, through: str | None = None) -> dict[str, Any]:
        proposal = self._required(proposal_id)
        result = self.pipeline.run(proposal, through=through)
        return self.store.save(result)

    def update(self, proposal_id: str, payload: dict[str, Any]) -> dict[str, Any]:
        proposal = self._required(proposal_id)
        allowed = {"client_name", "opportunity", "owner", "due_date", "transcript", "requirements_input", "scope_input", "assumptions_input", "products", "open_questions", "sections", "governance"}
        for key in allowed:
            if key in payload:
                proposal[key] = payload[key]
        if "governance" in payload:
            unresolved_internal = [
                key
                for key, decision in proposal.get("governance", {}).items()
                if decision.get("state") == "populos_internal_decision" and not decision.get("value")
            ]
            commercial = proposal.setdefault("qa", {}).setdefault("commercial", [])
            proposal["qa"]["commercial"] = [
                item for item in commercial
                if not str(item.get("message", "")).startswith("Decisão interna POPULOS não resolvida:")
            ]
            proposal["qa"]["commercial"].extend(
                {"severity": "critical", "message": f"Decisão interna POPULOS não resolvida: {key}."}
                for key in unresolved_internal
            )
            other_critical = any(
                issue.get("severity") == "critical"
                for group in proposal.get("qa", {}).values()
                for issue in group
            )
            if not unresolved_internal and not other_critical:
                proposal["status"] = "review"
                proposal["current_stage"] = "approval"
                proposal["document"] = {"status": "ready_to_generate", "generated_at": None, "filename": None}
        proposal["updated_at"] = now_iso()
        proposal["events"].append({"at": now_iso(), "type": "edited", "message": "Proposta atualizada"})
        return self.store.save(proposal)

    def generate_docx(self, proposal_id: str) -> tuple[dict[str, Any], Path]:
        proposal = self._required(proposal_id)
        if not proposal.get("sections"):
            proposal = self.pipeline.run(proposal, through="document")
        unresolved_internal = [
            key
            for key, decision in proposal.get("governance", {}).items()
            if decision.get("state") == "populos_internal_decision" and not decision.get("value")
        ]
        if unresolved_internal:
            raise ValueError(
                "Emissão bloqueada por decisão interna POPULOS: " + ", ".join(unresolved_internal)
            )
        filename = f"{proposal['code']}-{proposal['client_name']}-Akamai.docx"
        safe_name = "".join(ch if ch.isalnum() or ch in "-_." else "-" for ch in filename)
        output = self.generated / safe_name
        manifest = proposal.get("document_manifest") or build_document_manifest(proposal)
        proposal["document_manifest"] = manifest
        build_neutral_template_docx(proposal, self.template, output)
        proposal["document"] = {"status": "generated", "generated_at": now_iso(), "filename": safe_name}
        proposal["events"].append({"at": now_iso(), "type": "document", "message": "DOCX gerado sobre o template neutro aprovado, com blocos condicionais decididos pelo manifesto"})
        proposal["updated_at"] = now_iso()
        self.store.save(proposal)
        return proposal, output

    def approve(self, proposal_id: str, approver: str) -> dict[str, Any]:
        proposal = self._required(proposal_id)
        if not approver.strip():
            raise ValueError("Informe o nome de quem aprova")
        unresolved_internal = [
            key
            for key, decision in proposal.get("governance", {}).items()
            if decision.get("state") == "populos_internal_decision" and not decision.get("value")
        ]
        if unresolved_internal:
            raise ValueError("Aprovação bloqueada por decisão interna POPULOS: " + ", ".join(unresolved_internal))
        proposal["status"] = "approved"
        proposal["approved_by"] = approver.strip()
        proposal["approved_at"] = now_iso()
        proposal["updated_at"] = now_iso()
        proposal["events"].append({"at": now_iso(), "type": "approved", "message": f"Aprovada por {approver.strip()}"})
        return self.store.save(proposal)

    def delete(self, proposal_id: str) -> bool:
        return self.store.delete(proposal_id)

    def _required(self, proposal_id: str) -> dict[str, Any]:
        proposal = self.store.get(proposal_id)
        if proposal is None:
            raise KeyError("Proposta não encontrada")
        return proposal
