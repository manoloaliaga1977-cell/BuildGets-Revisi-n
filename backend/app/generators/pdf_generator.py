"""
PDF Generator
Generates PDF budget documents from Budget objects
"""
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT
from datetime import datetime
from ..models.budget import Budget, BudgetChapter


class PDFGenerator:
    """Generator for PDF budget documents"""

    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()

    def _setup_custom_styles(self):
        """Setup custom paragraph styles"""
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=18,
            textColor=colors.HexColor('#1a365d'),
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))

        self.styles.add(ParagraphStyle(
            name='ChapterTitle',
            parent=self.styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#2d3748'),
            spaceAfter=12,
            spaceBefore=12,
            fontName='Helvetica-Bold'
        ))

        self.styles.add(ParagraphStyle(
            name='SubChapterTitle',
            parent=self.styles['Heading3'],
            fontSize=12,
            textColor=colors.HexColor('#4a5568'),
            spaceAfter=8,
            spaceBefore=8,
            fontName='Helvetica-Bold',
            leftIndent=20
        ))

    def generate_file(self, budget: Budget, file_path: str):
        """Generate a PDF file from a Budget object"""
        doc = SimpleDocTemplate(
            file_path,
            pagesize=A4,
            rightMargin=2*cm,
            leftMargin=2*cm,
            topMargin=2*cm,
            bottomMargin=2*cm
        )

        story = []

        # Title and metadata
        story.extend(self._generate_header(budget))

        # Chapters
        for chapter in budget.chapters:
            story.extend(self._generate_chapter(chapter, level=0))

        # Summary
        story.extend(self._generate_summary(budget))

        # Build PDF
        doc.build(story)

    def _generate_header(self, budget: Budget) -> list:
        """Generate PDF header with budget info"""
        elements = []

        # Title
        title = Paragraph(budget.metadata.title, self.styles['CustomTitle'])
        elements.append(title)
        elements.append(Spacer(1, 0.5*cm))

        # Metadata table
        metadata_data = [
            ['Fecha:', budget.metadata.date.strftime('%d/%m/%Y')],
            ['Moneda:', budget.metadata.currency],
        ]

        if budget.metadata.owner:
            metadata_data.insert(0, ['Empresa:', budget.metadata.owner])

        metadata_table = Table(metadata_data, colWidths=[4*cm, 12*cm])
        metadata_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#2d3748')),
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ]))

        elements.append(metadata_table)
        elements.append(Spacer(1, 1*cm))

        return elements

    def _generate_chapter(self, chapter: BudgetChapter, level: int = 0) -> list:
        """Generate chapter section"""
        elements = []

        # Chapter title
        style_name = 'ChapterTitle' if level == 0 else 'SubChapterTitle'
        title_text = f"{chapter.code} - {chapter.title}"
        title = Paragraph(title_text, self.styles[style_name])
        elements.append(title)

        # Items table
        if chapter.items:
            elements.append(self._generate_items_table(chapter.items, level))

        # Subchapters
        for subchapter in chapter.subchapters:
            elements.extend(self._generate_chapter(subchapter, level + 1))

        # Chapter total
        if level == 0:
            total_data = [[
                '',
                '',
                '',
                'TOTAL CAPÍTULO:',
                f"{float(chapter.total):,.2f} €"
            ]]

            total_table = Table(total_data, colWidths=[2*cm, 6*cm, 2*cm, 3*cm, 3*cm])
            total_table.setStyle(TableStyle([
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 11),
                ('ALIGN', (3, 0), (-1, -1), 'RIGHT'),
                ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#1a365d')),
                ('LINEABOVE', (3, 0), (-1, 0), 2, colors.HexColor('#1a365d')),
            ]))

            elements.append(Spacer(1, 0.3*cm))
            elements.append(total_table)
            elements.append(Spacer(1, 0.5*cm))

        return elements

    def _generate_items_table(self, items: list, level: int) -> Table:
        """Generate table for budget items"""
        # Header
        data = [[
            'Código',
            'Descripción',
            'Cantidad',
            'Precio',
            'Total'
        ]]

        # Items
        for item in items:
            data.append([
                item.code,
                item.description,
                f"{float(item.quantity)} {item.unit}",
                f"{float(item.price):,.2f} €",
                f"{float(item.total):,.2f} €"
            ])

        # Create table
        table = Table(data, colWidths=[2*cm, 6*cm, 2*cm, 3*cm, 3*cm])

        # Style
        table.setStyle(TableStyle([
            # Header
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4299e1')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),

            # Body
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('ALIGN', (2, 1), (-1, -1), 'RIGHT'),
            ('ALIGN', (0, 1), (1, -1), 'LEFT'),

            # Grid
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f7fafc')]),

            # Padding
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ]))

        return table

    def _generate_summary(self, budget: Budget) -> list:
        """Generate budget summary"""
        elements = []

        elements.append(Spacer(1, 1*cm))
        elements.append(Paragraph('RESUMEN DEL PRESUPUESTO', self.styles['ChapterTitle']))

        # Summary data
        summary_data = [
            ['Total de partidas:', str(budget.total_items)],
            ['TOTAL PRESUPUESTO:', f"{float(budget.total):,.2f} €"]
        ]

        summary_table = Table(summary_data, colWidths=[10*cm, 6*cm])
        summary_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 12),
            ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
            ('LINEABOVE', (0, 1), (-1, 1), 2, colors.HexColor('#1a365d')),
            ('LINEBELOW', (0, 1), (-1, 1), 2, colors.HexColor('#1a365d')),
            ('TEXTCOLOR', (0, 1), (-1, 1), colors.HexColor('#1a365d')),
            ('TOPPADDING', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ]))

        elements.append(summary_table)

        return elements
