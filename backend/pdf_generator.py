from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.enums import TA_RIGHT, TA_LEFT, TA_CENTER
from reportlab.platypus import (
    SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image, KeepTogether
)
from reportlab.lib.units import cm, mm
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
import os

def _fmt_money(v, symbol="$"):
    try:
        return f"{symbol}{float(v):,.2f}"
    except Exception:
        return f"{symbol}{v}"

def _register_font_if_exists(path, name="CustomFont"):
    if not path or not os.path.isfile(path):
        return None
    try:
        pdfmetrics.registerFont(TTFont(name, path))
        return name
    except Exception:
        return None

def generate_invoice_pdf(invoice, user, logo_path=None, theme_color="#0ea5e4",
                         font_path=None, currency_symbol="$"):
    """
    Generates a clean, well-aligned invoice PDF.
    """
    ACCENT = colors.HexColor(theme_color)
    TEXT = colors.HexColor("#1f2937")
    MUTED = colors.HexColor("#6b7280")
    BORDER = colors.HexColor("#e5e7eb")
    BG_LIGHT = colors.HexColor("#f9fafb")

    FONT_NAME = _register_font_if_exists(font_path, "CustomFont") or "Helvetica"
    FONT_BOLD = FONT_NAME + "-Bold" if FONT_NAME == "Helvetica" else FONT_NAME

    styles = getSampleStyleSheet()
    
    # Define consistent styles
    styles.add(ParagraphStyle(
        'CompanyName',
        fontName=FONT_BOLD,
        fontSize=24,
        textColor=ACCENT,
        leading=28,
        spaceAfter=2
    ))
    
    styles.add(ParagraphStyle(
        'InvoiceTitle',
        fontName=FONT_NAME,
        fontSize=16,
        textColor=ACCENT,
        leading=20,
        spaceAfter=8
    ))
    
    styles.add(ParagraphStyle(
        'CompanyInfo',
        fontName=FONT_NAME,
        fontSize=9,
        textColor=MUTED,
        leading=13,
        alignment=TA_RIGHT
    ))
    
    styles.add(ParagraphStyle(
        'SectionLabel',
        fontName=FONT_BOLD,
        fontSize=10,
        textColor=TEXT,
        leading=14,
        spaceAfter=4
    ))
    
    styles.add(ParagraphStyle(
        'NormalText',
        fontName=FONT_NAME,
        fontSize=9,
        textColor=TEXT,
        leading=13
    ))
    
    styles.add(ParagraphStyle(
        'MetaLabel',
        fontName=FONT_NAME,
        fontSize=9,
        textColor=TEXT,
        leading=13,
        alignment=TA_RIGHT
    ))
    
    styles.add(ParagraphStyle(
        'MetaValue',
        fontName=FONT_NAME,
        fontSize=9,
        textColor=TEXT,
        leading=13,
        alignment=TA_RIGHT
    ))
    
    styles.add(ParagraphStyle(
        'TableHeader',
        fontName=FONT_BOLD,
        fontSize=10,
        textColor=colors.white,
        leading=14
    ))
    
    styles.add(ParagraphStyle(
        'TableCell',
        fontName=FONT_NAME,
        fontSize=9,
        textColor=TEXT,
        leading=13
    ))
    
    styles.add(ParagraphStyle(
        'FooterNote',
        fontName=FONT_NAME,
        fontSize=8,
        textColor=MUTED,
        leading=11,
        alignment=TA_CENTER
    ))

    # Create PDF
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        leftMargin=2.5*cm,
        rightMargin=2.5*cm,
        topMargin=2*cm,
        bottomMargin=2*cm
    )

    story = []
    page_width = A4[0] - 5*cm  # Available width

    # ========== HEADER SECTION ==========
    header_data = []
    left_content = []
    right_content = []
    
    # Left side: Logo and Company Name
    if logo_path and os.path.isfile(logo_path):
        try:
            img = Image(logo_path)
            aspect = img.imageWidth / float(img.imageHeight)
            img.drawHeight = 2.5*cm
            img.drawWidth = 2.5*cm * aspect
            left_content.append(img)
            left_content.append(Spacer(1, 8))
        except Exception as e:
            print(f"Logo error: {e}")
    
    # Company name
    company_name = (user.company_name or user.full_name or "Company").strip()
    left_content.append(Paragraph(company_name, styles['CompanyName']))
    left_content.append(Spacer(1, 4))
    left_content.append(Paragraph("Invoice", styles['InvoiceTitle']))
    
    # Right side: Company contact info
    if getattr(user, 'company_name', None):
        right_content.append(Paragraph(f"<b>{user.company_name}</b>", styles['CompanyInfo']))
    if getattr(user, 'email', None):
        right_content.append(Paragraph(user.email, styles['CompanyInfo']))
    if getattr(user, 'phone', None):
        right_content.append(Paragraph(user.phone, styles['CompanyInfo']))
    if getattr(user, 'address', None):
        right_content.append(Paragraph(user.address, styles['CompanyInfo']))
    
    header_table = Table(
        [[left_content, right_content]],
        colWidths=[page_width * 0.55, page_width * 0.45]
    )
    header_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('ALIGN', (0, 0), (0, 0), 'LEFT'),
        ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ('TOPPADDING', (0, 0), (-1, -1), 0),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
    ]))
    story.append(header_table)
    story.append(Spacer(1, 20))

    # ========== BILL TO & INVOICE DETAILS SECTION ==========
    bill_to_content = []
    bill_to_content.append(Paragraph("<b>Bill To:</b>", styles['SectionLabel']))
    bill_to_content.append(Paragraph(invoice.client_name or "-", styles['NormalText']))
    
    if getattr(invoice, 'client_email', None):
        bill_to_content.append(Paragraph(invoice.client_email, styles['NormalText']))
    
    if getattr(invoice, 'client_address', None):
        # Split address by newlines and add each line
        addr_lines = invoice.client_address.strip().split('\n')
        for line in addr_lines:
            if line.strip():
                bill_to_content.append(Paragraph(line.strip(), styles['NormalText']))
    
    # Invoice details (right aligned)
    invoice_details = []
    invoice_details.append([
        Paragraph("<b>Invoice number:</b>", styles['MetaLabel']),
        Paragraph(invoice.invoice_number, styles['MetaValue'])
    ])
    
    if getattr(invoice, 'invoice_date', None):
        date_str = invoice.invoice_date.strftime('%d/%m/%Y') if hasattr(invoice.invoice_date, 'strftime') else str(invoice.invoice_date)
        invoice_details.append([
            Paragraph("<b>Invoice date:</b>", styles['MetaLabel']),
            Paragraph(date_str, styles['MetaValue'])
        ])
    
    if getattr(invoice, 'due_date', None):
        due_str = invoice.due_date.strftime('%d/%m/%Y') if hasattr(invoice.due_date, 'strftime') else str(invoice.due_date)
        invoice_details.append([
            Paragraph("<b>Due date:</b>", styles['MetaLabel']),
            Paragraph(due_str, styles['MetaValue'])
        ])
    
    details_table = Table(invoice_details, colWidths=[3.5*cm, 3*cm])
    details_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
        ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ('TOPPADDING', (0, 0), (-1, -1), 1),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 1),
    ]))
    
    info_section = Table(
        [[bill_to_content, details_table]],
        colWidths=[page_width * 0.55, page_width * 0.45]
    )
    info_section.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ('TOPPADDING', (0, 0), (-1, -1), 0),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
    ]))
    story.append(info_section)
    story.append(Spacer(1, 20))

    # ========== ITEMS TABLE ==========
    items_data = [[
        Paragraph("<b>Items</b>", styles['TableHeader']),
        Paragraph("<b>Quantity</b>", styles['TableHeader']),
        Paragraph("<b>Price</b>", styles['TableHeader']),
        Paragraph("<b>Amount</b>", styles['TableHeader'])
    ]]
    
    for item in invoice.items:
        items_data.append([
            Paragraph(item.description or "", styles['TableCell']),
            Paragraph(str(item.quantity), styles['TableCell']),
            Paragraph(_fmt_money(item.unit_price, currency_symbol), styles['TableCell']),
            Paragraph(_fmt_money(item.total, currency_symbol), styles['TableCell'])
        ])
    
    items_table = Table(
        items_data,
        colWidths=[page_width * 0.50, page_width * 0.16, page_width * 0.17, page_width * 0.17]
    )
    
    items_table.setStyle(TableStyle([
        # Header row
        ('BACKGROUND', (0, 0), (-1, 0), ACCENT),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), FONT_BOLD),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('TOPPADDING', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        ('LEFTPADDING', (0, 0), (0, -1), 12),
        ('RIGHTPADDING', (-1, 0), (-1, -1), 12),
        
        # Data rows
        ('FONTNAME', (0, 1), (-1, -1), FONT_NAME),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('TOPPADDING', (0, 1), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
        ('LEFTPADDING', (0, 1), (0, -1), 12),
        ('RIGHTPADDING', (-1, 1), (-1, -1), 12),
        
        # Alignment
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
        ('ALIGN', (1, 0), (-1, -1), 'RIGHT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        
        # Grid
        ('LINEBELOW', (0, 0), (-1, -1), 0.5, BORDER),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, BG_LIGHT]),
    ]))
    
    story.append(items_table)
    story.append(Spacer(1, 15))

    # ========== TOTALS SECTION ==========
    totals_data = []
    
    # Subtotal
    totals_data.append([
        Paragraph("Subtotal", styles['MetaLabel']),
        Paragraph(_fmt_money(invoice.subtotal, currency_symbol), styles['MetaValue'])
    ])
    
    # Tax
    tax_amount = getattr(invoice, 'tax_amount', 0) or 0
    totals_data.append([
        Paragraph("Tax (+)", styles['MetaLabel']),
        Paragraph(_fmt_money(tax_amount, currency_symbol), styles['MetaValue'])
    ])
    
    # Discount
    discount = getattr(invoice, 'discount', 0) or 0
    totals_data.append([
        Paragraph("Discount (-)", styles['MetaLabel']),
        Paragraph(_fmt_money(discount, currency_symbol), styles['MetaValue'])
    ])
    
    # Total
    totals_data.append([
        Paragraph("<b>Total</b>", styles['SectionLabel']),
        Paragraph(f"<b>{_fmt_money(invoice.total, currency_symbol)}</b>", styles['SectionLabel'])
    ])
    
    totals_table = Table(totals_data, colWidths=[page_width * 0.70, page_width * 0.30])
    totals_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
        ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 12),
        ('TOPPADDING', (0, 0), (-1, -2), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -2), 4),
        ('TOPPADDING', (0, -1), (-1, -1), 8),
        ('BOTTOMPADDING', (0, -1), (-1, -1), 8),
        ('LINEABOVE', (0, -1), (-1, -1), 1, BORDER),
    ]))
    
    story.append(totals_table)
    story.append(Spacer(1, 25))

    # ========== NOTES ==========
    if getattr(invoice, 'notes', None) and invoice.notes.strip():
        story.append(Paragraph("<b>Notes</b>", styles['SectionLabel']))
        story.append(Spacer(1, 4))
        story.append(Paragraph(invoice.notes, styles['NormalText']))
        story.append(Spacer(1, 20))

    # ========== FOOTER ==========
    footer_text = "Please pay the invoice before the due date. Let us know if you have any questions."
    story.append(Spacer(1, 10))
    story.append(Paragraph(footer_text, styles['FooterNote']))

    # Build PDF
    doc.build(story)
    pdf_bytes = buffer.getvalue()
    buffer.close()
    return pdf_bytes