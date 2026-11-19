import os
import re
from PIL import Image as PILImage

import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import registerFontFamily
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image as RLImage, Table as RLTable, TableStyle
)

# Register TrueType Times New Roman for full Unicode glyph support in PDF
FONT_DIR = r"C:\Windows\Fonts"
pdfmetrics.registerFont(TTFont('TimesUni', os.path.join(FONT_DIR, 'times.ttf')))
pdfmetrics.registerFont(TTFont('TimesUni-Bold', os.path.join(FONT_DIR, 'timesbd.ttf')))
pdfmetrics.registerFont(TTFont('TimesUni-Italic', os.path.join(FONT_DIR, 'timesi.ttf')))
pdfmetrics.registerFont(TTFont('TimesUni-BoldItalic', os.path.join(FONT_DIR, 'timesbi.ttf')))
registerFontFamily(
    'TimesUni',
    normal='TimesUni',
    bold='TimesUni-Bold',
    italic='TimesUni-Italic',
    boldItalic='TimesUni-BoldItalic'
)


def latex_to_unicode(text: str) -> str:
    """Convert inline and display LaTeX math into clean Unicode with zero leftover LaTeX commands."""
    s = text

    # Protect significance stars $**$ and $***$ before stripping dollars
    s = s.replace('$***$', '⟪THREE_STARS⟫').replace('$**$', '⟪TWO_STARS⟫')

    # 1. Replace multi-character LaTeX commands BEFORE prefix commands (\right, \in, \to)
    ordered_replacements = [
        (r'\rightleftharpoons', '⇌'),
        (r'\rightarrow', '→'),
        (r'\mapsto', '→'),
        (r'\infty', '∞'),
        (r'\notin', '∉'),
        (r'\subset', '⊂'),
        (r'\propto', '∝'),
        (r'\approx', '≈'),
        (r'\dots', '...'),
        (r'\sim', '~'),
        (r'\top', 'ᵀ'),
        (r'\geq', '≥'),
        (r'\leq', '≤'),
        (r'\ge', '≥'),
        (r'\le', '≤'),
        (r'\ll', '≪'),
        (r'\gg', '≫'),
        (r'\pm', '±'),
        (r'\times', '×'),
        (r'\cdot', '·'),
        (r'\nabla', '∇'),
        (r'\partial', '∂'),
        (r'\sum', '∑'),
        (r'\prod', '∏'),
        (r'\Delta', 'Δ'),
        (r'\Sigma', 'Σ'),
        (r'\Phi', 'Φ'),
        (r'\alpha', 'α'),
        (r'\beta', 'β'),
        (r'\gamma', 'γ'),
        (r'\delta', 'δ'),
        (r'\eta', 'η'),
        (r'\lambda', 'λ'),
        (r'\mu', 'μ'),
        (r'\nu', 'ν'),
        (r'\pi', 'π'),
        (r'\rho', 'ρ'),
        (r'\sigma', 'σ'),
        (r'\tau', 'τ'),
        (r'\phi', 'φ'),
        (r'\psi', 'ψ'),
        (r'\omega', 'ω'),
        (r'\in', '∈'),
        (r'\to', '→'),
        (r'^\circ', '°'),
        (r'\%', '%'),
        (r'\$', '$'),
        (r'\left\|', '‖'),
        (r'\right\|', '‖'),
        (r'\|', '‖'),
        (r'\left', ''),
        (r'\right', ''),
        (r'\!', ''),
        (r'\;', ' '),
        (r'\,', ' '),
        (r'\ ', ' '),
        (r'\qquad', '    '),
        (r'\quad', '  '),
        (r'\exp', 'exp'),
        (r'\max', 'max'),
        (r'\min', 'min'),
    ]
    for k, v in ordered_replacements:
        s = s.replace(k, v)

    # 2. Iteratively strip formatting wrappers \text{...}, \mathrm{...}, \mathbf{...}, \mathcal{...}, \mathbb{...}, \boldsymbol{...}
    for _ in range(4):
        for cmd in [r'\\text', r'\\mathrm', r'\\mathbf', r'\\mathcal', r'\\mathbb', r'\\boldsymbol']:
            s = re.sub(cmd + r'\{([^{}]*)\}', r'\1', s)

    # 3. Handle \hat{...} and \bar{...} using precomposed or clean Unicode
    hat_map = {'y': 'ŷ', 'u': 'û', 'x': 'x̂', 'φ': 'φ̂'}
    def replace_hat(m):
        inner = m.group(1).strip()
        return hat_map.get(inner, f"{inner}̂")
    for _ in range(3):
        s = re.sub(r'\\hat\{([^{}]*)\}', replace_hat, s)
        s = re.sub(r'\\bar\{([^{}]*)\}', r'mean(\1)', s)

    # 4. Handle \sqrt{...} and \frac{...}{...} and \underbrace{...}_{...} iteratively (innermost braces first)
    for _ in range(6):
        s = re.sub(r'\\sqrt\{([^{}]*)\}', r'√(\1)', s)
        s = re.sub(r'\\frac\{([^{}]*)\}\{([^{}]*)\}', r'(\1)/(\2)', s)
        s = re.sub(r'\\underbrace\{([^{}]*)\}_\{([^{}]*)\}', r'[\1] (\2)', s)

    # 5. Clean remaining sub/superscripts with braces
    for _ in range(4):
        s = re.sub(r'\^\{([^{}]*)\}', r'^\1', s)
        s = re.sub(r'_\{([^{}]*)\}', r'_\1', s)

    # Handle escaped braces
    s = s.replace(r'\{', '{').replace(r'\}', '}')

    # Strip remaining dollar signs
    s = s.replace('$$', '').replace('$', '')
    return s


