#!/usr/bin/env python3
"""Generate CaseWise documentation as PDF."""
import os
from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Preformatted
from reportlab.lib.enums import TA_LEFT, TA_CENTER
import re

def markdown_to_pdf(output_file):
    """Convert markdown docs to PDF."""
    doc = SimpleDocTemplate(output_file, pagesize=letter,
                          rightMargin=0.75*inch, leftMargin=0.75*inch,
                          topMargin=0.75*inch, bottomMargin=0.75*inch)

    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor='#1a1a1a',
        spaceAfter=30,
        alignment=TA_CENTER
    )

    h1_style = ParagraphStyle(
        'CustomH1',
        parent=styles['Heading1'],
        fontSize=18,
        textColor='#2c5282',
        spaceAfter=12,
        spaceBefore=12
    )

    h2_style = ParagraphStyle(
        'CustomH2',
        parent=styles['Heading2'],
        fontSize=14,
        textColor='#2d3748',
        spaceAfter=10,
        spaceBefore=10
    )

    h3_style = ParagraphStyle(
        'CustomH3',
        parent=styles['Heading3'],
        fontSize=12,
        textColor='#4a5568',
        spaceAfter=8,
        spaceBefore=8
    )

    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['BodyText'],
        fontSize=10,
        leading=14,
        spaceAfter=6
    )

    code_style = ParagraphStyle(
        'CustomCode',
        parent=styles['Code'],
        fontSize=8,
        fontName='Courier',
        leftIndent=20,
        spaceAfter=10,
        spaceBefore=10
    )

    story = []

    # Title page
    story.append(Paragraph("CaseWise AI", title_style))
    story.append(Spacer(1, 0.3*inch))
    story.append(Paragraph("Complete Project Documentation", styles['Heading2']))
    story.append(Spacer(1, 0.5*inch))
    story.append(PageBreak())

    # Documentation files to include
    docs = [
        ('README.md', 'Project Overview'),
        ('CASEWISE_PROJECT_CONTEXT.md', 'Project Context'),
        ('docs/architecture.md', 'Architecture'),
        ('docs/api.md', 'API Documentation'),
        ('docs/database.md', 'Database Schema'),
        ('docs/ai-features.md', 'AI Features'),
        ('docs/rag.md', 'RAG Implementation'),
        ('docs/security.md', 'Security'),
        ('docs/mcp.md', 'MCP Integration'),
        ('docs/development-roadmap.md', 'Development Roadmap'),
    ]

    for file_path, section_title in docs:
        full_path = Path(file_path)
        if not full_path.exists():
            continue

        # Section title
        story.append(Paragraph(section_title, h1_style))
        story.append(Spacer(1, 0.2*inch))

        # Read and process markdown
        with open(full_path, 'r', encoding='utf-8') as f:
            content = f.read()

        lines = content.split('\n')
        in_code_block = False
        code_block = []

        for line in lines:
            # Code blocks
            if line.strip().startswith('```'):
                if in_code_block:
                    # End code block
                    if code_block:
                        code_text = '\n'.join(code_block)
                        story.append(Preformatted(code_text, code_style))
                    code_block = []
                    in_code_block = False
                else:
                    in_code_block = True
                continue

            if in_code_block:
                code_block.append(line)
                continue

            # Skip empty lines
            if not line.strip():
                story.append(Spacer(1, 0.1*inch))
                continue

            # Headers
            if line.startswith('# '):
                text = line[2:].strip()
                story.append(Paragraph(text, h1_style))
            elif line.startswith('## '):
                text = line[3:].strip()
                story.append(Paragraph(text, h2_style))
            elif line.startswith('### '):
                text = line[4:].strip()
                story.append(Paragraph(text, h3_style))
            elif line.startswith('#### '):
                text = line[5:].strip()
                story.append(Paragraph(text, h3_style))
            # Lists
            elif line.strip().startswith('- ') or line.strip().startswith('* '):
                text = line.strip()[2:]
                story.append(Paragraph(f"• {text}", body_style))
            elif re.match(r'^\d+\.', line.strip()):
                text = re.sub(r'^\d+\.\s*', '', line.strip())
                story.append(Paragraph(f"• {text}", body_style))
            # Tables (simple conversion)
            elif '|' in line and not line.startswith('---'):
                cells = [c.strip() for c in line.split('|') if c.strip()]
                if cells:
                    text = ' | '.join(cells)
                    story.append(Paragraph(text, body_style))
            # Regular paragraphs
            else:
                # Escape special XML characters
                text = line.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
                # Handle inline code
                text = re.sub(r'`([^`]+)`', r'<font name="Courier">\1</font>', text)
                # Handle bold
                text = re.sub(r'\*\*([^*]+)\*\*', r'<b>\1</b>', text)
                # Handle italic
                text = re.sub(r'\*([^*]+)\*', r'<i>\1</i>', text)
                story.append(Paragraph(text, body_style))

        story.append(PageBreak())

    # Build PDF
    doc.build(story)
    print(f"✓ PDF generated: {output_file}")

if __name__ == '__main__':
    output = 'CaseWise_Documentation.pdf'
    markdown_to_pdf(output)
