import os
import re
import matplotlib
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

# Register TrueType DejaVuSerif from Matplotlib for 100% Mathematical Unicode Glyph Support in PDF
MPL_FONT_DIR = os.path.join(matplotlib.get_data_path(), 'fonts', 'ttf')
pdfmetrics.registerFont(TTFont('MathSerif', os.path.join(MPL_FONT_DIR, 'DejaVuSerif.ttf')))
pdfmetrics.registerFont(TTFont('MathSerif-Bold', os.path.join(MPL_FONT_DIR, 'DejaVuSerif-Bold.ttf')))
pdfmetrics.registerFont(TTFont('MathSerif-Italic', os.path.join(MPL_FONT_DIR, 'DejaVuSerif-Italic.ttf')))
pdfmetrics.registerFont(TTFont('MathSerif-BoldItalic', os.path.join(MPL_FONT_DIR, 'DejaVuSerif-BoldItalic.ttf')))
registerFontFamily(
    'MathSerif',
    normal='MathSerif',
    bold='MathSerif-Bold',
    italic='MathSerif-Italic',
    boldItalic='MathSerif-BoldItalic'
)

EQ_DIR = r"c:\Users\aaksh\Downloads\paper\nopo_paper_pkg\equations"


def convert_inline_latex_to_tokens(text: str) -> str:
    """
    Convert inline LaTeX math into clean Unicode + structured tokens:
    ⟪SUP:...⟫ for superscripts and ⟪SUB:...⟫ for subscripts.
    Zero raw ^ or _ or \\ characters remain.
    """
    s = text

    # Protect significance stars $**$ and $***$ (no underscores in token name!)
    s = s.replace('$***$', '⟪THREESTARS⟫').replace('$**$', '⟪TWOSTARS⟫')

    # Protect markdown code backticks
    code_spans = []
    def save_code(m):
        code_spans.append(m.group(1))
        return f"⟪CODE{len(code_spans)-1}⟫"
    s = re.sub(r'`([^`]+?)`', save_code, s)

    # Replace \rightleftharpoons FIRST before \right is stripped!
    s = s.replace(r'\rightleftharpoons', '⇄')

    # Strip \left and \right FIRST before \le is replaced!
    s = s.replace(r'\left\|', '‖').replace(r'\right\|', '‖').replace(r'\|', '‖')
    s = s.replace(r'\left', '').replace(r'\right', '').replace(r'\!', '')
    s = s.replace(r'\;', ' ').replace(r'\,', ' ').replace(r'\ ', ' ')
    s = s.replace(r'\qquad', '    ').replace(r'\quad', '  ')

    # Blackboard bold sets (use R inside bold headers, ℝ in regular text)
    s = s.replace(r'\mathbb{R}', 'ℝ').replace(r'\mathbb{E}', 'E')

    # Bold vectors \mathbf{x} -> ⟪BOLD:x⟫ so it never collides with markdown **...**
    s = re.sub(r'\\mathbf\{([^{}]*)\}', r'⟪BOLD:\1⟫', s)
    s = re.sub(r'\\boldsymbol\{\\Sigma\}', '⟪BOLD:Σ⟫', s)
    s = re.sub(r'\\boldsymbol\{([^{}]*)\}', r'⟪BOLD:\1⟫', s)

    # Strip \text{...}, \mathrm{...}, \mathcal{...}
    for _ in range(4):
        for cmd in [r'\\text', r'\\mathrm', r'\\mathcal']:
            s = re.sub(cmd + r'\{([^{}]*)\}', r'\1', s)

    # Handle \hat{...} and \bar{...}
    hat_map = {
        'y': 'ŷ', 'u': 'û', 'x': 'x̂', r'\phi': 'φ̂', 'φ': 'φ̂',
        r'\theta': 'θ̂', 'θ': 'θ̂', '⟪BOLD:\\theta⟫': '⟪BOLD:θ̂⟫', '⟪BOLD:θ⟫': '⟪BOLD:θ̂⟫',
        '⟪BOLD:y⟫': '⟪BOLD:ŷ⟫', '⟪BOLD:u⟫': '⟪BOLD:û⟫'
    }
    def replace_hat(m):
        inner = m.group(1).strip()
        return hat_map.get(inner, f"{inner}̂")
    for _ in range(3):
        s = re.sub(r'\\hat\{([^{}]*)\}', replace_hat, s)
        s = re.sub(r'\\bar\{\\Delta\}', 'Δ̄', s)
        s = re.sub(r'\\bar\{([^{}]*)\}', r'\1̄', s)

    # Replace LaTeX symbol commands BEFORE sub/superscript extraction
    ordered_replacements = [
        (r'\rightarrow', '→'),
        (r'\mapsto', '↦'),
        (r'\infty', '∞'),
        (r'\notin', '∉'),
        (r'\subset', '⊂'),
        (r'\propto', '∝'),
        (r'\approx', '≈'),
        (r'\dots', '...'),
        (r'\sim', '~'),
        (r'\top', 'T'),
        (r'\geq', '≥'),
        (r'\leq', '≤'),
        (r'\ge', '≥'),
        (r'\le', '≤'),
        (r'\ll', '<<'),
        (r'\gg', '>>'),
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
        (r'\theta', 'θ'),
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
        (r'\exp', 'exp'),
        (r'\max', 'max'),
        (r'\min', 'min'),
    ]
    for k, v in ordered_replacements:
        s = s.replace(k, v)

    # Convert braced superscripts ^{...} and subscripts _{...} BEFORE \sqrt and \frac so inner braces are gone!
    s = s.replace('_{L_1}', '⟪SUB:L1⟫').replace('_{\\text{CO}_2}', '⟪SUB:CO2⟫').replace('_{CO_2}', '⟪SUB:CO2⟫')
    s = s.replace('_{a,\\text{nuc}}', '⟪SUB:a,nuc⟫').replace('_{a,nuc}', '⟪SUB:a,nuc⟫')
    s = s.replace('|_{⟪BOLD:x⟫_t}', '|⟪SUB:x,t⟫').replace('|_{\\mathbf{x}_t}', '|⟪SUB:x,t⟫')

    # Replace mathematical superscript star ^* or ^{*} with Unicode math asterisk ∗ so it never triggers *italic* regex
    s = s.replace('^{*}', '⟪SUP:∗⟫').replace('^*', '⟪SUP:∗⟫')

    for _ in range(3):
        s = re.sub(r'\^\{([^{}]*)\}', r'⟪SUP:\1⟫', s)
        s = re.sub(r'_\{([^{}]*)\}', r'⟪SUB:\1⟫', s)

    # Convert unbraced superscripts ^x and subscripts _x
    s = re.sub(r'\^([A-Za-z0-9\+\-∞]+)', r'⟪SUP:\1⟫', s)
    s = re.sub(r'_([A-Za-z0-9,\+\-]+)', r'⟪SUB:\1⟫', s)

    # Now handle inline \sqrt{...} and \frac{...}{...}
    for _ in range(4):
        s = re.sub(r'\\sqrt\{([^{}]*)\}', r'√(\1)', s)
        s = re.sub(r'\\frac\{([^{}]*)\}\{([^{}]*)\}', r'(\1)/(\2)', s)

    # Strip any ⟪BOLD:...⟫ inside ⟪SUP:...⟫ or ⟪SUB:...⟫ so tags never nest inside <super>/<sub>
    s = re.sub(r'⟪SUP:(.*?)⟫', lambda m: '⟪SUP:' + re.sub(r'⟪BOLD:(.*?)⟫', r'\1', m.group(1)) + '⟫', s)
    s = re.sub(r'⟪SUB:(.*?)⟫', lambda m: '⟪SUB:' + re.sub(r'⟪BOLD:(.*?)⟫', r'\1', m.group(1)) + '⟫', s)

    # Convert remaining ⟪BOLD:x⟫ to **x** only if not already inside **...**
    def clean_outer_bold(m):
        inner = re.sub(r'⟪BOLD:(.*?)⟫', r'\1', m.group(1)).replace('ℝ', 'R')
        return f"**{inner}**"
    s = re.sub(r'\*\*(.*?)\*\*', clean_outer_bold, s)
    s = re.sub(r'⟪BOLD:(.*?)⟫', r'**\1**', s)

    # Escaped braces
    s = s.replace(r'\{', '{').replace(r'\}', '}')

    # Strip dollar delimiters
    s = s.replace('$$', '').replace('$', '')

    # Restore code spans
    for idx, c in enumerate(code_spans):
        s = s.replace(f"⟪CODE{idx}⟫", f"`{c}`")

    return s


