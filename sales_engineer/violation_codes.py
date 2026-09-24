"""Stable codes for validator messages (auditoria v10, N5).

A code that repeats across executions of different cases points to a limit of the engine; a code that shows
up once points to the author. The report of a round aggregates attempts by code.
"""
from __future__ import annotations

import re

CODES = [
    ("GATE-INSUMO", r"^GATE insumo_insuficiente"),
    ("GATE-CATALOGO", r"^GATE sem_catalogo"),
    ("FORMATO", r"^formato \("),
    ("DECISAO-ABERTA", r"^decisão interna aberta"),
    ("APROVACAO-CITACAO", r"citação|approval_quote|valor aprovado não aparece"),
    ("APROVACAO-CAMPOS", r"aprovação|aprovador|approved_|mode|modo de dado|padrão institucional"),
    ("SLA-APLICACAO", r"sla_applicability|tabela institucional de SLA"),
    ("DATA-SEM-ORIGEM", r"^data \d{2}/\d{2} em texto do cliente"),
    ("VIABILIDADE", r"viabilidade|caminho até o evento|passo do caminho|lead_times|prazo desconhecido|prazo sem origem|congelamento"),
    ("SEMANAS", r"semanas diverge|faixa numérica de semanas|faixa de semanas"),
    ("PRONTIDAO", r"prontidão|plano de evento"),
    ("CONFLITO-PADRAO", r"padrão POPULOS|standard_conflicts|esclarecimento"),
    ("TEXTO-SLOT", r"^document_text\.|front_titles|team_competencies|client_roles|restrictions deve|assessment_items deve|dimensioning deve|Resumo executivo"),
    ("ID-INTERNO", r"identificador interno"),
    ("PRODUTO", r"produto|catálogo|onda"),
    ("COBERTURA", r"cobertura|trecho do insumo|número|requisito"),
    ("ESCOPO", r"escopo|entrega contratada|opcional|critério"),
]
_COMPILED = [(code, re.compile(pattern, re.IGNORECASE)) for code, pattern in CODES]


def code_of(message: str) -> str:
    for code, pattern in _COMPILED:
        if pattern.search(message):
            return code
    return "OUTRO"
