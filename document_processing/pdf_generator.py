"""
PDF Generator for AutoDoc AI

Converts Markdown documentation to professionally formatted PDF.

Supports multiple backends:
1. WeasyPrint (primary) - HTML/CSS to PDF
2. Markdown to HTML to PDF
3. Pandoc (if available)
"""

from pathlib import Path
from typing import Optional
import markdown
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PDFGenerator:
    """
    Generate PDF documents from Markdown content.

    Uses WeasyPrint for high-quality PDF generation with CSS styling.
    Falls back to simpler methods if WeasyPrint is not available.
    """

    def __init__(self):
        """Initialize PDF generator."""
        self.weasyprint_available = False
        self.pandoc_available = False

        # Check for WeasyPrint
        try:
            import weasyprint
            self.weasyprint_available = True
            logger.info("WeasyPrint is available")
        except ImportError:
            logger.warning("WeasyPrint not available. Install with: pip install weasyprint")

        # Check for Pandoc
        try:
            import pypandoc
            self.pandoc_available = True
            logger.info("Pandoc is available")
        except (ImportError, OSError):
            logger.warning("Pandoc not available")

    def markdown_to_pdf(
        self,
        markdown_content: str,
        output_path: Path,
        title: Optional[str] = None,
        author: Optional[str] = None,
        include_toc: bool = True
    ) -> bool:
        """
        Convert Markdown content to PDF.

        Args:
            markdown_content: Markdown text to convert
            output_path: Path for output PDF file
            title: Document title for cover page
            author: Author name
            include_toc: Include table of contents

        Returns:
            True if successful, False otherwise
        """
        if self.weasyprint_available:
            return self._generate_with_weasyprint(
                markdown_content, output_path, title, author, include_toc
            )
        elif self.pandoc_available:
            return self._generate_with_pandoc(
                markdown_content, output_path, title, author
            )
        else:
            logger.error("No PDF generation backend available")
            return False

    def _generate_with_weasyprint(
        self,
        markdown_content: str,
        output_path: Path,
        title: Optional[str],
        author: Optional[str],
        include_toc: bool
    ) -> bool:
        """Generate PDF using WeasyPrint."""
        try:
            import weasyprint
            from weasyprint import HTML, CSS

            # Convert Markdown to HTML
            html_content = self._markdown_to_html(
                markdown_content, title, author, include_toc
            )

            # Generate PDF
            HTML(string=html_content).write_pdf(
                output_path,
                stylesheets=[CSS(string=self._get_pdf_styles())]
            )

            logger.info(f"PDF generated successfully: {output_path}")
            return True

        except Exception as e:
            logger.error(f"Error generating PDF with WeasyPrint: {e}")
            return False

    def _generate_with_pandoc(
        self,
        markdown_content: str,
        output_path: Path,
        title: Optional[str],
        author: Optional[str]
    ) -> bool:
        """Generate PDF using Pandoc."""
        try:
            import pypandoc

            # Add metadata
            if title or author:
                metadata = "---\n"
                if title:
                    metadata += f"title: \"{title}\"\n"
                if author:
                    metadata += f"author: \"{author}\"\n"
                metadata += "---\n\n"
                markdown_content = metadata + markdown_content

            # Convert to PDF
            pypandoc.convert_text(
                markdown_content,
                'pdf',
                format='md',
                outputfile=str(output_path),
                extra_args=['--pdf-engine=pdflatex']
            )

            logger.info(f"PDF generated successfully with Pandoc: {output_path}")
            return True

        except Exception as e:
            logger.error(f"Error generating PDF with Pandoc: {e}")
            return False

    def _markdown_to_html(
        self,
        markdown_content: str,
        title: Optional[str],
        author: Optional[str],
        include_toc: bool
    ) -> str:
        """
        Convert Markdown to HTML with styling.

        Args:
            markdown_content: Markdown text
            title: Document title
            author: Author name
            include_toc: Include table of contents

        Returns:
            HTML string
        """
        # Configure Markdown extensions
        extensions = [
            'markdown.extensions.tables',
            'markdown.extensions.fenced_code',
            'markdown.extensions.codehilite',
            'markdown.extensions.toc',
            'markdown.extensions.meta',
            'markdown.extensions.nl2br',
        ]

        # Convert Markdown to HTML
        md = markdown.Markdown(extensions=extensions)
        body_html = md.convert(markdown_content)

        # Extract TOC if available
        toc_html = ""
        if include_toc and hasattr(md, 'toc'):
            toc_html = f"""
            <div class="toc">
                <h2>Table of Contents</h2>
                {md.toc}
            </div>
            <div class="page-break"></div>
            """

        # Build full HTML document
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>{title or 'Model Documentation'}</title>
        </head>
        <body>
            <div class="cover-page">
                <h1>{title or 'Insurance Model Documentation'}</h1>
                {f'<p class="author">{author}</p>' if author else ''}
                <p class="date">{datetime.now().strftime('%B %d, %Y')}</p>
                <p class="disclaimer">⚠️ SYNTHETIC DATA - FOR DEMONSTRATION ONLY</p>
            </div>
            <div class="page-break"></div>

            {toc_html}

            <div class="content">
                {body_html}
            </div>

            <div class="page-break"></div>
            <div class="footer-page">
                <p>Generated by AutoDoc AI</p>
                <p>{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            </div>
        </body>
        </html>
        """

        return html

    def _get_pdf_styles(self) -> str:
        """
        Get CSS styles for PDF formatting.

        Returns:
            CSS string
        """
        return """
        @page {
            size: letter;
            margin: 1in;

            @top-right {
                content: "Page " counter(page);
                font-size: 9pt;
                color: #666;
            }
        }

        body {
            font-family: 'Georgia', 'Times New Roman', serif;
            font-size: 11pt;
            line-height: 1.6;
            color: #333;
        }

        .cover-page {
            text-align: center;
            padding-top: 3in;
        }

        .cover-page h1 {
            font-size: 28pt;
            margin-bottom: 0.5in;
            color: #1f77b4;
        }

        .cover-page .author {
            font-size: 14pt;
            margin: 0.5in 0;
        }

        .cover-page .date {
            font-size: 12pt;
            color: #666;
        }

        .cover-page .disclaimer {
            margin-top: 1in;
            padding: 20px;
            background-color: #fff3cd;
            border: 2px solid #ffc107;
            color: #856404;
            font-weight: bold;
        }

        .page-break {
            page-break-after: always;
        }

        .toc {
            padding: 20px 0;
        }

        .toc h2 {
            font-size: 18pt;
            color: #1f77b4;
            border-bottom: 2px solid #1f77b4;
            padding-bottom: 10px;
        }

        .content h1 {
            font-size: 20pt;
            color: #1f77b4;
            border-bottom: 2px solid #1f77b4;
            padding-bottom: 10px;
            margin-top: 30px;
            page-break-before: always;
        }

        .content h2 {
            font-size: 16pt;
            color: #2c3e50;
            margin-top: 25px;
            border-bottom: 1px solid #ddd;
            padding-bottom: 5px;
        }

        .content h3 {
            font-size: 13pt;
            color: #34495e;
            margin-top: 20px;
        }

        .content p {
            margin: 10px 0;
            text-align: justify;
        }

        .content ul, .content ol {
            margin: 10px 0 10px 30px;
        }

        .content li {
            margin: 5px 0;
        }

        .content table {
            width: 100%;
            border-collapse: collapse;
            margin: 15px 0;
            font-size: 10pt;
        }

        .content table th {
            background-color: #1f77b4;
            color: white;
            padding: 8px;
            text-align: left;
            font-weight: bold;
        }

        .content table td {
            border: 1px solid #ddd;
            padding: 8px;
        }

        .content table tr:nth-child(even) {
            background-color: #f9f9f9;
        }

        .content code {
            background-color: #f5f5f5;
            padding: 2px 5px;
            border-radius: 3px;
            font-family: 'Courier New', monospace;
            font-size: 9pt;
        }

        .content pre {
            background-color: #f5f5f5;
            padding: 15px;
            border-left: 4px solid #1f77b4;
            overflow-x: auto;
            font-family: 'Courier New', monospace;
            font-size: 9pt;
        }

        .content blockquote {
            border-left: 4px solid #ddd;
            padding-left: 15px;
            margin-left: 0;
            color: #666;
            font-style: italic;
        }

        .footer-page {
            text-align: center;
            padding-top: 3in;
            color: #666;
            font-size: 10pt;
        }

        strong {
            color: #2c3e50;
        }

        a {
            color: #1f77b4;
            text-decoration: none;
        }
        """


def main():
    """Test the PDF generator."""
    import sys

    # Sample Markdown content
    sample_markdown = """---
title: "Insurance Model Documentation"
model_type: "frequency"
---

# Insurance Model Documentation

⚠️ **SYNTHETIC DATA - FOR DEMONSTRATION ONLY**

## Executive Summary

This model documentation describes the development and validation of an auto insurance
frequency model for Bodily Injury coverage. The model was developed using a Generalized
Linear Model (GLM) with Poisson distribution and log link function.

### Key Findings

- **Model Performance:** AUC of 0.72, Gini coefficient of 0.44
- **Predictor Variables:** 12 statistically significant variables
- **Business Impact:** Improved risk segmentation with 15% lift in top decile
- **Validation:** Passed out-of-sample validation with stable performance

## Methodology

### Model Type Selection

A Generalized Linear Model (GLM) with Poisson distribution was selected for
frequency modeling based on the following considerations:

1. **Target Variable:** Binary outcome (claim/no claim) with low frequency
2. **Distribution:** Count data best modeled with Poisson distribution
3. **Link Function:** Log link provides multiplicative effects
4. **Regulatory Acceptance:** GLMs widely accepted for insurance applications

### Performance Metrics

| Metric | Training | Validation | Test |
|--------|----------|------------|------|
| AUC | 0.74 | 0.73 | 0.72 |
| Gini | 0.48 | 0.46 | 0.44 |
| Lift (Top 10%) | 2.5x | 2.4x | 2.3x |

## Conclusion

The model demonstrates strong predictive performance and meets all regulatory requirements.
Recommendation: Approve for production deployment.
"""

    print("=== PDF Generator Test ===\n")

    generator = PDFGenerator()

    if not (generator.weasyprint_available or generator.pandoc_available):
        print("⚠️  No PDF generation backend available")
        print("\nTo enable PDF generation, install one of:")
        print("  - WeasyPrint: pip install weasyprint")
        print("  - Pandoc: pip install pypandoc (requires pandoc binary)")
        print("\nDemo output (HTML preview):")
        print("=" * 60)
        html = generator._markdown_to_html(
            sample_markdown,
            "Insurance Model Documentation",
            "AutoDoc AI",
            True
        )
        print(html[:500] + "...")
        return

    # Generate PDF
    output_path = Path("test_output.pdf")

    print(f"Generating PDF: {output_path}")
    success = generator.markdown_to_pdf(
        sample_markdown,
        output_path,
        title="Insurance Model Documentation",
        author="AutoDoc AI",
        include_toc=True
    )

    if success:
        print(f"✅ PDF generated successfully: {output_path}")
        print(f"File size: {output_path.stat().st_size / 1024:.1f} KB")
    else:
        print("❌ PDF generation failed")


if __name__ == "__main__":
    main()
