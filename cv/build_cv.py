"""Build the CV as .docx and .pdf from the shared content in cv_content.py.

    python3 cv/build_cv.py

Both renderers follow the same ATS-safe rules: one column, no text boxes, no layout
tables around body content, standard headings, and a font that exists on every machine
(Arial in Word, its metric twin Helvetica in the PDF).
"""

import os
import sys

from docx import Document
from docx.enum.section import WD_SECTION
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_TAB_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (
    HRFlowable,
    KeepTogether,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import cv_content as C  # noqa: E402

OUT_DIR = os.path.dirname(os.path.abspath(__file__))
DOCX_PATH = os.path.join(OUT_DIR, "Higor-Mesquita-CV.docx")
PDF_PATH = os.path.join(OUT_DIR, "Higor-Mesquita-CV.pdf")

MARGIN_X = 1.6
MARGIN_Y = 1.3
CONTENT_W_CM = 21.0 - (2 * MARGIN_X)

INK = RGBColor(0x1A, 0x1A, 0x1A)
MUTED = RGBColor(0x44, 0x44, 0x44)
RULE = "999999"

PDF_INK = colors.HexColor("#1A1A1A")
PDF_MUTED = colors.HexColor("#444444")
PDF_RULE = colors.HexColor("#999999")

BODY_PT = 9.5
SMALL_PT = 8.7

# Vertical rhythm, shared by both renderers so the .docx and .pdf stay visually
# identical. Tuned so the page break falls between roles, never inside one.
LEADING_EXTRA = 3.2
BULLET_GAP = 3.4
SKILL_GAP = 4.0
SECTION_BEFORE = 11
SECTION_AFTER = 4
JOB_GAP = 9
CONTEXT_GAP = 3.4

# Bullet geometry in cm, applied identically in both renderers.
BULLET_X = 0.35
BULLET_TEXT_X = 0.85


# --------------------------------------------------------------------------- docx


def _set_normal_style(doc):
    style = doc.styles["Normal"]
    style.font.name = "Arial"
    style.font.size = Pt(BODY_PT)
    style.font.color.rgb = INK
    # Arial must also be declared for the East Asian / complex-script slots, or Word
    # silently substitutes a different face for some glyphs.
    rpr = style.element.get_or_add_rPr()
    rfonts = rpr.get_or_add_rFonts()
    for attr in ("w:ascii", "w:hAnsi", "w:eastAsia", "w:cs"):
        rfonts.set(qn(attr), "Arial")
    pf = style.paragraph_format
    pf.space_before = Pt(0)
    pf.space_after = Pt(0)
    pf.line_spacing = 1.0


def _para(doc, text="", size=BODY_PT, bold=False, italic=False, align=None,
          space_before=0, space_after=0, color=None, left_indent=0, hanging=0):
    p = doc.add_paragraph()
    pf = p.paragraph_format
    pf.space_before = Pt(space_before)
    pf.space_after = Pt(space_after)
    if align is not None:
        p.alignment = align
    if left_indent:
        pf.left_indent = Cm(left_indent)
    if hanging:
        pf.first_line_indent = Cm(-hanging)
    if text:
        run = p.add_run(text)
        run.font.size = Pt(size)
        run.bold = bold
        run.italic = italic
        run.font.color.rgb = color or INK
    return p


def _run(p, text, size=BODY_PT, bold=False, italic=False, color=None):
    run = p.add_run(text)
    run.font.size = Pt(size)
    run.bold = bold
    run.italic = italic
    run.font.color.rgb = color or INK
    return run


def _hyperlink(p, text, url, size=SMALL_PT):
    r_id = p.part.relate_to(
        url,
        "http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink",
        is_external=True,
    )
    link = OxmlElement("w:hyperlink")
    link.set(qn("r:id"), r_id)
    run = OxmlElement("w:r")
    rpr = OxmlElement("w:rPr")
    for tag, val in (("w:color", "1A1A1A"), ("w:sz", str(int(size * 2)))):
        el = OxmlElement(tag)
        el.set(qn("w:val"), val)
        rpr.append(el)
    underline = OxmlElement("w:u")
    underline.set(qn("w:val"), "single")
    rpr.append(underline)
    run.append(rpr)
    t = OxmlElement("w:t")
    t.text = text
    run.append(t)
    link.append(run)
    p._p.append(link)


def _bottom_border(p, color=RULE, size=6):
    ppr = p._p.get_or_add_pPr()
    borders = OxmlElement("w:pBdr")
    bottom = OxmlElement("w:bottom")
    bottom.set(qn("w:val"), "single")
    bottom.set(qn("w:sz"), str(size))
    bottom.set(qn("w:space"), "2")
    bottom.set(qn("w:color"), color)
    borders.append(bottom)
    ppr.append(borders)


def _page_number_field(p, size=SMALL_PT):
    """Insert a live PAGE field so Word renumbers correctly if content shifts."""
    for instr, kind in (("begin", "fldChar"), ("PAGE", "instrText"), ("end", "fldChar")):
        run = OxmlElement("w:r")
        rpr = OxmlElement("w:rPr")
        sz = OxmlElement("w:sz")
        sz.set(qn("w:val"), str(int(size * 2)))
        rpr.append(sz)
        color = OxmlElement("w:color")
        color.set(qn("w:val"), "444444")
        rpr.append(color)
        run.append(rpr)
        el = OxmlElement(f"w:{kind}")
        if kind == "fldChar":
            el.set(qn("w:fldCharType"), instr)
        else:
            el.set(qn("xml:space"), "preserve")
            el.text = instr
        run.append(el)
        p._p.append(run)


def _add_footer(doc):
    footer = doc.sections[0].footer
    p = footer.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    _run(p, f"{C.DISPLAY_NAME}  ·  Page ", size=7.5, color=MUTED)
    _page_number_field(p, size=7.5)


def _keep_block_together(paragraphs):
    """Bind a run of paragraphs so Word does not split them across a page."""
    for p in paragraphs[:-1]:
        p.paragraph_format.keep_with_next = True
    for p in paragraphs:
        p.paragraph_format.keep_together = True


def _section_heading(doc, text, first=False):
    p = _para(doc, text, size=10.5, bold=True,
              space_before=0 if first else SECTION_BEFORE,
              space_after=SECTION_AFTER)
    _bottom_border(p)
    return p


def build_docx():
    doc = Document()
    section = doc.sections[0]
    section.top_margin = Cm(MARGIN_Y)
    section.bottom_margin = Cm(MARGIN_Y)
    section.left_margin = Cm(MARGIN_X)
    section.right_margin = Cm(MARGIN_X)
    _set_normal_style(doc)

    _para(doc, C.NAME, size=18, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=2)
    _para(doc, C.HEADLINE, size=9.2, align=WD_ALIGN_PARAGRAPH.CENTER,
          space_after=3, color=MUTED)
    _para(doc, C.CONTACT_LINE_1, size=SMALL_PT, align=WD_ALIGN_PARAGRAPH.CENTER,
          space_after=1, color=MUTED)

    links = doc.add_paragraph()
    links.alignment = WD_ALIGN_PARAGRAPH.CENTER
    links.paragraph_format.space_after = Pt(2)
    for i, (label, url) in enumerate(C.CONTACT_LINKS):
        if i:
            _run(links, "   ·   ", size=SMALL_PT, color=MUTED)
        _hyperlink(links, label, url)

    _section_heading(doc, "SUMMARY")
    _para(doc, C.SUMMARY, space_after=1)

    _section_heading(doc, "CORE SKILLS")
    for label, text in C.SKILLS:
        p = _para(doc, space_after=SKILL_GAP, left_indent=0.45, hanging=0.45)
        _run(p, f"{label} — ", bold=True)
        _run(p, text)

    _section_heading(doc, "EXPERIENCE")
    for i, job in enumerate(C.EXPERIENCE):
        header = _para(doc, space_before=0 if i == 0 else JOB_GAP, space_after=1)
        header.paragraph_format.tab_stops.add_tab_stop(
            Cm(CONTENT_W_CM), WD_TAB_ALIGNMENT.RIGHT
        )
        _run(header, job["company"], bold=True)
        _run(header, " — ")
        _run(header, job["title"])
        _run(header, "\t")
        _run(header, job["dates"], size=SMALL_PT, color=MUTED)

        context = _para(doc, job["context"], size=SMALL_PT, italic=True,
                        space_after=CONTEXT_GAP, color=MUTED)

        block = [header, context]
        for bullet in job["bullets"]:
            p = _para(doc, space_after=BULLET_GAP, left_indent=BULLET_TEXT_X,
                      hanging=BULLET_TEXT_X - BULLET_X)
            p.paragraph_format.tab_stops.add_tab_stop(
                Cm(BULLET_TEXT_X), WD_TAB_ALIGNMENT.LEFT
            )
            _run(p, "•\t")
            _run(p, bullet)
            block.append(p)
        _keep_block_together(block)

    _section_heading(doc, "EDUCATION")
    for edu in C.EDUCATION:
        p = _para(doc, space_after=1)
        p.paragraph_format.tab_stops.add_tab_stop(
            Cm(CONTENT_W_CM), WD_TAB_ALIGNMENT.RIGHT
        )
        _run(p, edu["degree"], bold=True)
        _run(p, "\t")
        _run(p, edu["dates"], size=SMALL_PT, color=MUTED)
        _para(doc, edu["school"], size=SMALL_PT, italic=True, color=MUTED, space_after=1)

    _section_heading(doc, "LANGUAGES")
    _para(doc, C.LANGUAGES)

    _add_footer(doc)
    doc.save(DOCX_PATH)
    return DOCX_PATH


# ---------------------------------------------------------------------------- pdf


def _pdf_styles():
    base = ParagraphStyle(
        "base", fontName="Helvetica", fontSize=BODY_PT, leading=BODY_PT + LEADING_EXTRA,
        textColor=PDF_INK, spaceBefore=0, spaceAfter=0,
    )
    return {
        "name": ParagraphStyle("name", parent=base, fontName="Helvetica-Bold",
                               fontSize=18, leading=21, alignment=TA_CENTER,
                               spaceAfter=3),
        "headline": ParagraphStyle("headline", parent=base, fontSize=9.2, leading=11.6,
                                   alignment=TA_CENTER, textColor=PDF_MUTED,
                                   spaceAfter=4),
        "contact": ParagraphStyle("contact", parent=base, fontSize=SMALL_PT,
                                  leading=11, alignment=TA_CENTER,
                                  textColor=PDF_MUTED, spaceAfter=1),
        "section": ParagraphStyle("section", parent=base, fontName="Helvetica-Bold",
                                  fontSize=10.5, leading=12.5,
                                  spaceBefore=SECTION_BEFORE, spaceAfter=2),
        "body": ParagraphStyle("body", parent=base),
        "skill": ParagraphStyle("skill", parent=base, leftIndent=0.45 * cm,
                                firstLineIndent=-0.45 * cm, spaceAfter=SKILL_GAP),
        "job": ParagraphStyle("job", parent=base),
        "jobdate": ParagraphStyle("jobdate", parent=base, fontSize=SMALL_PT,
                                  leading=12, alignment=2, textColor=PDF_MUTED),
        "context": ParagraphStyle("context", parent=base, fontSize=SMALL_PT,
                                  leading=10.8, textColor=PDF_MUTED,
                                  spaceAfter=CONTEXT_GAP),
        "bullet": ParagraphStyle("bullet", parent=base, leftIndent=BULLET_TEXT_X * cm,
                                 bulletIndent=BULLET_X * cm, spaceAfter=BULLET_GAP),
        "footer": ParagraphStyle("footer", parent=base, fontSize=7.5, leading=9,
                                 alignment=TA_CENTER, textColor=PDF_MUTED),
    }


def _pdf_section(story, styles, text):
    story.append(Paragraph(text, styles["section"]))
    story.append(HRFlowable(width="100%", thickness=0.6, color=PDF_RULE,
                            spaceBefore=1, spaceAfter=SECTION_AFTER))


def _draw_footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 7.5)
    canvas.setFillColor(PDF_MUTED)
    canvas.drawCentredString(
        A4[0] / 2.0,
        0.75 * cm,
        f"{C.DISPLAY_NAME}  ·  Page {canvas.getPageNumber()}",
    )
    canvas.restoreState()


