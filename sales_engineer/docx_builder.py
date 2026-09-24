from __future__ import annotations

import re
import zipfile
from datetime import datetime
from pathlib import Path
from typing import Any

from docx import Document
from docx.enum.text import WD_BREAK
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from lxml import etree

from .catalog import PRODUCTS


def _normalize(value: str) -> str:
    return re.sub(r"\s+", " ", value.casefold()).strip()


def _replace_runs(paragraph, old: str, new: str) -> None:
    if old not in paragraph.text:
        return
    for run in paragraph.runs:
        if old in run.text:
            run.text = run.text.replace(old, new)


def _replace_paragraph_text(paragraph, new: str) -> None:
    if paragraph.runs:
        paragraph.runs[0].text = new
        for run in paragraph.runs[1:]:
            run.text = ""
    else:
        paragraph.add_run(new)


def _find_heading(doc: Document, contains: str):
    needle = _normalize(contains)
    headings = [
        paragraph
        for paragraph in doc.paragraphs
        if paragraph.style and paragraph.style.name.startswith("Heading")
    ]
    for paragraph in headings:
        label = re.sub(r"^\d+(?:\.\d+)*\s+", "", _normalize(paragraph.text))
        if label == needle:
            return paragraph
    for paragraph in headings:
        if needle in _normalize(paragraph.text):
            return paragraph
    return None


def _next_heading(doc: Document, current):
    seen = False
    for paragraph in doc.paragraphs:
        if paragraph._p is current._p:
            seen = True
            continue
        if seen and paragraph.style and paragraph.style.name.startswith("Heading 1"):
            return paragraph
    return None


def _clear_between(start, end) -> None:
    node = start._p.getnext()
    stop = end._p if end is not None else None
    while node is not None and node is not stop:
        if node.tag == qn("w:sectPr"):
            break
        next_node = node.getnext()
        node.getparent().remove(node)
        node = next_node


def _write_section(doc: Document, heading_contains: str, paragraphs: list[str]) -> None:
    heading = _find_heading(doc, heading_contains)
    if heading is None:
        return
    following = _next_heading(doc, heading)
    if following is None:
        following = doc.add_paragraph()
    _clear_between(heading, following)
    target = following
    for text in paragraphs:
        clean = str(text).strip()
        if not clean:
            continue
        inserted = target.insert_paragraph_before(clean)
        try:
            inserted.style = "Normal0"
        except KeyError:
            inserted.style = "Normal"


def _remove_section(doc: Document, heading_contains: str) -> None:
    heading = _find_heading(doc, heading_contains)
    if heading is None:
        return
    following = _next_heading(doc, heading)
    _clear_between(heading, following)
    heading._p.getparent().remove(heading._p)


def _set_update_fields(doc: Document) -> None:
    settings = doc.settings._element
    node = settings.find(qn("w:updateFields"))
    if node is None:
        node = OxmlElement("w:updateFields")
        settings.append(node)
    node.set(qn("w:val"), "true")


def _section(proposal: dict[str, Any], title: str) -> list[str]:
    for section in proposal.get("sections", []):
        if _normalize(section.get("title", "")) == _normalize(title):
            return [str(item) for item in section.get("paragraphs", [])]
    return []


def _patch_all_xml(path: Path, replacements: dict[str, str]) -> None:
    temp = path.with_suffix(".patching.docx")
    with zipfile.ZipFile(path, "r") as source, zipfile.ZipFile(temp, "w", zipfile.ZIP_DEFLATED) as target:
        for item in source.infolist():
            payload = source.read(item.filename)
            if item.filename.endswith(".xml"):
                text = payload.decode("utf-8", errors="strict")
                def replace_visible(match: re.Match[str]) -> str:
                    visible = match.group(2)
                    for old, new in replacements.items():
                        visible = visible.replace(old, new)
                    return match.group(1) + visible + match.group(3)

                text = re.sub(r"(<w:t(?:\s[^>]*)?>)(.*?)(</w:t>)", replace_visible, text, flags=re.DOTALL)
                # Word may split a visible word across multiple runs. Handle only
                # those cross-run matches here, leaving ordinary run formatting
                # untouched whenever the simple replacement above succeeded.
                root = etree.fromstring(text.encode("utf-8"))
                for paragraph in root.xpath("//*[local-name()='p']"):
                    nodes = paragraph.xpath(".//*[local-name()='t']")
                    if not nodes:
                        continue
                    joined = "".join(node.text or "" for node in nodes)
                    replaced = joined
                    for old, new in replacements.items():
                        if old in replaced:
                            replaced = replaced.replace(old, new)
                    if replaced != joined:
                        nodes[0].text = replaced
                        for node in nodes[1:]:
                            node.text = ""
                text = etree.tostring(root, encoding="unicode")
                # Content controls in the source template are data-bound to the
                # legacy company name in docProps/app.xml. Replace that binding
                # value too, otherwise Word restores the old name when opening.
                for old, new in replacements.items():
                    text = text.replace(old, new)
                payload = text.encode("utf-8")
            target.writestr(item, payload)
    temp.replace(path)


