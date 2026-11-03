#!/usr/bin/env python3
"""
Build script to generate resume.html and resume.pdf from RESUME.md.

Usage:
    uv run build_resume.py          # Generate HTML only
    uv run build_resume.py --pdf    # Generate HTML and PDF

The HTML page matches the retro terminal aesthetic of the site; the PDF uses
a plain print layout. Both render the same parsed structure.

RESUME.md layout the parser understands:

    ## **Name**
    **Headline**
    Location • email • site • github        (contact line, split on "•")
    ### **Section**                         (sections render in file order)

Within a section, each line is classified by its shape rather than by the
section's name, so adding or renaming a section needs no code change:

    **Organization — Role**    starts an entry (a job or project)
    _Place | Dates_            the current entry's place and dates
    - text                     a bullet (inside the current entry, if any)
      - text                   a sub-bullet of the previous bullet
    **Label:** value           a label/value row
    anything else              paragraph text

Inline **bold**, *italic*, _italic_, `code` and [text](url) are rendered.
HTML comments are not rendered.
"""

import argparse
import html
import re
import sys
from pathlib import Path

ENTRY_RE = re.compile(r"\*\*(.+?) — (.+?)\*\*")
PAIR_RE = re.compile(r"\*\*(.+?):\*\*\s*(.+)")
SUB_BULLET_RE = re.compile(r"\s+- (.+)")


def md_links_to_html(text: str) -> str:
    """Convert markdown links [text](url) to 'text: <a href="url">url</a>' format."""
    return re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'\1: <a href="\2">\2</a>', text)