def tokens_to_rl_xml(raw_text: str) -> str:
    """Convert markdown + ⟪SUP:...⟫ / ⟪SUB:...⟫ tokens into ReportLab Paragraph XML."""
    s = convert_inline_latex_to_tokens(raw_text)
    s = s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    s = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', s)
    s = re.sub(r'\*([^\*]+?)\*', lambda m: '<i>' + m.group(1).replace('ℝ', '<font name="MathSerif">ℝ</font>') + '</i>', s)
    s = re.sub(r'`([^`]+?)`', r'<font name="Courier">\1</font>', s)
    s = re.sub(r'⟪SUP:(.*?)⟫', r'<super>\1</super>', s)
    s = re.sub(r'⟪SUB:(.*?)⟫', r'<sub>\1</sub>', s)
    s = s.replace('⟪THREESTARS⟫', '<b>***</b>').replace('⟪TWOSTARS⟫', '<b>**</b>')
    return s


def add_formatted_runs_docx(paragraph, raw_text: str, base_font_size=10.5, force_bold=False, color_rgb=None):
    """Add Word runs with true superscript, subscript, bold, italic, and code formatting."""
    text = convert_inline_latex_to_tokens(raw_text)
    pattern = r'(\*\*.*?\*\*|\*[^\*]+?\*|`[^`]+?`|⟪SUP:.*?⟫|⟪SUB:.*?⟫)'
    tokens = re.split(pattern, text)
    for tok in tokens:
        if not tok:
            continue
        tok_clean = tok.replace('⟪THREESTARS⟫', '***').replace('⟪TWOSTARS⟫', '**')
        if tok.startswith('⟪SUP:') and tok.endswith('⟫'):
            inner = tok_clean[5:-1].replace('**', '')
            run = paragraph.add_run(inner)
            run.font.superscript = True
            run.font.name = 'Cambria'
            run.font.size = Pt(base_font_size)
            if force_bold:
                run.bold = True
            if color_rgb:
                run.font.color.rgb = color_rgb
        elif tok.startswith('⟪SUB:') and tok.endswith('⟫'):
            inner = tok_clean[5:-1].replace('**', '')
            run = paragraph.add_run(inner)
            run.font.subscript = True
            run.font.name = 'Cambria'
            run.font.size = Pt(base_font_size)
            if force_bold:
                run.bold = True
            if color_rgb:
                run.font.color.rgb = color_rgb
        elif tok.startswith('**') and tok.endswith('**'):
            inner = tok[2:-2]
            if '⟪SUP:' in inner or '⟪SUB:' in inner:
                add_formatted_runs_docx(paragraph, inner, base_font_size=base_font_size, force_bold=True, color_rgb=color_rgb)
            else:
                run = paragraph.add_run(tok_clean[2:-2])
                run.bold = True
                run.font.name = 'Cambria'
                run.font.size = Pt(base_font_size)
                if color_rgb:
                    run.font.color.rgb = color_rgb
        elif tok.startswith('*') and tok.endswith('*'):
            inner = tok[1:-1]
            run = paragraph.add_run(inner.replace('⟪SUP:', '').replace('⟪SUB:', '').replace('⟫', ''))
            run.italic = True
            run.font.name = 'Cambria'
            run.font.size = Pt(base_font_size)
            if force_bold:
                run.bold = True
            if color_rgb:
                run.font.color.rgb = color_rgb
        elif tok.startswith('`') and tok.endswith('`'):
            run = paragraph.add_run(tok_clean[1:-1])
            run.font.name = 'Consolas'
            run.font.size = Pt(base_font_size - 0.5)
        else:
            run = paragraph.add_run(tok_clean)
            run.font.name = 'Cambria'
            run.font.size = Pt(base_font_size)
            if force_bold:
                run.bold = True
            if color_rgb:
                run.font.color.rgb = color_rgb


