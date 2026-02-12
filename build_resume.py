#!/usr/bin/env python3
"""
Build script to generate resume.html and resume.pdf from RESUME.md.

Usage:
    uv run build_resume.py          # Generate HTML only
    uv run build_resume.py --pdf    # Generate HTML and PDF

This parses RESUME.md and generates a styled HTML resume page
matching the retro terminal aesthetic of the site.
"""

import argparse
import re
from pathlib import Path


def md_links_to_html(text: str) -> str:
    """Convert markdown links [text](url) to 'text: <a href="url">url</a>' format."""
    return re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'\1: <a href="\2">\2</a>', text)


def parse_resume_md(content: str) -> dict:
    """Parse RESUME.md content into structured sections."""
    sections = {
        "name": "",
        "title": "",
        "location": "",
        "email": "",
        "summary": "",
        "experience": [],
        "projects": [],
        "education": "",
        "skills": {},
        "patents": [],
        "current_focus": "",
    }

    lines = content.strip().split("\n")
    current_section = None
    current_job = None
    current_project = None
    buffer = []

    for line in lines:
        # Parse header info
        if line.startswith("## **") and "**" in line[5:]:
            sections["name"] = line.replace("## **", "").replace("**", "").strip()
        elif line.startswith("**Software Engineer**"):
            sections["title"] = "Software Engineer"
        elif "jon@gorgeguy.com" in line:
            parts = line.split("•")
            if len(parts) >= 1:
                sections["location"] = parts[0].strip()
            sections["email"] = "jon@gorgeguy.com"

        # Detect section headers
        elif line.startswith("### **"):
            section_name = line.replace("### **", "").replace("**", "").strip().lower()
            current_section = section_name
            if current_job:
                sections["experience"].append(current_job)
                current_job = None
            if current_project:
                sections["projects"].append(current_project)
                current_project = None
            buffer = []

        # Parse content based on current section
        elif current_section == "summary":
            if line.strip() and not line.startswith("---"):
                sections["summary"] += line.strip() + " "

        elif current_section == "experience":
            # Job header: **Company — Title**
            if line.startswith("**") and "—" in line:
                if current_job:
                    sections["experience"].append(current_job)
                match = re.match(r"\*\*(.+?) — (.+?)\*\*", line)
                if match:
                    current_job = {
                        "company": match.group(1),
                        "title": match.group(2),
                        "dates": "",
                        "location": "",
                        "duties": [],
                    }
            # Date/location line: _Location | Dates_
            elif line.startswith("_") and current_job:
                date_loc = line.strip("_").strip()
                if "|" in date_loc:
                    parts = date_loc.split("|")
                    current_job["location"] = parts[0].strip()
                    current_job["dates"] = parts[1].strip()
            # Duty bullet point
            elif line.startswith("- ") and current_job:
                current_job["duties"].append(line[2:].strip())

        elif current_section == "projects":
            # Project header: **Project Name — Description**
            if line.startswith("**") and "—" in line:
                if current_project:
                    sections["projects"].append(current_project)
                match = re.match(r"\*\*(.+?) — (.+?)\*\*", line)
                if match:
                    current_project = {
                        "name": match.group(1),
                        "description": match.group(2),
                        "subtitle": "",
                        "bullets": [],
                    }
            # Subtitle line: _AI-Accelerated Development | Nov–Dec 2025_
            elif line.startswith("_") and current_project:
                current_project["subtitle"] = line.strip("_").strip()
            # Bullet point
            elif line.startswith("- ") and current_project:
                current_project["bullets"].append(line[2:].strip())

        elif current_section == "education":
            if line.startswith("**"):
                sections["education"] = line.replace("**", "").strip()

        elif current_section == "skills":
            if line.startswith("**") and ":" in line:
                match = re.match(r"\*\*(.+?):\*\*\s*(.+)", line)
                if match:
                    sections["skills"][match.group(1)] = match.group(2)

        elif current_section == "patents":
            if line.startswith("- *"):
                match = re.match(r"- \*(.+?)\* — (.+)", line)
                if match:
                    sections["patents"].append(
                        {"number": match.group(1), "title": match.group(2)}
                    )

        elif current_section == "current focus":
            if line.strip() and not line.startswith("---"):
                sections["current_focus"] += line.strip() + " "

    # Don't forget the last job or project
    if current_job:
        sections["experience"].append(current_job)
    if current_project:
        sections["projects"].append(current_project)

    # Clean up whitespace
    sections["summary"] = sections["summary"].strip()
    sections["current_focus"] = sections["current_focus"].strip()

    return sections