def inline_md(text: str) -> str:
    """Render inline markdown (code, links, bold, italic) as HTML, escaping everything else."""
    text = html.escape(text, quote=False)
    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
    text = md_links_to_html(text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    # Single-character emphasis must not fire inside words (snake_case, 3*4).
    text = re.sub(r"(?<![\w*])\*(?=\S)(.+?)(?<=\S)\*(?![\w*])", r"<em>\1</em>", text)
    text = re.sub(r"(?<!\w)_(?=\S)(.+?)(?<=\S)_(?!\w)", r"<em>\1</em>", text)
    return text


def parse_contact(line: str) -> list[dict]:
    """Split the contact line on "•". Emails become mailto links and bare domains https links."""
    contact = []
    for part in (p.strip() for p in line.split("•")):
        if not part:
            continue
        if "@" in part:
            href = f"mailto:{part}"
        elif "." in part and " " not in part:
            href = f"https://{part}"
        else:
            href = ""
        contact.append({"text": part, "href": href})
    return contact


def current_bullets(section: dict) -> list[dict]:
    """Return the bullet list new bullets belong to: the latest entry's, else the section's."""
    if section["entries"]:
        return section["entries"][-1]["bullets"]
    return section["bullets"]


def parse_resume_md(content: str) -> dict:
    """Parse RESUME.md content into header fields plus an ordered list of sections."""
    content = re.sub(r"<!--.*?-->", "", content, flags=re.DOTALL)
    resume = {"name": "", "title": "", "contact": [], "sections": []}
    section = None
    paragraph_open = False

    for line in content.strip().split("\n"):
        stripped = line.strip()
        if not stripped or stripped == "---":
            paragraph_open = False
            continue
        is_paragraph = False

        if line.startswith("### **"):
            section = {
                "title": stripped.removeprefix("###").replace("**", "").strip(),
                "paragraphs": [],
                "bullets": [],
                "entries": [],
                "pairs": [],
            }
            resume["sections"].append(section)
        elif line.startswith("## **"):
            resume["name"] = stripped.removeprefix("##").replace("**", "").strip()
        elif section is None:
            # Header block between the name and the first section.
            if "•" in stripped:
                resume["contact"] = parse_contact(stripped)
            elif not resume["title"] and stripped.startswith("**"):
                resume["title"] = stripped.replace("**", "").strip()
        elif match := ENTRY_RE.fullmatch(stripped):
            section["entries"].append(
                {"org": match.group(1), "role": match.group(2), "place": "", "dates": "", "bullets": []}
            )
        elif stripped.startswith("_") and stripped.endswith("_") and section["entries"]:
            place, _, dates = stripped.strip("_").partition("|")
            section["entries"][-1]["place"] = place.strip()
            section["entries"][-1]["dates"] = dates.strip()
        elif line.startswith("- "):
            current_bullets(section).append({"text": line[2:].strip(), "children": []})
        elif (match := SUB_BULLET_RE.fullmatch(line)) and current_bullets(section):
            current_bullets(section)[-1]["children"].append(match.group(1).strip())
        elif match := PAIR_RE.fullmatch(stripped):
            section["pairs"].append({"label": match.group(1), "value": match.group(2)})
        else:
            # Consecutive text lines form one paragraph; a blank line starts the next.
            if paragraph_open:
                section["paragraphs"][-1] += " " + stripped
            else:
                section["paragraphs"].append(stripped)
            is_paragraph = True

        paragraph_open = is_paragraph

    return resume


def render_bullets(bullets: list[dict]) -> str:
    """Render bullets, nesting each bullet's sub-bullets in a list of their own."""
    items = []
    for bullet in bullets:
        children = ""
        if bullet["children"]:
            children = (
                '<ul class="bullets">'
                + "".join(f"<li>{inline_md(child)}</li>" for child in bullet["children"])
                + "</ul>"
            )
        items.append(f"<li>{inline_md(bullet['text'])}{children}</li>")
    return '<ul class="bullets">\n' + "\n".join(items) + "\n</ul>"


def render_contact(contact: list[dict]) -> str:
    """Render the contact line, linking the items that have an href."""
    return " | ".join(
        f'<a href="{html.escape(item["href"])}">{html.escape(item["text"])}</a>'
        if item["href"]
        else html.escape(item["text"])
        for item in contact
    )


def render_sections(sections: list[dict]) -> str:
    """Render parsed sections as markup shared by the web and PDF templates.

    Each template styles the same class names, so a new kind of content only
    needs CSS in each template, not a second renderer.
    """
    rendered = []
    for section in sections:
        body = [f'<h2 class="section-title">{html.escape(section["title"])}</h2>']
        body += [f'<p class="section-text">{inline_md(text)}</p>' for text in section["paragraphs"]]
        if section["bullets"]:
            body.append(render_bullets(section["bullets"]))
        for entry in section["entries"]:
            when = " | ".join(part for part in (entry["dates"], entry["place"]) if part)
            bullets = render_bullets(entry["bullets"]) if entry["bullets"] else ""
            body.append(
                '<div class="entry">\n'
                '<div class="entry-header">'
                f'<span class="entry-org">{inline_md(entry["org"])}</span>'
                f'<span class="entry-when">{html.escape(when)}</span>'
                "</div>\n"
                f'<p class="entry-role">{inline_md(entry["role"])}</p>\n'
                f"{bullets}\n"
                "</div>"
            )
        if section["pairs"]:
            rows = "\n".join(
                f'<div class="pair"><span class="pair-label">{inline_md(pair["label"])}:</span> '
                f'<span class="pair-value">{inline_md(pair["value"])}</span></div>'
                for pair in section["pairs"]
            )
            body.append(f'<div class="pairs">\n{rows}\n</div>')
        rendered.append('<section class="section">\n' + "\n".join(body) + "\n</section>")
    return "\n\n".join(rendered)


def generate_html(resume: dict) -> str:
    """Generate the styled HTML resume from the parsed resume."""
    html_doc = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Resume | {html.escape(resume['name'])}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=VT323&family=Fira+Code:wght@300;400;500&display=swap" rel="stylesheet">
    <style>
        :root {{
            --phosphor-green: #33ff33;
            --phosphor-bright: #9dff9d;
            --phosphor-dim: #1a8a1a;
            --phosphor-glow: #00ff0050;
            --terminal-bg: #0a0a0a;
            --scanline-opacity: 0.03;
            --crt-curve: 8px;
        }}

        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        html {{
            font-size: 16px;
        }}

        body {{
            background: #000;
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: flex-start;
            padding: 2rem;
            font-family: 'VT323', monospace;
        }}

        .crt-container {{
            position: relative;
            width: 100%;
            max-width: 900px;
        }}

        .crt-bezel {{
            background: linear-gradient(145deg, #2a2a2a 0%, #1a1a1a 50%, #0f0f0f 100%);
            border-radius: 20px;
            padding: 30px;
            box-shadow:
                0 0 0 4px #333,
                0 0 0 8px #1a1a1a,
                0 20px 60px rgba(0,0,0,0.8),
                inset 0 2px 4px rgba(255,255,255,0.1);
        }}

        .crt-screen {{
            position: relative;
            background: var(--terminal-bg);
            border-radius: var(--crt-curve);
            padding: 2rem;
            overflow: hidden;
            box-shadow:
                inset 0 0 100px rgba(0,255,0,0.05),
                inset 0 0 20px rgba(0,0,0,0.8);
        }}

        .crt-screen::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: repeating-linear-gradient(
                0deg,
                transparent,
                transparent 2px,
                rgba(0,0,0,var(--scanline-opacity)) 2px,
                rgba(0,0,0,var(--scanline-opacity)) 4px
            );
            pointer-events: none;
            z-index: 10;
        }}

        .crt-screen::after {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: radial-gradient(
                ellipse at center,
                transparent 0%,
                rgba(0,0,0,0.3) 90%,
                rgba(0,0,0,0.6) 100%
            );
            pointer-events: none;
            z-index: 11;
        }}

        .terminal-content {{
            position: relative;
            z-index: 5;
            color: var(--phosphor-green);
            text-shadow: 0 0 10px var(--phosphor-glow), 0 0 20px var(--phosphor-glow);
        }}

        .terminal-content a {{
            color: var(--phosphor-green);
            text-decoration: none;
        }}

        .terminal-content a:hover {{
            text-decoration: underline;
        }}

        .terminal-content strong {{
            font-weight: 500;
            color: var(--phosphor-bright);
        }}

        .terminal-content code {{
            font-family: 'Fira Code', monospace;
            border-bottom: 1px dashed var(--phosphor-dim);
        }}

        .crt-screen {{
            animation: flicker 0.15s infinite;
        }}

        @keyframes flicker {{
            0% {{ opacity: 0.97; }}
            50% {{ opacity: 1; }}
            100% {{ opacity: 0.98; }}
        }}

        .back-link {{
            display: inline-flex;
            align-items: center;
            color: var(--phosphor-dim);
            text-decoration: none;
            font-size: 1.1rem;
            margin-bottom: 1.5rem;
            transition: color 0.2s ease;
        }}

        .terminal-content .back-link {{
            color: var(--phosphor-dim);
        }}

        .terminal-content .back-link:hover {{
            color: var(--phosphor-green);
            text-decoration: none;
        }}

        .back-link::before {{
            content: '<';
            margin-right: 0.5rem;
        }}

        .file-header {{
            border-bottom: 1px dashed var(--phosphor-dim);
            padding-bottom: 1rem;
            margin-bottom: 1.5rem;
        }}

        .file-path {{
            color: var(--phosphor-dim);
            font-size: 0.9rem;
            margin-bottom: 0.5rem;
        }}

        .resume-name {{
            font-size: 2.5rem;
            color: var(--phosphor-green);
            margin-bottom: 0.3rem;
        }}

        .resume-title {{
            font-size: 1.3rem;
            color: var(--phosphor-dim);
            margin-bottom: 0.5rem;
        }}

        .resume-contact {{
            font-size: 1rem;
            color: var(--phosphor-dim);
        }}

        .section {{
            margin: 2rem 0;
        }}

        .section-title {{
            font-size: 1.4rem;
            color: var(--phosphor-green);
            margin-bottom: 1rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }}

        .section-title::before {{
            content: '##';
            color: var(--phosphor-dim);
        }}

        .section-text {{
            font-family: 'Fira Code', monospace;
            font-size: 0.9rem;
            line-height: 1.8;
            color: var(--phosphor-green);
            padding-left: 1rem;
            border-left: 2px solid var(--phosphor-dim);
        }}

        .section > .bullets,
        .entry {{
            padding-left: 1rem;
        }}

        .entry {{
            margin-bottom: 1.5rem;
        }}

        .entry-header {{
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            flex-wrap: wrap;
            gap: 0.5rem;
            margin-bottom: 0.5rem;
        }}

        .entry-org {{
            font-size: 1.2rem;
            color: var(--phosphor-green);
        }}

        .entry-when {{
            font-size: 0.9rem;
            color: var(--phosphor-dim);
        }}

        .entry-role {{
            font-size: 1rem;
            color: var(--phosphor-dim);
            margin-bottom: 0.5rem;
        }}

        .bullets {{
            list-style: none;
            font-family: 'Fira Code', monospace;
            font-size: 0.85rem;
            line-height: 1.7;
        }}

        .bullets li {{
            position: relative;
            padding-left: 1.5rem;
            margin-bottom: 0.3rem;
        }}

        .bullets li::before {{
            content: '-';
            position: absolute;
            left: 0;
            color: var(--phosphor-dim);
        }}

        .bullets .bullets {{
            margin-top: 0.3rem;
        }}

        .bullets .bullets li::before {{
            content: '\\00b7';
        }}

        .pairs {{
            display: grid;
            grid-template-columns: auto 1fr;
            gap: 0.5rem 1.5rem;
            font-family: 'Fira Code', monospace;
            font-size: 0.9rem;
            padding-left: 1rem;
        }}

        .pair {{
            display: contents;
        }}

        .pair-label {{
            color: var(--phosphor-dim);
        }}

        .pair-value {{
            color: var(--phosphor-green);
        }}

        .status-bar {{
            display: flex;
            justify-content: space-between;
            margin-top: 2rem;
            padding-top: 1rem;
            border-top: 1px solid var(--phosphor-dim);
            font-size: 0.9rem;
            color: var(--phosphor-dim);
        }}

        .blink {{
            animation: blink 1s infinite;
        }}

        @keyframes blink {{
            0%, 50% {{ opacity: 1; }}
            51%, 100% {{ opacity: 0; }}
        }}

        .power-led {{
            position: absolute;
            bottom: 10px;
            right: 30px;
            width: 8px;
            height: 8px;
            background: var(--phosphor-green);
            border-radius: 50%;
            box-shadow: 0 0 10px var(--phosphor-green);
            animation: led-pulse 2s ease-in-out infinite;
        }}

        @keyframes led-pulse {{
            0%, 100% {{ opacity: 1; }}
            50% {{ opacity: 0.6; }}
        }}

        .bezel-label {{
            position: absolute;
            bottom: 8px;
            left: 30px;
            font-family: 'Fira Code', sans-serif;
            font-size: 0.7rem;
            color: #444;
            letter-spacing: 2px;
        }}

        @media (max-width: 600px) {{
            html {{ font-size: 14px; }}
            body {{ padding: 0.75rem; }}
            .crt-bezel {{ padding: 15px; }}
            .crt-screen {{ padding: 1rem; }}
            .entry-header {{ flex-direction: column; }}
            .pairs {{ grid-template-columns: 1fr; gap: 0.1rem; }}
            .pair-value {{ margin-bottom: 0.5rem; }}
        }}

        @media print {{
            body {{
                background: white;
                padding: 0;
            }}
            .crt-bezel {{
                background: white;
                box-shadow: none;
                padding: 0;
            }}
            .crt-screen {{
                background: white;
                box-shadow: none;
                animation: none;
            }}
            .crt-screen::before,
            .crt-screen::after {{
                display: none;
            }}
            .terminal-content {{
                color: #000;
                text-shadow: none;
            }}
            .back-link,
            .power-led,
            .bezel-label {{
                display: none;
            }}
            :root {{
                --phosphor-green: #000;
                --phosphor-bright: #000;
                --phosphor-dim: #555;
            }}
        }}
    </style>