def set_cell_shading(cell, color_hex: str):
    shading = OxmlElement('w:shd')
    shading.set(qn('w:val'), 'clear')
    shading.set(qn('w:color'), 'auto')
    shading.set(qn('w:fill'), color_hex)
    cell._tc.get_or_add_tcPr().append(shading)


def parse_markdown_blocks(md_path: str):
    with open(md_path, 'r', encoding='utf-8') as f:
        lines = f.read().splitlines()

    blocks = []
    i = 0
    n = len(lines)
    eq_counter = 0
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
            eq_counter += 1
            eq_img = os.path.join(EQ_DIR, f"eq{eq_counter}.png")
            blocks.append(('math', line[2:-2].strip(), eq_img, eq_counter))
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


def build_latex_source(blocks, out_tex: str):
    """Generate a complete, compilable IEEE/academic LaTeX (.tex) manuscript."""
    tex = [
        r"\documentclass[10pt,journal,onecolumn]{IEEEtran}",
        r"\usepackage[utf8]{inputenc}",
        r"\usepackage[T1]{fontenc}",
        r"\usepackage{amsmath,amssymb,amsfonts}",
        r"\usepackage{booktabs}",
        r"\usepackage{tabularx}",
        r"\usepackage{graphicx}",
        r"\usepackage{hyperref}",
        r"\usepackage[margin=0.75in]{geometry}",
        r"\begin{document}",
    ]

    for idx, blk in enumerate(blocks):
        btype = blk[0]
        if btype == 'h1':
            tex.append(f"\\title{{{blk[1]}}}")
            tex.append(r"\author{Aakshay Chordia\\ \textit{Department of Electronics and Communication Engineering, PES University, Bengaluru, India}}")
            tex.append(r"\maketitle")
        elif btype == 'h2':
            title = blk[1]
            if title == 'Abstract':
                continue
            elif title in ('Acknowledgements', 'References'):
                tex.append(f"\\section*{{{title}}}")
            else:
                clean_t = re.sub(r'^\d+\.\s*', '', title)
                tex.append(f"\\section{{{clean_t}}}")
        elif btype == 'h3':
            clean_t = re.sub(r'^\d+\.\d+\s*', '', blk[1])
            tex.append(f"\\subsection{{{clean_t}}}")
        elif btype == 'math':
            tex.append("\\begin{equation}")
            tex.append(blk[1])
            tex.append("\\end{equation}")
        elif btype == 'image':
            cap, path = blk[1], blk[2]
            tex.append("\\begin{figure}[htbp]")
            tex.append("\\centering")
            tex.append(f"\\includegraphics[width=0.92\\textwidth]{{{path}}}")
            tex.append(f"\\caption{{{cap}}}")
            tex.append("\\end{figure}")
        elif btype == 'bullet':
            body = re.sub(r'\*\*(.*?)\*\*', r'\\textbf{\1}', blk[1])
            body = re.sub(r'\*([^\*]+?)\*', r'\\textit{\1}', body)
            tex.append(f"\\noindent $\\bullet$ {body}\\par\\smallskip")
        elif btype == 'numbered':
            body = re.sub(r'\*\*(.*?)\*\*', r'\\textbf{\1}', blk[1])
            body = re.sub(r'\*([^\*]+?)\*', r'\\textit{\1}', body)
            tex.append(f"\\noindent {body}\\par\\smallskip")
        elif btype == 'table':
            rows = blk[1]
            ncols = max(len(r) for r in rows)
            col_spec = "l" + "c" * (ncols - 1)
            tex.append("\\begin{table}[htbp]\\centering\\footnotesize")
            tex.append(f"\\begin{{tabular}}{{{col_spec}}}\\toprule")
            for r_i, row in enumerate(rows):
                cells = []
                for c in row:
                    c_tex = re.sub(r'\*\*(.*?)\*\*', r'\\textbf{\1}', c)
                    c_tex = re.sub(r'\*([^\*]+?)\*', r'\\textit{\1}', c_tex)
                    cells.append(c_tex)
                tex.append(" & ".join(cells) + r" \\")
                if r_i == 0:
                    tex.append(r"\midrule")
            tex.append(r"\bottomrule\end{tabular}\end{table}")
        elif btype == 'p':
            txt = blk[1]
            if idx in (1, 2) and ('Chordia' in txt or 'PES University' in txt):
                continue
            body = re.sub(r'\*\*(.*?)\*\*', r'\\textbf{\1}', txt)
            body = re.sub(r'\*([^\*]+?)\*', r'\\textit{\1}', body)
            if idx == 4:
                tex.append(f"\\begin{{abstract}}\n{body}\n\\end{{abstract}}")
            else:
                tex.append(body + "\n")

    tex.append(r"\end{document}")
    with open(out_tex, 'w', encoding='utf-8') as f:
        f.write("\n".join(tex))
    print(f"Saved LaTeX source: {out_tex} ({os.path.getsize(out_tex):,} bytes)")