def set_cell_shading(cell, color_hex: str):
    shading = OxmlElement('w:shd')
    shading.set(qn('w:val'), 'clear')
    shading.set(qn('w:color'), 'auto')
    shading.set(qn('w:fill'), color_hex)
    cell._tc.get_or_add_tcPr().append(shading)


def add_formatted_runs_docx(paragraph, raw_text: str, base_font_size=10.5):
    """Parse **bold** and *italic* markdown tokens after converting LaTeX math."""
    text = latex_to_unicode(raw_text)
    tokens = re.split(r'(\*\*.*?\*\*|\*[^\*]+?\*|`[^`]+?`)', text)
    for tok in tokens:
        if not tok:
            continue
        tok_clean = tok.replace('⟪THREE_STARS⟫', '***').replace('⟪TWO_STARS⟫', '**')
        if tok.startswith('**') and tok.endswith('**'):
            run = paragraph.add_run(tok_clean[2:-2])
            run.bold = True
        elif tok.startswith('*') and tok.endswith('*'):
            run = paragraph.add_run(tok_clean[1:-1])
            run.italic = True
        elif tok.startswith('`') and tok.endswith('`'):
            run = paragraph.add_run(tok_clean[1:-1])
            run.font.name = 'Consolas'
        else:
            run = paragraph.add_run(tok_clean)
        run.font.size = Pt(base_font_size)
        if not (tok.startswith('`') and tok.endswith('`')):
            run.font.name = 'Times New Roman'


def markdown_to_rl_xml(raw_text: str) -> str:
    """Convert Markdown + LaTeX into ReportLab XML tags."""
    s = latex_to_unicode(raw_text)
    s = s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    s = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', s)
    s = re.sub(r'\*([^\*]+?)\*', r'<i>\1</i>', s)
    s = re.sub(r'`([^`]+?)`', r'<font name="Courier">\1</font>', s)
    s = s.replace('⟪THREE_STARS⟫', '***').replace('⟪TWO_STARS⟫', '**')
    return s


def parse_markdown_blocks(md_path: str):
    with open(md_path, 'r', encoding='utf-8') as f:
        lines = f.read().splitlines()

    blocks = []
    i = 0
    n = len(lines)
    while i < n:
        line = lines[i].strip()
        if not line:
            i += 1
            continue

        img_match = re.match(r'^!\[(.*?)\]\((.*?)\)$', line)
        if img_match:
            blocks.append(('image', img_match.group(1), img_match.group(2)))
            i += 1
            continue

        if line.startswith('$$') and line.endswith('$$') and len(line) > 4:
            blocks.append(('math', line[2:-2].strip()))
            i += 1
            continue

        if line.startswith('|') and i + 1 < n and lines[i + 1].strip().startswith('|'):
            table_rows = []
            while i < n and lines[i].strip().startswith('|'):
                row_str = lines[i].strip()
                if not re.match(r'^\|[\s\:\-\|]+\|$', row_str):
                    cells = [c.strip() for c in row_str.strip('|').split('|')]
                    table_rows.append(cells)
                i += 1
            blocks.append(('table', table_rows))
            continue

        if line.startswith('# '):
            blocks.append(('h1', line[2:].strip()))
            i += 1
            continue
        if line.startswith('## '):
            blocks.append(('h2', line[3:].strip()))
            i += 1
            continue
        if line.startswith('### '):
            blocks.append(('h3', line[4:].strip()))
            i += 1
            continue

        if line.startswith('* '):
            blocks.append(('bullet', line[2:].strip()))
            i += 1
            continue

        num_match = re.match(r'^(\d+)\.\s+(.*)$', line)
        if num_match:
            blocks.append(('numbered', f"{num_match.group(1)}. {num_match.group(2)}"))
            i += 1
            continue

        blocks.append(('p', line))
        i += 1

    return blocks