def generate_html(sections: dict) -> str:
    """Generate the styled HTML resume from parsed sections."""

    # Generate experience HTML
    experience_html = ""
    for job in sections["experience"]:
        duties_html = "\n".join(
            f"                                <li>{md_links_to_html(duty)}</li>" for duty in job["duties"]
        )
        experience_html += f"""
                        <div class="job">
                            <div class="job-header">
                                <span class="job-company">{job['company']}</span>
                                <span class="job-dates">{job['dates']} | {job['location']}</span>
                            </div>
                            <p class="job-title">{job['title']}</p>
                            <ul class="job-duties">
{duties_html}
                            </ul>
                        </div>
"""

    # Generate projects HTML
    projects_html = ""
    for project in sections["projects"]:
        bullets_html = "\n".join(
            f"                                <li>{md_links_to_html(bullet)}</li>" for bullet in project["bullets"]
        )
        projects_html += f"""
                        <div class="project">
                            <div class="project-header">
                                <span class="project-name">{project['name']}</span>
                                <span class="project-subtitle">{project['subtitle']}</span>
                            </div>
                            <p class="project-description">{project['description']}</p>
                            <ul class="project-bullets">
{bullets_html}
                            </ul>
                        </div>
"""

    # Generate skills HTML
    skills_html = ""
    for label, value in sections["skills"].items():
        skills_html += f"""                            <span class="skill-label">{label}:</span>
                            <span class="skill-value">{value}</span>

"""

    # Generate patents HTML
    patents_html = ""
    for patent in sections["patents"]:
        patents_html += f"""                            <li>
                                <span class="patent-number">{patent['number']}</span>
                                <span class="patent-title">— {patent['title']}</span>
                            </li>
"""

    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Resume | {sections['name']}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=VT323&family=Fira+Code:wght@300;400;500&display=swap" rel="stylesheet">
    <style>
        :root {{
            --phosphor-green: #33ff33;
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

        .back-link:hover {{
            color: var(--phosphor-green);
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

        .resume-contact a {{
            color: var(--phosphor-green);
            text-decoration: none;
        }}

        .resume-contact a:hover {{
            text-decoration: underline;
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

        .summary-text {{
            font-family: 'Fira Code', monospace;
            font-size: 0.9rem;
            line-height: 1.8;
            color: var(--phosphor-green);
            padding-left: 1rem;
            border-left: 2px solid var(--phosphor-dim);
        }}

        .job {{
            margin-bottom: 1.5rem;
            padding-left: 1rem;
        }}

        .job-header {{
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            flex-wrap: wrap;
            gap: 0.5rem;
            margin-bottom: 0.5rem;
        }}

        .job-company {{
            font-size: 1.2rem;
            color: var(--phosphor-green);
        }}

        .job-dates {{
            font-size: 0.9rem;
            color: var(--phosphor-dim);
        }}

        .job-title {{
            font-size: 1rem;
            color: var(--phosphor-dim);
            margin-bottom: 0.5rem;
        }}

        .job-duties {{
            list-style: none;
            font-family: 'Fira Code', monospace;
            font-size: 0.85rem;
            line-height: 1.7;
        }}

        .job-duties li {{
            position: relative;
            padding-left: 1.5rem;
            margin-bottom: 0.3rem;
        }}

        .job-duties li::before {{
            content: '-';
            position: absolute;
            left: 0;
            color: var(--phosphor-dim);
        }}

        .project {{
            margin-bottom: 1.5rem;
            padding-left: 1rem;
        }}

        .project-header {{
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            flex-wrap: wrap;
            gap: 0.5rem;
            margin-bottom: 0.5rem;
        }}

        .project-name {{
            font-size: 1.2rem;
            color: var(--phosphor-green);
        }}

        .project-subtitle {{
            font-size: 0.9rem;
            color: var(--phosphor-dim);
        }}

        .project-description {{
            font-size: 1rem;
            color: var(--phosphor-dim);
            margin-bottom: 0.5rem;
        }}

        .project-bullets {{
            list-style: none;
            font-family: 'Fira Code', monospace;
            font-size: 0.85rem;
            line-height: 1.7;
        }}

        .project-bullets li {{
            position: relative;
            padding-left: 1.5rem;
            margin-bottom: 0.3rem;
        }}

        .project-bullets li::before {{
            content: '-';
            position: absolute;
            left: 0;
            color: var(--phosphor-dim);
        }}

        .project-bullets a {{
            color: var(--phosphor-green);
            text-decoration: none;
        }}

        .project-bullets a:hover {{
            text-decoration: underline;
        }}

        .skills-grid {{
            display: grid;
            grid-template-columns: auto 1fr;
            gap: 0.5rem 1.5rem;
            font-family: 'Fira Code', monospace;
            font-size: 0.9rem;
            padding-left: 1rem;
        }}

        .skill-label {{
            color: var(--phosphor-dim);
        }}

        .skill-value {{
            color: var(--phosphor-green);
        }}

        .patents-list {{
            list-style: none;
            padding-left: 1rem;
            font-family: 'Fira Code', monospace;
            font-size: 0.9rem;
        }}

        .patents-list li {{
            margin-bottom: 0.5rem;
            display: flex;
            gap: 0.5rem;
        }}

        .patent-number {{
            color: var(--phosphor-green);
        }}

        .patent-title {{
            color: var(--phosphor-dim);
        }}

        .education-item {{
            padding-left: 1rem;
            font-family: 'Fira Code', monospace;
            font-size: 0.95rem;
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
            .crt-bezel {{ padding: 15px; }}
            .crt-screen {{ padding: 1rem; }}
            .job-header {{ flex-direction: column; }}
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
                        <h1 class="resume-name">{sections['name']}</h1>
                        <p class="resume-title">{sections['title']}</p>
                        <p class="resume-contact">
                            {sections['location']} |
                            <a href="mailto:{sections['email']}">{sections['email']}</a>
                        </p>
                    </header>

                    <section class="section">
                        <h2 class="section-title">Summary</h2>
                        <p class="summary-text">
                            {sections['summary']}
                        </p>
                    </section>

                    <section class="section">
                        <h2 class="section-title">Experience</h2>
{experience_html}
                    </section>

                    <section class="section">
                        <h2 class="section-title">Projects</h2>
{projects_html}
                    </section>

                    <section class="section">
                        <h2 class="section-title">Skills</h2>
                        <div class="skills-grid">
{skills_html.rstrip()}
                        </div>
                    </section>

                    <section class="section">
                        <h2 class="section-title">Patents</h2>
                        <ul class="patents-list">
{patents_html.rstrip()}
                        </ul>
                    </section>

                    <section class="section">
                        <h2 class="section-title">Education</h2>
                        <p class="education-item">{sections['education']}</p>
                    </section>

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
    return html


def generate_pdf_html(sections: dict) -> str:
    """Generate clean, professional HTML for PDF output."""

    # Generate experience HTML
    experience_html = ""
    for job in sections["experience"]:
        duties_html = "\n".join(f"<li>{md_links_to_html(duty)}</li>" for duty in job["duties"])
        experience_html += f"""
            <div class="job">
                <div class="job-header">
                    <span class="company">{job['company']}</span>
                    <span class="dates">{job['dates']} | {job['location']}</span>
                </div>
                <div class="title">{job['title']}</div>
                <ul>{duties_html}</ul>
            </div>
"""

    # Generate projects HTML
    projects_html = ""
    for project in sections["projects"]:
        bullets_html = "\n".join(f"<li>{md_links_to_html(bullet)}</li>" for bullet in project["bullets"])
        projects_html += f"""
            <div class="project">
                <div class="project-header">
                    <span class="name">{project['name']}</span>
                    <span class="subtitle">{project['subtitle']}</span>
                </div>
                <div class="description">{project['description']}</div>
                <ul>{bullets_html}</ul>
            </div>
"""

    # Generate skills HTML
    skills_html = ""
    for label, value in sections["skills"].items():
        skills_html += f"<div class='skill-row'><span class='label'>{label}:</span> {value}</div>\n"

    # Generate patents HTML
    patents_html = ""
    for patent in sections["patents"]:
        patents_html += f"<li><strong>{patent['number']}</strong> — {patent['title']}</li>\n"

    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Resume | {sections['name']}</title>
    <style>
        @page {{
            size: letter;
            margin: 0.6in 0.7in;
        }}

        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
            font-size: 10pt;
            line-height: 1.4;
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

        .contact a {{
            color: #0066cc;
            text-decoration: none;
        }}

        section {{
            margin-bottom: 14pt;
        }}

        h2 {{
            font-size: 12pt;
            font-weight: 700;
            color: #000;
            border-bottom: 1pt solid #ccc;
            padding-bottom: 3pt;
            margin-bottom: 8pt;
            text-transform: uppercase;
            letter-spacing: 0.5pt;
        }}

        .summary {{
            font-size: 10pt;
            color: #444;
            text-align: justify;
        }}

        .job, .project {{
            margin-bottom: 10pt;
        }}

        .job-header, .project-header {{
            display: flex;
            justify-content: space-between;
            align-items: baseline;
        }}

        .company, .name {{
            font-weight: 700;
            font-size: 11pt;
            color: #000;
        }}

        .dates, .subtitle {{
            font-size: 9pt;
            color: #666;
        }}

        .job .title {{
            font-style: italic;
            color: #555;
            margin-bottom: 4pt;
        }}

        .project .description {{
            font-style: italic;
            color: #555;
            margin-bottom: 4pt;
        }}

        ul {{
            margin-left: 18pt;
            margin-top: 4pt;
        }}

        li {{
            margin-bottom: 2pt;
        }}

        .skills {{
            display: block;
        }}

        .skill-row {{
            display: block;
            font-size: 10pt;
            margin-bottom: 3pt;
        }}

        .skill-row .label {{
            font-weight: 600;
        }}

        .patents ul {{
            list-style-type: none;
            margin-left: 0;
        }}

        .patents li {{
            margin-bottom: 3pt;
        }}

        .education {{
            font-size: 10pt;
        }}

        .focus {{
            font-size: 10pt;
            color: #444;
        }}
    </style>
</head>
<body>
    <header>
        <h1>{sections['name']}</h1>
        <div class="title">{sections['title']}</div>
        <div class="contact">
            {sections['location']} |
            <a href="mailto:{sections['email']}">{sections['email']}</a>
        </div>
    </header>

    <section>
        <h2>Summary</h2>
        <p class="summary">{sections['summary']}</p>
    </section>

    <section>
        <h2>Experience</h2>
{experience_html}
    </section>

    <section>
        <h2>Projects</h2>
{projects_html}
    </section>

    <section>
        <h2>Skills</h2>
        <div class="skills">
{skills_html}
        </div>
    </section>

    <section class="patents">
        <h2>Patents</h2>
        <ul>
{patents_html}
        </ul>
    </section>

    <section>
        <h2>Education</h2>
        <p class="education">{sections['education']}</p>
    </section>

    <section>
        <h2>Current Focus</h2>
        <p class="focus">{sections['current_focus']}</p>
    </section>
</body>
</html>
'''
    return html


def generate_pdf(sections: dict, output_path: Path) -> None:
    """Generate PDF from sections using clean professional template."""
    try:
        from weasyprint import HTML
    except ImportError:
        print("Error: weasyprint not installed. Run: uv add weasyprint")
        raise SystemExit(1)

    print("Generating professional PDF template...")
    html_content = generate_pdf_html(sections)

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
    sections = parse_resume_md(content)

    print("Generating HTML...")
    html = generate_html(sections)

    if not args.pdf_only:
        print(f"Writing {resume_html_path}...")
        resume_html_path.write_text(html)
        print("Done! resume.html has been generated.")

    if args.pdf or args.pdf_only:
        generate_pdf(sections, resume_pdf_path)
        print("Done! resume.pdf has been generated.")

    return 0


if __name__ == "__main__":
    exit(main())
