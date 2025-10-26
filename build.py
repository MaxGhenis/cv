#!/usr/bin/env python3
"""
Build script for generating HTML and PDF versions of CV from markdown.

Usage:
    python build.py [--html] [--pdf] [--all]

If no arguments provided, builds both HTML and PDF.
"""

import argparse
import re
import subprocess
import sys
from pathlib import Path


def markdown_to_html(markdown_path: Path, template_path: Path, output_path: Path) -> None:
    """
    Convert markdown CV to HTML using custom template.

    Args:
        markdown_path: Path to markdown CV file
        template_path: Path to HTML template file
        output_path: Path to output HTML file
    """
    # Read markdown content
    with open(markdown_path, 'r') as f:
        markdown_content = f.read()

    # Read template
    with open(template_path, 'r') as f:
        template = f.read()

    # Convert markdown to HTML using markdown library
    try:
        import markdown
        html_content = markdown.markdown(
            markdown_content,
            extensions=['extra', 'smarty']
        )
    except ImportError:
        # Fallback: use pandoc if markdown library not available
        try:
            result = subprocess.run(
                ['pandoc', str(markdown_path), '-t', 'html', '--no-highlight'],
                capture_output=True,
                text=True,
                check=True
            )
            html_content = result.stdout
        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            print(f"Error: Could not convert markdown to HTML. Install markdown or pandoc: pip install markdown")
            sys.exit(1)

    # Post-process HTML to add semantic structure
    html_content = add_semantic_classes(html_content)

    # Insert content into template
    final_html = template.replace('{{CONTENT}}', html_content)

    # Write output
    with open(output_path, 'w') as f:
        f.write(final_html)

    print(f"✓ Generated HTML: {output_path}")


def add_semantic_classes(html: str) -> str:
    """
    Add semantic CSS classes to HTML elements for better styling.

    Args:
        html: Raw HTML content

    Returns:
        HTML with added classes
    """
    # Wrap contact info in div (handles both old and new format)
    html = re.sub(
        r'(<p>max@policyengine\.org.*?linkedin\.com/in/maxghenis.*?</p>)',
        r'<div class="contact-info">\1</div>',
        html,
        flags=re.DOTALL
    )

    # Add summary class
    html = re.sub(
        r'(<h2>Summary</h2>\s*<p>)',
        r'<h2>Summary</h2>\n<div class="summary">\n<p>',
        html
    )
    html = re.sub(
        r'(economic impact assessment\.</p>)',
        r'\1\n</div>',
        html
    )

    return html


def html_to_pdf(html_path: Path, output_path: Path) -> None:
    """
    Convert HTML to PDF.

    Tries multiple methods in order of preference:
    1. weasyprint (best CSS support)
    2. playwright (browser-based, good CSS support)
    3. pandoc with wkhtmltopdf

    Args:
        html_path: Path to HTML file
        output_path: Path to output PDF file
    """
    # Try weasyprint first
    try:
        from weasyprint import HTML
        HTML(filename=str(html_path)).write_pdf(str(output_path))
        print(f"✓ Generated PDF: {output_path}")
        return
    except ImportError:
        pass

    # Try playwright
    try:
        from playwright.sync_api import sync_playwright

        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.goto(f'file://{html_path.absolute()}')
            page.pdf(path=str(output_path), format='Letter', print_background=True)
            browser.close()

        print(f"✓ Generated PDF: {output_path}")
        return
    except ImportError:
        pass

    # Try pandoc with wkhtmltopdf
    try:
        result = subprocess.run(
            ['pandoc', str(html_path), '-o', str(output_path), '--pdf-engine=wkhtmltopdf'],
            capture_output=True,
            text=True,
            check=True
        )
        print(f"✓ Generated PDF: {output_path}")
        return
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass

    # If all methods failed
    print("Error: Could not generate PDF. Install one of the following:")
    print("  - weasyprint: pip install weasyprint")
    print("  - playwright: pip install playwright && playwright install chromium")
    print("  - wkhtmltopdf: brew install wkhtmltopdf")
    print("\nAlternatively, open cv.html in your browser and use Print to PDF")
    sys.exit(1)


def main():
    """Main build function."""
    parser = argparse.ArgumentParser(description='Build CV in HTML and PDF formats')
    parser.add_argument('--html', action='store_true', help='Build HTML only')
    parser.add_argument('--pdf', action='store_true', help='Build PDF only')
    parser.add_argument('--all', action='store_true', help='Build both HTML and PDF (default)')

    args = parser.parse_args()

    # Default to building both if no specific format specified
    if not args.html and not args.pdf:
        args.all = True

    # Set up paths
    base_dir = Path(__file__).parent
    markdown_path = base_dir / 'cv.md'
    template_path = base_dir / 'template.html'
    html_path = base_dir / 'cv.html'
    pdf_path = base_dir / 'cv.pdf'

    # Build HTML
    if args.html or args.all:
        markdown_to_html(markdown_path, template_path, html_path)

    # Build PDF
    if args.pdf or args.all:
        # Ensure HTML is built first
        if not html_path.exists():
            markdown_to_html(markdown_path, template_path, html_path)
        html_to_pdf(html_path, pdf_path)

    print("\n✓ Build complete!")


if __name__ == '__main__':
    main()
