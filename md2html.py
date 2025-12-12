import sys
from pathlib import Path

import markdown


def main():
    if len(sys.argv) < 2:
        print("Usage: uv run md2html.py <input.md> [output.html]")
        sys.exit(1)

    input_path = Path(sys.argv[1])
    if not input_path.exists():
        print(f"Error: {input_path} not found")
        sys.exit(1)

    # Output path: use second arg if provided, otherwise replace .md with .html
    if len(sys.argv) >= 3:
        output_path = Path(sys.argv[2])
    else:
        output_path = input_path.with_suffix(".html")

    # Generate title from filename (capitalize, replace hyphens with spaces)
    title = input_path.stem.replace("-", " ").replace("_", " ").title()

    md_text = input_path.read_text(encoding="utf-8")

    html_body = markdown.markdown(md_text, extensions=["fenced_code", "tables"])

    html = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>{title}</title>
  <meta name="viewport" content="width=device-width, initial-scale=1">

  <style>
    body {{
      max-width: 900px;
      margin: 48px auto;
      padding: 0 20px;
      font-family: system-ui, -apple-system, BlinkMacSystemFont,
                   "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      line-height: 1.6;
      color: #111;
    }}

    h1, h2, h3 {{
      line-height: 1.25;
      margin-top: 2em;
    }}

    h1 {{ margin-top: 0; }}

    hr {{
      margin: 3em 0;
      border: none;
      border-top: 1px solid #ddd;
    }}

    code {{
      background: #f6f8fa;
      padding: 0.2em 0.4em;
      border-radius: 4px;
      font-size: 0.95em;
    }}

    pre {{
      background: #f6f8fa;
      padding: 1em;
      overflow-x: auto;
      border-radius: 8px;
    }}
  </style>
</head>
<body>
{html_body}
</body>
</html>
"""

    output_path.write_text(html, encoding="utf-8")
    print(f"Generated {output_path}")


if __name__ == "__main__":
    main()