def _repair_template_package(path: Path) -> None:
    ns = {
        "w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main",
        "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
        "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
        "pr": "http://schemas.openxmlformats.org/package/2006/relationships",
    }
    temp = path.with_suffix(".repairing.docx")
    with zipfile.ZipFile(path, "r") as source:
        document = etree.fromstring(source.read("word/document.xml"))
        rels = etree.fromstring(source.read("word/_rels/document.xml.rels"))
        logo_rel_ids = {
            rel.get("Id")
            for rel in rels.xpath("//pr:Relationship", namespaces=ns)
            if str(rel.get("Target", "")).lower().endswith("image9.gif")
        }

        for paragraph in list(document.xpath("//w:p", namespaces=ns)):
            relation_ids = set(paragraph.xpath(".//a:blip/@r:embed", namespaces=ns))
            instructions = " ".join(paragraph.xpath(".//w:instrText/text()", namespaces=ns))
            if (
                relation_ids.intersection(logo_rel_ids)
                or "Logo_CPFL_Energia" in instructions
                or "Logo_NexusPay Brasil S.A._Energia" in instructions
                or "Logo_NexusPay_Energia" in instructions
            ):
                parent = paragraph.getparent()
                if parent is not None:
                    parent.remove(paragraph)

        toc_controls = []
        for control in document.xpath("//w:sdt", namespaces=ns):
            instructions = " ".join(control.xpath(".//w:instrText/text()", namespaces=ns))
            if "PAGEREF" in instructions or " TOC " in f" {instructions} ":
                toc_controls.append(control)
        if toc_controls:
            heading_rows: list[tuple[str, str]] = []
            for paragraph in document.xpath("//w:p", namespaces=ns):
                styles = paragraph.xpath("./w:pPr/w:pStyle/@w:val", namespaces=ns)
                if not styles or styles[0] not in {"Heading1", "Heading2", "Heading3"}:
                    continue
                value = "".join(paragraph.xpath(".//w:t/text()", namespaces=ns)).strip()
                if value:
                    heading_rows.append((styles[0], value))

            content = toc_controls[0].find(qn("w:sdtContent"))
            if content is not None:
                for child in list(content):
                    content.remove(child)

                for index, (source_style, value) in enumerate(heading_rows):
                    row = etree.SubElement(content, qn("w:p"))
                    row_props = etree.SubElement(row, qn("w:pPr"))
                    row_style = etree.SubElement(row_props, qn("w:pStyle"))
                    row_style.set(qn("w:val"), "TOC1" if source_style == "Heading1" else "TOC2")
                    if index == 0:
                        # In this template the first TOC paragraph starts on a new
                        # page. Keep the heading in that same paragraph so Word
                        # cannot orphan it at the foot of the cover.
                        heading_run = etree.SubElement(row, qn("w:r"))
                        heading_run_props = etree.SubElement(heading_run, qn("w:rPr"))
                        etree.SubElement(heading_run_props, qn("w:b"))
                        heading_size = etree.SubElement(heading_run_props, qn("w:sz"))
                        heading_size.set(qn("w:val"), "28")
                        heading_text = etree.SubElement(heading_run, qn("w:t"))
                        heading_text.text = "Sumário"
                        etree.SubElement(heading_run, qn("w:br"))
                    row_run = etree.SubElement(row, qn("w:r"))
                    row_text = etree.SubElement(row_run, qn("w:t"))
                    row_text.text = value

            for extra in toc_controls[1:]:
                parent = extra.getparent()
                if parent is not None:
                    parent.remove(extra)

        first_heading = None
        for paragraph in document.xpath("//w:p", namespaces=ns):
            value = "".join(paragraph.xpath(".//w:t/text()", namespaces=ns)).strip()
            if "Sobre a POPULOS" in value:
                first_heading = paragraph
                break
        if first_heading is not None:
            props = first_heading.find(qn("w:pPr"))
            if props is None:
                props = etree.Element(qn("w:pPr"))
                first_heading.insert(0, props)
            if props.find(qn("w:pageBreakBefore")) is None:
                etree.SubElement(props, qn("w:pageBreakBefore"))
            previous = first_heading.getprevious()
            while previous is not None and previous.tag == qn("w:p") and not "".join(previous.xpath(".//w:t/text()", namespaces=ns)).strip():
                candidate = previous.getprevious()
                previous.getparent().remove(previous)
                previous = candidate

        repaired_document = etree.tostring(document, xml_declaration=True, encoding="UTF-8", standalone="yes")
        with zipfile.ZipFile(temp, "w", zipfile.ZIP_DEFLATED) as target:
            for item in source.infolist():
                payload = repaired_document if item.filename == "word/document.xml" else source.read(item.filename)
                target.writestr(item, payload)
    temp.replace(path)