def build_docx(blocks, out_docx: str):
    doc = Document()
    for section in doc.sections:
        section.top_margin = Inches(0.75)
        section.bottom_margin = Inches(0.75)
        section.left_margin = Inches(0.75)
        section.right_margin = Inches(0.75)

    for idx, blk in enumerate(blocks):
        btype = blk[0]
        if btype == 'h1':
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.space_after = Pt(8)
            run = p.add_run(latex_to_unicode(blk[1]))
            run.bold = True
            run.font.name = 'Times New Roman'
            run.font.size = Pt(15)
            run.font.color.rgb = RGBColor(15, 23, 42)
        elif btype == 'h2':
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(12)
            p.paragraph_format.space_after = Pt(4)
            run = p.add_run(latex_to_unicode(blk[1]))
            run.bold = True
            run.font.name = 'Times New Roman'
            run.font.size = Pt(12.5)
            run.font.color.rgb = RGBColor(15, 23, 42)
        elif btype == 'h3':
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(9)
            p.paragraph_format.space_after = Pt(3)
            run = p.add_run(latex_to_unicode(blk[1]))
            run.bold = True
            run.font.name = 'Times New Roman'
            run.font.size = Pt(11)
            run.font.color.rgb = RGBColor(30, 41, 59)
        elif btype == 'math':
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.space_before = Pt(4)
            p.paragraph_format.space_after = Pt(4)
            run = p.add_run(latex_to_unicode(blk[1]))
            run.italic = True
            run.font.name = 'Times New Roman'
            run.font.size = Pt(10.5)
        elif btype in ('bullet', 'numbered'):
            p = doc.add_paragraph()
            p.paragraph_format.left_indent = Inches(0.25)
            p.paragraph_format.space_before = Pt(2)
            p.paragraph_format.space_after = Pt(2)
            prefix = "• " if btype == 'bullet' else ""
            add_formatted_runs_docx(p, prefix + blk[1], base_font_size=10.0)
        elif btype == 'image':
            cap, img_path = blk[1], blk[2]
            if os.path.exists(img_path):
                p_img = doc.add_paragraph()
                p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
                p_img.paragraph_format.space_before = Pt(8)
                p_img.paragraph_format.space_after = Pt(2)
                run = p_img.add_run()
                run.add_picture(img_path, width=Inches(6.4))
            p_cap = doc.add_paragraph()
            p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_cap.paragraph_format.space_after = Pt(8)
            add_formatted_runs_docx(p_cap, f"*{cap}*", base_font_size=9.2)
        elif btype == 'table':
            rows = blk[1]
            if not rows:
                continue
            ncols = max(len(r) for r in rows)
            table = doc.add_table(rows=len(rows), cols=ncols)
            table.style = 'Table Grid'
            table.alignment = WD_TABLE_ALIGNMENT.CENTER
            for r_i, row in enumerate(rows):
                for c_i in range(ncols):
                    cell = table.cell(r_i, c_i)
                    val = row[c_i] if c_i < len(row) else ''
                    cell_p = cell.paragraphs[0]
                    cell_p.paragraph_format.space_before = Pt(2)
                    cell_p.paragraph_format.space_after = Pt(2)
                    if r_i == 0:
                        set_cell_shading(cell, '1E293B')
                        clean_hdr = latex_to_unicode(val).replace('**', '').replace('⟪THREE_STARS⟫', '***').replace('⟪TWO_STARS⟫', '**')
                        run = cell_p.add_run(clean_hdr)
                        run.bold = True
                        run.font.name = 'Times New Roman'
                        run.font.size = Pt(8.5)
                        run.font.color.rgb = RGBColor(255, 255, 255)
                    else:
                        if r_i % 2 == 0:
                            set_cell_shading(cell, 'F8FAFC')
                        add_formatted_runs_docx(cell_p, val, base_font_size=8.5)
        elif btype == 'p':
            txt = blk[1]
            p = doc.add_paragraph()
            if idx in (1, 2) and ('Chordia' in txt or 'PES University' in txt):
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                p.paragraph_format.space_after = Pt(4)
                add_formatted_runs_docx(p, txt, base_font_size=10.5)
            elif txt.startswith('**Table '):
                p.paragraph_format.space_before = Pt(8)
                p.paragraph_format.space_after = Pt(3)
                add_formatted_runs_docx(p, txt, base_font_size=9.5)
            elif txt.startswith('*Notes*:'):
                p.paragraph_format.space_before = Pt(2)
                p.paragraph_format.space_after = Pt(8)
                add_formatted_runs_docx(p, txt, base_font_size=8.5)
            else:
                p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
                p.paragraph_format.space_before = Pt(2)
                p.paragraph_format.space_after = Pt(5)
                add_formatted_runs_docx(p, txt, base_font_size=10.5)

    doc.save(out_docx)
    print(f"Saved Word document: {out_docx} ({os.path.getsize(out_docx):,} bytes)")