</head>
<body>
    <div class="crt-container">
        <div class="crt-bezel">
            <div class="crt-screen">
                <div class="terminal-content">
                    <a href="index.html" class="back-link">cd ..</a>

                    <header class="file-header">
                        <div class="file-path">~/documents/resume.txt</div>
                        <h1 class="resume-name">{html.escape(resume['name'])}</h1>
                        <p class="resume-title">{html.escape(resume['title'])}</p>
                        <p class="resume-contact">{render_contact(resume['contact'])}</p>
                    </header>

{render_sections(resume['sections'])}

                    <div class="status-bar">
                        <span>:wq to save and exit</span>
                        <span>EOF<span class="blink">_</span></span>
                    </div>
                </div>
            </div>
            <span class="bezel-label">GORGEGUY</span>
            <span class="power-led"></span>
        </div>
    </div>
</body>
</html>
'''
    return html_doc


def generate_pdf_html(resume: dict) -> str:
    """Generate clean, professional HTML for PDF output."""
    html_doc = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Resume | {html.escape(resume['name'])}</title>
    <style>
        @page {{
            size: letter;
            margin: 0.5in 0.65in;
        }}

        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
            font-size: 9.5pt;
            line-height: 1.35;
            color: #333;
        }}

        header {{
            text-align: center;
            margin-bottom: 16pt;
            padding-bottom: 10pt;
            border-bottom: 2pt solid #333;
        }}

        h1 {{
            font-size: 22pt;
            font-weight: 700;
            margin-bottom: 4pt;
            color: #000;
        }}

        .title {{
            font-size: 12pt;
            color: #555;
            margin-bottom: 4pt;
        }}

        .contact {{
            font-size: 10pt;
            color: #555;
        }}

        a {{
            color: #0066cc;
            text-decoration: none;
        }}

        strong {{
            color: #000;
        }}

        code {{
            font-family: Menlo, Consolas, monospace;
            font-size: 9pt;
        }}

        .section {{
            margin-bottom: 12pt;
        }}

        .section-title {{
            font-size: 12pt;
            font-weight: 700;
            color: #000;
            border-bottom: 1pt solid #ccc;
            padding-bottom: 3pt;
            margin-bottom: 8pt;
            text-transform: uppercase;
            letter-spacing: 0.5pt;
            break-after: avoid;
        }}

        .section-text {{
            font-size: 9.5pt;
            color: #444;
            text-align: justify;
        }}

        .entry {{
            margin-bottom: 10pt;
        }}

        .entry-header {{
            display: flex;
            justify-content: space-between;
            align-items: baseline;
            break-after: avoid;
        }}

        .entry-org {{
            font-weight: 700;
            font-size: 11pt;
            color: #000;
        }}

        .entry-when {{
            font-size: 9pt;
            color: #666;
            white-space: nowrap;
            padding-left: 8pt;
        }}

        .entry-role {{
            font-style: italic;
            color: #555;
            margin-bottom: 4pt;
            break-after: avoid;
        }}

        ul {{
            margin-left: 18pt;
            margin-top: 4pt;
        }}

        ul ul {{
            margin-top: 2pt;
            list-style-type: circle;
        }}

        li {{
            margin-bottom: 2pt;
            break-inside: avoid;
        }}

        .pair {{
            margin-bottom: 3pt;
        }}

        .pair-label {{
            font-weight: 600;
        }}
    </style>
</head>
<body>
    <header>
        <h1>{html.escape(resume['name'])}</h1>
        <div class="title">{html.escape(resume['title'])}</div>
        <div class="contact">{render_contact(resume['contact'])}</div>
    </header>

{render_sections(resume['sections'])}
</body>
</html>
'''
    return html_doc