def build_docx(blocks, out_docx: str):
    doc = Document()
    for section in doc.sections:
        section.top_margin = Inches(0.75)
        section.bottom_margin = Inches(0.75)
        section.left_margin = Inches(0.75)
        section.right_margin = Inches(0.75)

    table_counter = 0
    for idx, blk in enumerate(blocks):
        btype = blk[0]
        if btype == 'h1':
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.space_after = Pt(8)
            add_formatted_runs_docx(p, blk[1], base_font_size=15.0, force_bold=True, color_rgb=RGBColor(15, 23, 42))
        elif btype == 'h2':
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(12)
            p.paragraph_format.space_after = Pt(4)
            add_formatted_runs_docx(p, blk[1], base_font_size=12.5, force_bold=True, color_rgb=RGBColor(15, 23, 42))
        elif btype == 'h3':
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(9)
            p.paragraph_format.space_after = Pt(3)
            add_formatted_runs_docx(p, blk[1], base_font_size=11.0, force_bold=True, color_rgb=RGBColor(30, 41, 59))
        elif btype == 'math':
            eq_img = blk[2]
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.space_before = Pt(4)
            p.paragraph_format.space_after = Pt(4)
            if os.path.exists(eq_img):
                run = p.add_run()
                run.add_picture(eq_img, width=Inches(6.2))
            else:
                add_formatted_runs_docx(p, blk[1], base_font_size=10.5)
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
            table_counter += 1
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
                        add_formatted_runs_docx(
                            cell_p, val, base_font_size=8.5,
                            force_bold=True, color_rgb=RGBColor(255, 255, 255)
                        )
                    else:
                        if r_i % 2 == 0:
                            set_cell_shading(cell, 'F8FAFC')
                        if table_counter == 8 and c_i == 1 and 1 <= r_i <= 4:
                            sym_img = os.path.join(EQ_DIR, f"sym{r_i}.png")
                            if os.path.exists(sym_img):
                                with PILImage.open(sym_img) as im:
                                    iw, ih = im.size
                                sw_in = min(2.35, iw / 780.0)
                                run = cell_p.add_run()
                                run.add_picture(sym_img, width=Inches(sw_in))
                                continue
                        add_formatted_runs_docx(cell_p, val, base_font_size=8.5)
        elif btype == 'p':
            txt = blk[1]
            p = doc.add_paragraph()
            if idx in (1, 2) and ('Chordia' in txt or 'PES University' in txt):
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                p.paragraph_format.space_after = Pt(4)
                add_formatted_runs_docx(p, txt, base_font_size=10.5)
            elif txt.startswith('**Table ') and ':' in txt[:25]:
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
    canvas.setFont('MathSerif', 8.5)
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
        'PaperTitle', parent=styles['Normal'], fontName='MathSerif-Bold',
        fontSize=13.0, leading=16.8, alignment=TA_CENTER, spaceAfter=8, textColor=colors.HexColor('#0f172a')
    )
    st_author = ParagraphStyle(
        'PaperAuthor', parent=styles['Normal'], fontName='MathSerif',
        fontSize=9.8, leading=13.0, alignment=TA_CENTER, spaceAfter=10, textColor=colors.HexColor('#1e293b')
    )
    st_h2 = ParagraphStyle(
        'PaperH2', parent=styles['Normal'], fontName='MathSerif-Bold',
        fontSize=11.0, leading=14.2, spaceBefore=10, spaceAfter=4, textColor=colors.HexColor('#0f172a')
    )
    st_h3 = ParagraphStyle(
        'PaperH3', parent=styles['Normal'], fontName='MathSerif-Bold',
        fontSize=9.8, leading=13.0, spaceBefore=8, spaceAfter=3, textColor=colors.HexColor('#1e293b')
    )
    st_body = ParagraphStyle(
        'PaperBody', parent=styles['Normal'], fontName='MathSerif',
        fontSize=8.9, leading=12.8, alignment=TA_JUSTIFY, spaceAfter=5
    )
    st_bullet = ParagraphStyle(
        'PaperBullet', parent=styles['Normal'], fontName='MathSerif',
        fontSize=8.7, leading=12.4, leftIndent=14, alignment=TA_JUSTIFY, spaceAfter=3
    )
    st_cap = ParagraphStyle(
        'PaperCap', parent=styles['Normal'], fontName='MathSerif-Italic',
        fontSize=8.0, leading=11.0, alignment=TA_CENTER, spaceBefore=3, spaceAfter=8, textColor=colors.HexColor('#334155')
    )
    st_tbl_title = ParagraphStyle(
        'TblTitle', parent=styles['Normal'], fontName='MathSerif-Bold',
        fontSize=8.5, leading=11.5, spaceBefore=7, spaceAfter=3, textColor=colors.HexColor('#0f172a')
    )
    st_tbl_note = ParagraphStyle(
        'TblNote', parent=styles['Normal'], fontName='MathSerif',
        fontSize=7.3, leading=10.0, alignment=TA_JUSTIFY, spaceBefore=2, spaceAfter=7, textColor=colors.HexColor('#334155')
    )
    st_cell_hdr = ParagraphStyle(
        'CellHdr', parent=styles['Normal'], fontName='MathSerif-Bold',
        fontSize=7.1, leading=9.4, alignment=TA_CENTER, textColor=colors.white
    )
    st_cell = ParagraphStyle(
        'CellBody', parent=styles['Normal'], fontName='MathSerif',
        fontSize=6.9, leading=9.2, alignment=TA_LEFT
    )

    story = []
    max_w = 7.2 * inch
    table_counter = 0

    for idx, blk in enumerate(blocks):
        btype = blk[0]
        if btype == 'h1':
            story.append(Paragraph(tokens_to_rl_xml(blk[1]), st_title))
        elif btype == 'h2':
            story.append(Paragraph(tokens_to_rl_xml(blk[1]), st_h2))
        elif btype == 'h3':
            story.append(Paragraph(tokens_to_rl_xml(blk[1]), st_h3))
        elif btype == 'math':
            eq_img = blk[2]
            if os.path.exists(eq_img):
                with PILImage.open(eq_img) as im:
                    iw, ih = im.size
                disp_w = min(max_w * 0.94, 6.5 * inch)
                disp_h = disp_w * (ih / float(iw))
                story.append(Spacer(1, 3))
                story.append(RLImage(eq_img, width=disp_w, height=disp_h))
                story.append(Spacer(1, 3))
        elif btype in ('bullet', 'numbered'):
            prefix = "• " if btype == 'bullet' else ""
            story.append(Paragraph(tokens_to_rl_xml(prefix + blk[1]), st_bullet))
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
            story.append(Paragraph(tokens_to_rl_xml(cap), st_cap))
        elif btype == 'table':
            table_counter += 1
            rows = blk[1]
            if not rows:
                continue
            ncols = max(len(r) for r in rows)
            rl_rows = []
            for r_i, row in enumerate(rows):
                rl_row = []
                for c_i in range(ncols):
                    val = row[c_i] if c_i < len(row) else ''
                    if r_i == 0:
                        rl_row.append(Paragraph(tokens_to_rl_xml(val), st_cell_hdr))
                    else:
                        if table_counter == 8 and c_i == 1 and 1 <= r_i <= 4:
                            sym_img = os.path.join(EQ_DIR, f"sym{r_i}.png")
                            if os.path.exists(sym_img):
                                with PILImage.open(sym_img) as im:
                                    iw, ih = im.size
                                sw = min(2.30 * inch, (iw / 780.0) * inch)
                                sh = sw * (ih / float(iw))
                                rl_row.append(RLImage(sym_img, width=sw, height=sh))
                                continue
                        rl_row.append(Paragraph(tokens_to_rl_xml(val), st_cell))
                rl_rows.append(rl_row)

            col_w = max_w / ncols
            col_widths = [col_w] * ncols
            if table_counter == 8 and ncols == 5:
                col_widths = [1.20 * inch, 2.40 * inch, 0.75 * inch, 1.25 * inch, 1.60 * inch]
            elif ncols >= 5:
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
                story.append(Paragraph(tokens_to_rl_xml(txt), st_author))
            elif txt.startswith('**Table ') and ':' in txt[:25]:
                story.append(Paragraph(tokens_to_rl_xml(txt), st_tbl_title))
            elif txt.startswith('*Notes*:'):
                story.append(Paragraph(tokens_to_rl_xml(txt), st_tbl_note))
            else:
                story.append(Paragraph(tokens_to_rl_xml(txt), st_body))

    doc.build(story, onFirstPage=add_page_number, onLaterPages=add_page_number)
    print(f"Saved PDF document: {out_pdf} ({os.path.getsize(out_pdf):,} bytes)")