def add_page_number(canvas, doc):
    canvas.saveState()
    canvas.setFont('TimesUni', 9)
    canvas.setFillColor(colors.HexColor('#475569'))
    canvas.drawCentredString(4.25 * inch, 0.45 * inch, f"Page {doc.page}")
    canvas.restoreState()


def build_pdf(blocks, out_pdf: str):
    doc = SimpleDocTemplate(
        out_pdf,
        pagesize=letter,
        leftMargin=0.65 * inch,
        rightMargin=0.65 * inch,
        topMargin=0.65 * inch,
        bottomMargin=0.65 * inch,
    )
    styles = getSampleStyleSheet()
    st_title = ParagraphStyle(
        'PaperTitle', parent=styles['Normal'], fontName='TimesUni-Bold',
        fontSize=14.5, leading=18, alignment=TA_CENTER, spaceAfter=8, textColor=colors.HexColor('#0f172a')
    )
    st_author = ParagraphStyle(
        'PaperAuthor', parent=styles['Normal'], fontName='TimesUni',
        fontSize=10.5, leading=13.5, alignment=TA_CENTER, spaceAfter=10, textColor=colors.HexColor('#1e293b')
    )
    st_h2 = ParagraphStyle(
        'PaperH2', parent=styles['Normal'], fontName='TimesUni-Bold',
        fontSize=12, leading=15, spaceBefore=10, spaceAfter=4, textColor=colors.HexColor('#0f172a')
    )
    st_h3 = ParagraphStyle(
        'PaperH3', parent=styles['Normal'], fontName='TimesUni-Bold',
        fontSize=10.8, leading=13.5, spaceBefore=8, spaceAfter=3, textColor=colors.HexColor('#1e293b')
    )
    st_body = ParagraphStyle(
        'PaperBody', parent=styles['Normal'], fontName='TimesUni',
        fontSize=9.8, leading=13.2, alignment=TA_JUSTIFY, spaceAfter=5
    )
    st_bullet = ParagraphStyle(
        'PaperBullet', parent=styles['Normal'], fontName='TimesUni',
        fontSize=9.5, leading=12.8, leftIndent=14, alignment=TA_JUSTIFY, spaceAfter=3
    )
    st_math = ParagraphStyle(
        'PaperMath', parent=styles['Normal'], fontName='TimesUni-Italic',
        fontSize=9.8, leading=13, alignment=TA_CENTER, spaceBefore=4, spaceAfter=5, textColor=colors.HexColor('#0f172a')
    )
    st_cap = ParagraphStyle(
        'PaperCap', parent=styles['Normal'], fontName='TimesUni-Italic',
        fontSize=8.8, leading=11.5, alignment=TA_CENTER, spaceBefore=3, spaceAfter=8, textColor=colors.HexColor('#334155')
    )
    st_tbl_title = ParagraphStyle(
        'TblTitle', parent=styles['Normal'], fontName='TimesUni-Bold',
        fontSize=9.3, leading=12, spaceBefore=7, spaceAfter=3, textColor=colors.HexColor('#0f172a')
    )
    st_tbl_note = ParagraphStyle(
        'TblNote', parent=styles['Normal'], fontName='TimesUni',
        fontSize=8.0, leading=10.5, alignment=TA_JUSTIFY, spaceBefore=2, spaceAfter=7, textColor=colors.HexColor('#334155')
    )
    st_cell_hdr = ParagraphStyle(
        'CellHdr', parent=styles['Normal'], fontName='TimesUni-Bold',
        fontSize=7.8, leading=9.8, alignment=TA_CENTER, textColor=colors.white
    )
    st_cell = ParagraphStyle(
        'CellBody', parent=styles['Normal'], fontName='TimesUni',
        fontSize=7.6, leading=9.6, alignment=TA_LEFT
    )

    story = []
    max_w = 7.2 * inch

    for idx, blk in enumerate(blocks):
        btype = blk[0]
        if btype == 'h1':
            story.append(Paragraph(markdown_to_rl_xml(blk[1]), st_title))
        elif btype == 'h2':
            story.append(Paragraph(markdown_to_rl_xml(blk[1]), st_h2))
        elif btype == 'h3':
            story.append(Paragraph(markdown_to_rl_xml(blk[1]), st_h3))
        elif btype == 'math':
            story.append(Paragraph(markdown_to_rl_xml(blk[1]), st_math))
        elif btype in ('bullet', 'numbered'):
            prefix = "• " if btype == 'bullet' else ""
            story.append(Paragraph(markdown_to_rl_xml(prefix + blk[1]), st_bullet))
        elif btype == 'image':
            cap, img_path = blk[1], blk[2]
            if os.path.exists(img_path):
                with PILImage.open(img_path) as im:
                    iw, ih = im.size
                disp_w = min(max_w, 6.6 * inch)
                disp_h = disp_w * (ih / float(iw))
                if disp_h > 4.3 * inch:
                    disp_h = 4.3 * inch
                    disp_w = disp_h * (iw / float(ih))
                story.append(Spacer(1, 4))
                story.append(RLImage(img_path, width=disp_w, height=disp_h))
            story.append(Paragraph(markdown_to_rl_xml(cap), st_cap))
        elif btype == 'table':
            rows = blk[1]
            if not rows:
                continue
            ncols = max(len(r) for r in rows)
            rl_rows = []
            for r_i, row in enumerate(rows):
                rl_row = []
                for c_i in range(ncols):
                    val = row[c_i] if c_i < len(row) else ''
                    style = st_cell_hdr if r_i == 0 else st_cell
                    rl_row.append(Paragraph(markdown_to_rl_xml(val), style))
                rl_rows.append(rl_row)
            col_w = max_w / ncols
            col_widths = [col_w] * ncols
            if ncols >= 5:
                col_widths[0] = max_w * 0.24
                rem = (max_w - col_widths[0]) / (ncols - 1)
                for c_i in range(1, ncols):
                    col_widths[c_i] = rem
            t = RLTable(rl_rows, colWidths=col_widths, repeatRows=1)
            t.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e293b')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8fafc')]),
                ('GRID', (0, 0), (-1, -1), 0.4, colors.HexColor('#cbd5e1')),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('TOPPADDING', (0, 0), (-1, -1), 3),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
                ('LEFTPADDING', (0, 0), (-1, -1), 4),
                ('RIGHTPADDING', (0, 0), (-1, -1), 4),
            ]))
            story.append(t)
            story.append(Spacer(1, 3))
        elif btype == 'p':
            txt = blk[1]
            if idx in (1, 2) and ('Chordia' in txt or 'PES University' in txt):
                story.append(Paragraph(markdown_to_rl_xml(txt), st_author))
            elif txt.startswith('**Table '):
                story.append(Paragraph(markdown_to_rl_xml(txt), st_tbl_title))
            elif txt.startswith('*Notes*:'):
                story.append(Paragraph(markdown_to_rl_xml(txt), st_tbl_note))
            else:
                story.append(Paragraph(markdown_to_rl_xml(txt), st_body))

    doc.build(story, onFirstPage=add_page_number, onLaterPages=add_page_number)
    print(f"Saved PDF document: {out_pdf} ({os.path.getsize(out_pdf):,} bytes)")


if __name__ == '__main__':
    md_file = r"c:\Users\aaksh\Downloads\paper\HiPCO_KAN_Conference_Paper.md"
    docx_file = r"c:\Users\aaksh\Downloads\paper\HiPCO_KAN_Conference_Paper.docx"
    pdf_file = r"c:\Users\aaksh\Downloads\paper\HiPCO_KAN_Conference_Paper.pdf"
    parsed_blocks = parse_markdown_blocks(md_file)
    print(f"Parsed {len(parsed_blocks)} structured blocks from {md_file}")
    build_docx(parsed_blocks, docx_file)
    build_pdf(parsed_blocks, pdf_file)