def generate_pdf(resume: dict, output_path: Path) -> None:
    """Generate PDF from the parsed resume using the print template."""
    try:
        from weasyprint import HTML
    except ImportError:
        print("Error: weasyprint not installed. Run: uv add weasyprint")
        raise SystemExit(1)

    print("Generating professional PDF template...")
    html_content = generate_pdf_html(resume)

    print(f"Writing PDF to {output_path}...")
    HTML(string=html_content).write_pdf(output_path)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Build resume.html and optionally resume.pdf from RESUME.md"
    )
    parser.add_argument(
        "--pdf",
        action="store_true",
        help="Also generate PDF version of the resume",
    )
    parser.add_argument(
        "--pdf-only",
        action="store_true",
        help="Only generate PDF (implies --pdf, skips HTML)",
    )
    args = parser.parse_args()

    script_dir = Path(__file__).parent
    resume_md_path = script_dir / "RESUME.md"
    resume_html_path = script_dir / "resume.html"
    resume_pdf_path = script_dir / "resume.pdf"

    if not resume_md_path.exists():
        print(f"Error: {resume_md_path} not found")
        return 1

    print(f"Reading {resume_md_path}...")
    content = resume_md_path.read_text()

    print("Parsing markdown...")
    resume = parse_resume_md(content)

    print("Generating HTML...")
    html_doc = generate_html(resume)

    if not args.pdf_only:
        print(f"Writing {resume_html_path}...")
        resume_html_path.write_text(html_doc)
        print("Done! resume.html has been generated.")

    if args.pdf or args.pdf_only:
        generate_pdf(resume, resume_pdf_path)
        print("Done! resume.pdf has been generated.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
