from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List

class PDFExporter:
    def __init__(self, output_dir: str = "reports/pdf"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
    
    def _setup_custom_styles(self):
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#06b6d4'),
            spaceAfter=30,
            alignment=TA_CENTER
        ))
        
        self.styles.add(ParagraphStyle(
            name='SectionHeader',
            parent=self.styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#06b6d4'),
            spaceAfter=12,
            spaceBefore=12
        ))
    
    def generate_report(self, report_data: Dict[str, Any], filename: str) -> str:
        filepath = self.output_dir / f"{filename}.pdf"
        doc = SimpleDocTemplate(str(filepath), pagesize=letter)
        story = []
        
        # Title
        title = Paragraph(report_data.get('title', 'Security Report'), self.styles['CustomTitle'])
        story.append(title)
        story.append(Spacer(1, 0.2*inch))
        
        # Metadata
        meta_data = [
            ['Generated:', datetime.now().strftime('%Y-%m-%d %H:%M:%S')],
            ['Report Type:', report_data.get('type', 'Technical')],
            ['Target:', report_data.get('target', 'N/A')]
        ]
        meta_table = Table(meta_data, colWidths=[2*inch, 4*inch])
        meta_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#1f2937')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#374151'))
        ]))
        story.append(meta_table)
        story.append(Spacer(1, 0.3*inch))
        
        # Executive Summary
        if 'summary' in report_data:
            story.append(Paragraph('Executive Summary', self.styles['SectionHeader']))
            story.append(Paragraph(report_data['summary'], self.styles['BodyText']))
            story.append(Spacer(1, 0.2*inch))
        
        # Findings
        if 'findings' in report_data and report_data['findings']:
            story.append(Paragraph(f"Findings ({len(report_data['findings'])})", self.styles['SectionHeader']))
            
            findings_data = [['Severity', 'Title', 'Target']]
            for finding in report_data['findings'][:20]:  # Limit to 20
                findings_data.append([
                    finding.get('severity', 'N/A'),
                    finding.get('title', 'N/A')[:40],
                    finding.get('target', 'N/A')[:30]
                ])
            
            findings_table = Table(findings_data, colWidths=[1*inch, 3*inch, 2*inch])
            findings_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#06b6d4')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#374151')),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f3f4f6')])
            ]))
            story.append(findings_table)
            story.append(Spacer(1, 0.2*inch))
        
        # Credentials
        if 'credentials' in report_data and report_data['credentials']:
            story.append(PageBreak())
            story.append(Paragraph(f"Credentials ({len(report_data['credentials'])})", self.styles['SectionHeader']))
            
            creds_data = [['Service', 'Username', 'Target']]
            for cred in report_data['credentials'][:20]:
                creds_data.append([
                    cred.get('service', 'N/A'),
                    cred.get('username', 'N/A'),
                    cred.get('target', 'N/A')[:30]
                ])
            
            creds_table = Table(creds_data, colWidths=[1.5*inch, 2*inch, 2.5*inch])
            creds_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#10b981')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#374151')),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f3f4f6')])
            ]))
            story.append(creds_table)
        
        doc.build(story)
        return str(filepath)

pdf_exporter = PDFExporter()