def build_pdf():
    styles = _pdf_styles()
    doc = SimpleDocTemplate(
        PDF_PATH, pagesize=A4,
        leftMargin=MARGIN_X * cm, rightMargin=MARGIN_X * cm,
        topMargin=MARGIN_Y * cm, bottomMargin=MARGIN_Y * cm,
        title=f"{C.DISPLAY_NAME} — QA Engineer / SDET",
        author=C.DISPLAY_NAME,
        subject="Curriculum Vitae",
    )
    content_w = doc.width

    story = [
        Paragraph(C.NAME, styles["name"]),
        Paragraph(C.HEADLINE, styles["headline"]),
        Paragraph(C.CONTACT_LINE_1, styles["contact"]),
    ]

    linked = "   ·   ".join(
        f'<link href="{url}"><u>{label}</u></link>' for label, url in C.CONTACT_LINKS
    )
    story.append(Paragraph(linked, styles["contact"]))

    _pdf_section(story, styles, "SUMMARY")
    story.append(Paragraph(C.SUMMARY, styles["body"]))

    _pdf_section(story, styles, "CORE SKILLS")
    for label, text in C.SKILLS:
        story.append(Paragraph(f"<b>{label} —</b> {text}", styles["skill"]))

    _pdf_section(story, styles, "EXPERIENCE")
    for i, job in enumerate(C.EXPERIENCE):
        block = []
        if i:
            story.append(Spacer(1, JOB_GAP))
        header = Table(
            [[
                Paragraph(f'<b>{job["company"]}</b> — {job["title"]}', styles["job"]),
                Paragraph(job["dates"], styles["jobdate"]),
            ]],
            colWidths=[content_w * 0.72, content_w * 0.28],
        )
        header.setStyle(TableStyle([
            ("LEFTPADDING", (0, 0), (-1, -1), 0),
            ("RIGHTPADDING", (0, 0), (-1, -1), 0),
            ("TOPPADDING", (0, 0), (-1, -1), 0),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 1),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ]))
        block.append(header)
        block.append(Paragraph(f"<i>{job['context']}</i>", styles["context"]))
        block.extend(
            Paragraph(b, styles["bullet"], bulletText="•") for b in job["bullets"]
        )
        # A role is never split across pages: a reader who sees only page 2 still gets
        # the company, title, and dates above every bullet.
        story.append(KeepTogether(block))

    _pdf_section(story, styles, "EDUCATION")
    for edu in C.EDUCATION:
        row = Table(
            [[
                Paragraph(f'<b>{edu["degree"]}</b>', styles["job"]),
                Paragraph(edu["dates"], styles["jobdate"]),
            ]],
            colWidths=[content_w * 0.78, content_w * 0.22],
        )
        row.setStyle(TableStyle([
            ("LEFTPADDING", (0, 0), (-1, -1), 0),
            ("RIGHTPADDING", (0, 0), (-1, -1), 0),
            ("TOPPADDING", (0, 0), (-1, -1), 0),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 1),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ]))
        story.append(row)
        story.append(Paragraph(f'<i>{edu["school"]}</i>', styles["context"]))

    _pdf_section(story, styles, "LANGUAGES")
    story.append(Paragraph(C.LANGUAGES, styles["body"]))

    doc.build(story, onFirstPage=_draw_footer, onLaterPages=_draw_footer)
    return PDF_PATH


if __name__ == "__main__":
    print(f"docx -> {build_docx()}")
    print(f"pdf  -> {build_pdf()}")