if __name__ == '__main__':
    import shutil
    md_file = r"c:\Users\aaksh\Downloads\paper\HiPCO_KAN_Conference_Paper.md"
    md_v2 = r"c:\Users\aaksh\Downloads\paper\HiPCO_KAN_Conference_Paper_v2.md"
    shutil.copyfile(md_file, md_v2)

    tex_v2 = r"c:\Users\aaksh\Downloads\paper\HiPCO_KAN_Conference_Paper_v2.tex"
    docx_v2 = r"c:\Users\aaksh\Downloads\paper\HiPCO_KAN_Conference_Paper_v2.docx"
    pdf_v2 = r"c:\Users\aaksh\Downloads\paper\HiPCO_KAN_Conference_Paper_v2.pdf"

    parsed_blocks = parse_markdown_blocks(md_file)
    print(f"Parsed {len(parsed_blocks)} structured blocks from {md_file}")
    build_latex_source(parsed_blocks, tex_v2)
    build_docx(parsed_blocks, docx_v2)
    build_pdf(parsed_blocks, pdf_v2)

    for src, dst in [
        (tex_v2, r"c:\Users\aaksh\Downloads\paper\HiPCO_KAN_Conference_Paper.tex"),
        (docx_v2, r"c:\Users\aaksh\Downloads\paper\HiPCO_KAN_Conference_Paper.docx"),
        (pdf_v2, r"c:\Users\aaksh\Downloads\paper\HiPCO_KAN_Conference_Paper.pdf"),
    ]:
        try:
            shutil.copyfile(src, dst)
        except PermissionError:
            print(f"[INFO] {dst} is currently open in another app; saved updated version to {src}")