def build_proposal_docx(template: Path, proposal: dict[str, Any], output: Path) -> Path:
    output.parent.mkdir(parents=True, exist_ok=True)
    doc = Document(template)

    month_names = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]
    for paragraph in doc.paragraphs:
        if paragraph.style and paragraph.style.name == "Title2":
            _replace_paragraph_text(paragraph, proposal["opportunity"])
        elif paragraph.text.strip() == "Maio 2024":
            _replace_paragraph_text(paragraph, f"{month_names[datetime.now().month - 1]} {datetime.now().year}")

    selected_headings = {PRODUCTS[key]["template_heading"] for key in proposal.get("products", []) if key in PRODUCTS}
    for product in PRODUCTS.values():
        if product["template_heading"] not in selected_headings:
            _remove_section(doc, product["template_heading"])
    # Normalize heading text into one run. Some template headings are split into
    # runs that Word occasionally renders with missing glyphs after pagination.
    for paragraph in doc.paragraphs:
        if paragraph.text.strip() in selected_headings:
            _replace_paragraph_text(paragraph, paragraph.text.strip())

    # The source template contains an orphan "Exemplo:" followed by an
    # unavailable linked image immediately before the ALB section.
    orphan_example = next((p for p in doc.paragraphs if p.text.strip() == "Exemplo:"), None)
    alb_heading = _find_heading(doc, "Application Load Balancer - ALB")
    if orphan_example is not None and alb_heading is not None:
        _clear_between(orphan_example, alb_heading)
        orphan_example._p.getparent().remove(orphan_example._p)

    intro = _section(proposal, "Resumo executivo") + _section(proposal, "Objetivos e resultados esperados") + _section(proposal, "Arquitetura proposta")
    scope = _section(proposal, "Escopo de implementação") + _section(proposal, "Abordagem de entrega")
    assumptions = _section(proposal, "Premissas e responsabilidades")
    acceptance = _section(proposal, "Critérios de aceite")

    _write_section(doc, "Introdução a consultoria", intro)
    _write_section(doc, "Escopo definido para a consultoria", scope)
    _write_section(doc, "Premissas, requisitos e restrições", assumptions)
    optional_sections = {
        "Documentação": "Documentação e gestão do projeto",
        "Limites do Escopo Implementação": "Limites e exclusões",
        "Introdução ao Suporte": "Introdução ao suporte",
        "Escopo definido": "Escopo de suporte",
        "SLA e Critérios de Severidade": "SLA e severidades",
        "Garantia": "Garantia",
        "Nota de confidencialidade": "Confidencialidade",
    }
    for template_heading, generated_title in optional_sections.items():
        generated_paragraphs = _section(proposal, generated_title)
        if generated_paragraphs:
            _write_section(doc, template_heading, generated_paragraphs)
    _write_section(doc, "Termo de aceite e conformidade", acceptance)

    # Replace legacy client references before serialization. python-docx exposes
    # the visible paragraph text even when Word split the name across runs.
    for paragraph in doc.paragraphs:
        if "CPFL" in paragraph.text:
            _replace_paragraph_text(paragraph, paragraph.text.replace("CPFL", proposal["client_name"]))

    _set_update_fields(doc)
    doc.save(output)
    _patch_all_xml(
        output,
        {
            "CPFL": proposal["client_name"],
            "∙ CPFL": f"∙ {proposal['client_name']}",
        },
    )
    _repair_template_package(output)
    with zipfile.ZipFile(output, "r") as package:
        if package.testzip() is not None:
            raise RuntimeError("O DOCX gerado contém uma parte corrompida")
    return output
