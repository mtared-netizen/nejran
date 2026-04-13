# -*- coding: utf-8 -*-
import arabic_reshaper
from bidi.algorithm import get_display
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                 TableStyle, HRFlowable, PageBreak)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT, TA_JUSTIFY
import os

# Register Arabic fonts
pdfmetrics.registerFont(TTFont('ArabicRegular', r'C:\Windows\Fonts\BTraditionalArabic-Regular.ttf'))
pdfmetrics.registerFont(TTFont('ArabicBold', r'C:\Windows\Fonts\BTraditionalArabic-Bold.ttf'))
pdfmetrics.registerFont(TTFont('Tahoma', r'C:\Windows\Fonts\tahoma.ttf'))
pdfmetrics.registerFont(TTFont('TahomaBold', r'C:\Windows\Fonts\tahomabd.ttf'))

def ar(text):
    """Reshape and apply bidi to Arabic text for proper display."""
    reshaped = arabic_reshaper.reshape(text)
    return get_display(reshaped)

# ── Color palette ──────────────────────────────────────────────────────────────
DARK_GREEN   = colors.HexColor('#1a5c2e')
MED_GREEN    = colors.HexColor('#2e8b57')
LIGHT_GREEN  = colors.HexColor('#d4edda')
GOLD         = colors.HexColor('#c9a84c')
LIGHT_GRAY   = colors.HexColor('#f5f5f5')
DARK_GRAY    = colors.HexColor('#333333')
WHITE        = colors.white

# ── Styles ─────────────────────────────────────────────────────────────────────
def make_styles():
    s = {}

    s['cover_title'] = ParagraphStyle(
        'cover_title', fontName='ArabicBold', fontSize=26,
        textColor=WHITE, alignment=TA_CENTER, leading=36, spaceAfter=10)

    s['cover_sub'] = ParagraphStyle(
        'cover_sub', fontName='ArabicRegular', fontSize=16,
        textColor=GOLD, alignment=TA_CENTER, leading=24, spaceAfter=6)

    s['chapter'] = ParagraphStyle(
        'chapter', fontName='ArabicBold', fontSize=18,
        textColor=WHITE, alignment=TA_CENTER, leading=26,
        backColor=DARK_GREEN, borderPadding=(8, 12, 8, 12))

    s['section'] = ParagraphStyle(
        'section', fontName='ArabicBold', fontSize=14,
        textColor=DARK_GREEN, alignment=TA_RIGHT, leading=22,
        spaceAfter=4, spaceBefore=12,
        borderPad=4)

    s['body'] = ParagraphStyle(
        'body', fontName='ArabicRegular', fontSize=11,
        textColor=DARK_GRAY, alignment=TA_RIGHT, leading=20,
        spaceAfter=6, rightIndent=0)

    s['bullet'] = ParagraphStyle(
        'bullet', fontName='ArabicRegular', fontSize=11,
        textColor=DARK_GRAY, alignment=TA_RIGHT, leading=20,
        spaceAfter=4, rightIndent=14, leftIndent=0)

    s['table_header'] = ParagraphStyle(
        'table_header', fontName='ArabicBold', fontSize=11,
        textColor=WHITE, alignment=TA_CENTER, leading=18)

    s['table_cell'] = ParagraphStyle(
        'table_cell', fontName='ArabicRegular', fontSize=10,
        textColor=DARK_GRAY, alignment=TA_CENTER, leading=16)

    s['footer'] = ParagraphStyle(
        'footer', fontName='ArabicRegular', fontSize=9,
        textColor=colors.grey, alignment=TA_CENTER, leading=14)

    s['highlight_box'] = ParagraphStyle(
        'highlight_box', fontName='ArabicBold', fontSize=12,
        textColor=DARK_GREEN, alignment=TA_CENTER, leading=20,
        backColor=LIGHT_GREEN, borderPadding=(6, 10, 6, 10))

    return s

# ── Helper: section header ─────────────────────────────────────────────────────
def section_title(text, styles):
    return [
        Paragraph(ar(text), styles['section']),
        HRFlowable(width="100%", thickness=2, color=GOLD, spaceAfter=8),
    ]

def chapter_header(text, styles):
    data = [[Paragraph(ar(text), styles['chapter'])]]
    t = Table(data, colWidths=[17*cm])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), DARK_GREEN),
        ('TOPPADDING', (0,0), (-1,-1), 10),
        ('BOTTOMPADDING', (0,0), (-1,-1), 10),
        ('ROUNDEDCORNERS', [6]),
    ]))
    return [Spacer(1, 0.3*cm), t, Spacer(1, 0.4*cm)]

def bullet_item(text, styles):
    return Paragraph("◄  " + ar(text), styles['bullet'])

# ══════════════════════════════════════════════════════════════════════════════
# BUILD DOCUMENT
# ══════════════════════════════════════════════════════════════════════════════
output_path = r"c:\Users\mtare\ابو عثمان\الخطة_الاستراتيجية_جمعية_الدعوة_نجران.pdf"

doc = SimpleDocTemplate(
    output_path,
    pagesize=A4,
    rightMargin=2*cm, leftMargin=2*cm,
    topMargin=2*cm, bottomMargin=2*cm,
    title="الخطة الاستراتيجية - جمعية الدعوة في نجران"
)

styles = make_styles()
story = []

# ══════════════════════════════════════════════════════════════
# COVER PAGE
# ══════════════════════════════════════════════════════════════
# Green banner at top
cover_banner = Table([[""]], colWidths=[17*cm], rowHeights=[4*cm])
cover_banner.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,-1), DARK_GREEN),
]))
story.append(cover_banner)
story.append(Spacer(1, 0.6*cm))

# Decorative gold line
story.append(HRFlowable(width="100%", thickness=4, color=GOLD))
story.append(Spacer(1, 0.4*cm))

cover_data = [
    [Paragraph(ar("المملكة العربية السعودية"), styles['cover_sub'])],
    [Paragraph(ar("وزارة الشؤون الإسلامية والدعوة والإرشاد"), styles['cover_sub'])],
    [Spacer(1, 0.3*cm)],
    [Paragraph(ar("جمعية الدعوة الإسلامية"), styles['cover_title'])],
    [Paragraph(ar("منطقة نجران"), styles['cover_title'])],
    [Spacer(1, 0.5*cm)],
    [HRFlowable(width="80%", thickness=2, color=GOLD)],
    [Spacer(1, 0.3*cm)],
    [Paragraph(ar("الخطة الاستراتيجية"), styles['cover_title'])],
    [Paragraph(ar("2025 م – 2030 م"), styles['cover_sub'])],
    [Spacer(1, 0.5*cm)],
    [Paragraph(ar("تقرير شامل لبناء وتطوير العمل الدعوي"), styles['cover_sub'])],
]
cover_table = Table(cover_data, colWidths=[17*cm])
cover_table.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,-1), DARK_GREEN),
    ('ALIGN', (0,0), (-1,-1), 'CENTER'),
    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ('TOPPADDING', (0,0), (-1,-1), 6),
    ('BOTTOMPADDING', (0,0), (-1,-1), 6),
]))
story.append(cover_table)

story.append(Spacer(1, 0.4*cm))
story.append(HRFlowable(width="100%", thickness=4, color=GOLD))
story.append(Spacer(1, 0.3*cm))

# Date / footer on cover
story.append(Paragraph(ar("تاريخ الإصدار: 1446 هـ  |  2025 م"), styles['footer']))
story.append(PageBreak())

# ══════════════════════════════════════════════════════════════
# CHAPTER 1: INTRODUCTION & EXECUTIVE SUMMARY
# ══════════════════════════════════════════════════════════════
story += chapter_header("الفصل الأول: المقدمة والملخص التنفيذي", styles)

story += section_title("مقدمة", styles)
story.append(Paragraph(ar(
    "تُعدّ الخطة الاستراتيجية الأداة الرئيسية لتحديد مسارات العمل وتوجيه الموارد نحو "
    "تحقيق الأهداف المنشودة، وانطلاقاً من رسالة جمعية الدعوة الإسلامية في منطقة نجران "
    "القائمة على نشر الإسلام الصحيح وتعزيز الوعي الديني في المجتمع، جاءت هذه الخطة "
    "الاستراتيجية لتمتد على مدى خمس سنوات (2025–2030م)."
), styles['body']))
story.append(Paragraph(ar(
    "تنبثق هذه الخطة من الإطار التنظيمي لوزارة الشؤون الإسلامية والدعوة والإرشاد، "
    "وتتوافق مع أهداف رؤية المملكة العربية السعودية 2030 في مجال تعزيز الهوية الإسلامية "
    "وترسيخ القيم الدينية في نفوس الأجيال."
), styles['body']))
story.append(Spacer(1, 0.3*cm))

story += section_title("الملخص التنفيذي", styles)
summary_items = [
    "تأسست الجمعية بهدف تفعيل دور الدعوة الإسلامية وترسيخها في منطقة نجران.",
    "تشمل الخطة 6 محاور استراتيجية تغطي جميع جوانب العمل الدعوي.",
    "تستهدف الخطة الوصول إلى أكثر من 200,000 مستفيد خلال مدة تنفيذها.",
    "تتضمن الخطة 24 مبادرة استراتيجية و48 برنامجاً تنفيذياً.",
    "تُقدَّر الميزانية الإجمالية للخطة بـ 35 مليون ريال سعودي.",
    "تُبنى الخطة على مبادئ الشفافية والمساءلة وقياس الأداء المستمر.",
]
for item in summary_items:
    story.append(bullet_item(item, styles))
story.append(Spacer(1, 0.3*cm))

# Highlight box
hb = Table([[Paragraph(ar(
    "هذه الخطة وثيقة حية قابلة للمراجعة والتحديث بحسب المستجدات والمتغيرات البيئية"
), styles['highlight_box'])]], colWidths=[17*cm])
hb.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,-1), LIGHT_GREEN),
    ('TOPPADDING', (0,0), (-1,-1), 10),
    ('BOTTOMPADDING', (0,0), (-1,-1), 10),
    ('BOX', (0,0), (-1,-1), 1.5, MED_GREEN),
    ('ROUNDEDCORNERS', [6]),
]))
story.append(hb)
story.append(PageBreak())

# ══════════════════════════════════════════════════════════════
# CHAPTER 2: VISION, MISSION, VALUES
# ══════════════════════════════════════════════════════════════
story += chapter_header("الفصل الثاني: الرؤية والرسالة والقيم", styles)

story += section_title("الرؤية", styles)
vision_box = Table([[Paragraph(ar(
    '"مجتمع نجران الواعي المتمسك بثوابت الإسلام، رائد في نشر قيم الوسطية والاعتدال"'
), styles['highlight_box'])]], colWidths=[17*cm])
vision_box.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,-1), DARK_GREEN),
    ('TOPPADDING', (0,0), (-1,-1), 14),
    ('BOTTOMPADDING', (0,0), (-1,-1), 14),
    ('ROUNDEDCORNERS', [8]),
]))
story.append(vision_box)
story.append(Spacer(1, 0.5*cm))

story += section_title("الرسالة", styles)
mission_box = Table([[Paragraph(ar(
    '"تقديم الدعوة الإسلامية الصحيحة القائمة على الكتاب والسنة، وتنمية الوعي الديني '
    'لدى أبناء منطقة نجران وزوارها، وتأهيل الكوادر الدعوية المؤهلة"'
), styles['highlight_box'])]], colWidths=[17*cm])
mission_box.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,-1), LIGHT_GREEN),
    ('TOPPADDING', (0,0), (-1,-1), 12),
    ('BOTTOMPADDING', (0,0), (-1,-1), 12),
    ('BOX', (0,0), (-1,-1), 2, DARK_GREEN),
    ('ROUNDEDCORNERS', [6]),
]))
story.append(mission_box)
story.append(Spacer(1, 0.5*cm))

story += section_title("القيم المؤسسية", styles)
values_data = [
    [Paragraph(ar("القيمة"), styles['table_header']),
     Paragraph(ar("المفهوم والممارسة"), styles['table_header'])],
    [Paragraph(ar("الإخلاص"), styles['table_cell']),
     Paragraph(ar("العمل لوجه الله تعالى والتجرد من الأهواء الشخصية"), styles['table_cell'])],
    [Paragraph(ar("الوسطية"), styles['table_cell']),
     Paragraph(ar("اعتماد منهج الاعتدال وتجنب الغلو والتطرف"), styles['table_cell'])],
    [Paragraph(ar("المهنية"), styles['table_cell']),
     Paragraph(ar("الالتزام بأعلى معايير الجودة في تقديم الخدمات الدعوية"), styles['table_cell'])],
    [Paragraph(ar("الشراكة"), styles['table_cell']),
     Paragraph(ar("بناء تحالفات فاعلة مع المؤسسات والجهات ذات العلاقة"), styles['table_cell'])],
    [Paragraph(ar("الابتكار"), styles['table_cell']),
     Paragraph(ar("توظيف الأساليب الحديثة والتقنية في خدمة العمل الدعوي"), styles['table_cell'])],
    [Paragraph(ar("الشمولية"), styles['table_cell']),
     Paragraph(ar("استيعاب جميع فئات المجتمع ومكوناته في برامج الجمعية"), styles['table_cell'])],
]
values_table = Table(values_data, colWidths=[4*cm, 13*cm])
values_table.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), DARK_GREEN),
    ('BACKGROUND', (0,1), (-1,1), LIGHT_GREEN),
    ('BACKGROUND', (0,2), (-1,2), WHITE),
    ('BACKGROUND', (0,3), (-1,3), LIGHT_GREEN),
    ('BACKGROUND', (0,4), (-1,4), WHITE),
    ('BACKGROUND', (0,5), (-1,5), LIGHT_GREEN),
    ('BACKGROUND', (0,6), (-1,6), WHITE),
    ('ALIGN', (0,0), (-1,-1), 'CENTER'),
    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ('TOPPADDING', (0,0), (-1,-1), 8),
    ('BOTTOMPADDING', (0,0), (-1,-1), 8),
    ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
    ('ROWBACKGROUNDS', (0,1), (-1,-1), [LIGHT_GREEN, WHITE]),
]))
story.append(values_table)
story.append(PageBreak())

# ══════════════════════════════════════════════════════════════
# CHAPTER 3: SITUATION ANALYSIS
# ══════════════════════════════════════════════════════════════
story += chapter_header("الفصل الثالث: تحليل الوضع الراهن (SWOT)", styles)

story += section_title("نظرة عامة على منطقة نجران", styles)
story.append(Paragraph(ar(
    "تقع منطقة نجران في الجنوب الغربي من المملكة العربية السعودية، وتتميز بموقعها "
    "الجغرافي المتاخم للحدود اليمنية مما يجعلها ذات أهمية استراتيجية بالغة. يبلغ عدد "
    "سكانها أكثر من 600,000 نسمة ينتمون إلى قبائل وشرائح اجتماعية متنوعة، مما يُشكّل "
    "تحدياً وفرصة في آنٍ معاً للعمل الدعوي."
), styles['body']))
story.append(Spacer(1, 0.3*cm))

# SWOT Table
swot_data = [
    [Paragraph(ar("نقاط القوة  S"), styles['table_header']),
     Paragraph(ar("نقاط الضعف  W"), styles['table_header'])],
    [
        Paragraph(ar(
            "• كوادر دعوية متخصصة ومؤهلة\n"
            "• شبكة علاقات مع المؤسسات الدينية\n"
            "• دعم حكومي وإشراف وزاري مباشر\n"
            "• وجود ميداني واسع في المنطقة\n"
            "• سمعة طيبة في الأوساط المحلية"
        ), styles['table_cell']),
        Paragraph(ar(
            "• محدودية الموارد المالية الذاتية\n"
            "• ضعف التواجد الرقمي والإلكتروني\n"
            "• قلة الكوادر الإدارية المتخصصة\n"
            "• غياب منظومة قياس الأداء\n"
            "• ضعف التوثيق والأرشفة المؤسسية"
        ), styles['table_cell']),
    ],
    [Paragraph(ar("الفرص  O"), styles['table_header']),
     Paragraph(ar("التهديدات  T"), styles['table_header'])],
    [
        Paragraph(ar(
            "• رؤية 2030 والدعم الحكومي للمنظمات\n"
            "• التوسع في استخدام التقنية للدعوة\n"
            "• الشراكات مع الجامعات والمدارس\n"
            "• الزيارات السياحية لمنطقة نجران\n"
            "• البرامج الوطنية للتطوع"
        ), styles['table_cell']),
        Paragraph(ar(
            "• الغزو الفكري والتأثيرات السلبية\n"
            "• ضعف اهتمام الشباب بالعمل التطوعي\n"
            "• التنافس مع المحتوى الرقمي الهادم\n"
            "• التغيرات الاجتماعية المتسارعة\n"
            "• شُح التمويل في بعض المراحل"
        ), styles['table_cell']),
    ],
]
swot_table = Table(swot_data, colWidths=[8.5*cm, 8.5*cm])
swot_table.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (0,0), MED_GREEN),
    ('BACKGROUND', (1,0), (1,0), colors.HexColor('#c0392b')),
    ('BACKGROUND', (0,2), (0,2), colors.HexColor('#2980b9')),
    ('BACKGROUND', (1,2), (1,2), colors.HexColor('#8e44ad')),
    ('ALIGN', (0,0), (-1,-1), 'CENTER'),
    ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ('TOPPADDING', (0,0), (-1,-1), 10),
    ('BOTTOMPADDING', (0,0), (-1,-1), 10),
    ('LEFTPADDING', (0,0), (-1,-1), 8),
    ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ('GRID', (0,0), (-1,-1), 1, colors.white),
    ('BACKGROUND', (0,1), (0,1), colors.HexColor('#d5f5e3')),
    ('BACKGROUND', (1,1), (1,1), colors.HexColor('#fadbd8')),
    ('BACKGROUND', (0,3), (0,3), colors.HexColor('#d6eaf8')),
    ('BACKGROUND', (1,3), (1,3), colors.HexColor('#e8daef')),
]))
story.append(swot_table)
story.append(PageBreak())

# ══════════════════════════════════════════════════════════════
# CHAPTER 4: STRATEGIC GOALS
# ══════════════════════════════════════════════════════════════
story += chapter_header("الفصل الرابع: المحاور والأهداف الاستراتيجية", styles)

strategic_goals = [
    ("المحور الأول: التمكين المؤسسي",
     "بناء مؤسسة دعوية احترافية متكاملة الأركان بحوكمة رشيدة وكوادر مؤهلة وأنظمة حديثة.",
     ["تطوير الهيكل التنظيمي وتوصيف الوظائف بحلول 2026م",
      "بناء نظام معلوماتي متكامل لإدارة أعمال الجمعية",
      "تطبيق نظام الجودة ومعايير الأداء المؤسسي",
      "رفع طاقة استيعاب الكوادر إلى 150 متطوعاً بحلول 2027م"]),
    ("المحور الثاني: الدعوة والتوعية الدينية",
     "نشر الوعي الديني الصحيح ومفاهيم الإسلام الوسطي بين شرائح المجتمع كافة.",
     ["تنظيم 500 محاضرة ودرس ديني سنوياً في المساجد والمراكز",
      "إصدار 12 مطبوعة دعوية متنوعة سنوياً باللغتين العربية والإنجليزية",
      "تدريب 100 داعية محترف في أساليب الدعوة الحديثة",
      "الوصول إلى 50,000 مستفيد من البرامج الدعوية سنوياً"]),
    ("المحور الثالث: الدعوة الرقمية والإعلامية",
     "توظيف التقنية ووسائل التواصل الاجتماعي في خدمة الدعوة الإسلامية.",
     ["إطلاق منصة رقمية متكاملة للمحتوى الدعوي بحلول 2026م",
      "الوصول إلى 100,000 متابع عبر منصات التواصل الاجتماعي",
      "إنتاج 200 مقطع فيديو دعوي سنوياً بجودة عالية",
      "إطلاق بودكاست ديني أسبوعي يخدم الشباب"]),
    ("المحور الرابع: التعليم والتأهيل الشرعي",
     "تنمية الكفاءات الدعوية وتأهيل العلماء والدعاة عبر برامج تعليمية منهجية.",
     ["تأسيس مركز تدريب دعوي متخصص في نجران",
      "إطلاق برامج دبلوم في الدعوة والإرشاد بالتعاون مع الجامعات",
      "تنفيذ 30 دورة تدريبية متخصصة سنوياً للدعاة",
      "منح 200 منحة دراسية للعلوم الشرعية خلال مدة الخطة"]),
    ("المحور الخامس: خدمة المجتمع والشراكات",
     "تفعيل دور الجمعية في المجتمع المحلي وبناء شراكات مؤثرة مع الجهات ذات العلاقة.",
     ["إبرام 20 اتفاقية شراكة مع مدارس ومؤسسات تعليمية",
      "تنفيذ 50 برنامجاً مجتمعياً سنوياً في الأحياء والقرى",
      "استهداف فئة الشباب بـ 100 برنامج متخصص سنوياً",
      "تأسيس شبكة تطوع دعوي بـ 500 متطوع فاعل"]),
    ("المحور السادس: الاستدامة المالية",
     "بناء قاعدة مالية متنوعة ومستدامة تضمن استمرارية العمل الدعوي وتوسعه.",
     ["تنويع مصادر التمويل لتشمل الوقف والتبرعات والرعاية",
      "تأسيس صندوق وقفي خاص بالجمعية بحلول 2027م",
      "استقطاب 10 مليون ريال من رعايا الأعمال والمحسنين",
      "تحقيق الاستدامة المالية الذاتية بنسبة 40% بحلول 2030م"]),
]

for i, (title, desc, goals) in enumerate(strategic_goals):
    color = DARK_GREEN if i % 2 == 0 else MED_GREEN
    # Title box
    t_data = [[Paragraph(ar(title), ParagraphStyle(
        'gt', fontName='ArabicBold', fontSize=13, textColor=WHITE,
        alignment=TA_CENTER, leading=22))]]
    t_box = Table(t_data, colWidths=[17*cm])
    t_box.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), color),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_box)
    story.append(Paragraph(ar(desc), styles['body']))
    for g in goals:
        story.append(bullet_item(g, styles))
    story.append(Spacer(1, 0.3*cm))

story.append(PageBreak())

# ══════════════════════════════════════════════════════════════
# CHAPTER 5: IMPLEMENTATION PLAN
# ══════════════════════════════════════════════════════════════
story += chapter_header("الفصل الخامس: خطة التنفيذ والجداول الزمنية", styles)

story += section_title("مراحل تنفيذ الخطة الاستراتيجية", styles)

phases_data = [
    [Paragraph(ar("المرحلة"), styles['table_header']),
     Paragraph(ar("الفترة الزمنية"), styles['table_header']),
     Paragraph(ar("المحتوى والأولويات"), styles['table_header']),
     Paragraph(ar("المخرجات الرئيسية"), styles['table_header'])],
    [Paragraph(ar("التأسيس والبناء"), styles['table_cell']),
     Paragraph(ar("2025م"), styles['table_cell']),
     Paragraph(ar("إعداد البنية التحتية، وتشكيل الفرق، وإطلاق الأنظمة"), styles['table_cell']),
     Paragraph(ar("هيكل تنظيمي + نظام إداري"), styles['table_cell'])],
    [Paragraph(ar("الانطلاق والتوسع"), styles['table_cell']),
     Paragraph(ar("2026م"), styles['table_cell']),
     Paragraph(ar("إطلاق البرامج الرئيسية والمنصة الرقمية والشراكات"), styles['table_cell']),
     Paragraph(ar("50 برنامجاً + منصة رقمية"), styles['table_cell'])],
    [Paragraph(ar("النمو والتطوير"), styles['table_cell']),
     Paragraph(ar("2027م"), styles['table_cell']),
     Paragraph(ar("توسيع نطاق التغطية الجغرافية وزيادة المستفيدين"), styles['table_cell']),
     Paragraph(ar("مركز تدريب + صندوق وقفي"), styles['table_cell'])],
    [Paragraph(ar("الريادة والتميز"), styles['table_cell']),
     Paragraph(ar("2028-2029م"), styles['table_cell']),
     Paragraph(ar("ترسيخ الريادة الدعوية وتصدير التجربة"), styles['table_cell']),
     Paragraph(ar("جوائز + نموذج قابل للتكرار"), styles['table_cell'])],
    [Paragraph(ar("الاستدامة والإرث"), styles['table_cell']),
     Paragraph(ar("2030م"), styles['table_cell']),
     Paragraph(ar("تقييم شامل وإعداد الخطة الاستراتيجية التالية"), styles['table_cell']),
     Paragraph(ar("تقرير إنجاز شامل + خطة 2035"), styles['table_cell'])],
]
phases_table = Table(phases_data, colWidths=[3.5*cm, 2.5*cm, 6.5*cm, 4.5*cm])
phases_table.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), DARK_GREEN),
    ('ROWBACKGROUNDS', (0,1), (-1,-1), [LIGHT_GREEN, WHITE]),
    ('ALIGN', (0,0), (-1,-1), 'CENTER'),
    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ('TOPPADDING', (0,0), (-1,-1), 8),
    ('BOTTOMPADDING', (0,0), (-1,-1), 8),
    ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
]))
story.append(phases_table)
story.append(PageBreak())

# ══════════════════════════════════════════════════════════════
# CHAPTER 6: KPIs
# ══════════════════════════════════════════════════════════════
story += chapter_header("الفصل السادس: مؤشرات الأداء الرئيسية (KPIs)", styles)

story += section_title("المؤشرات الاستراتيجية للقياس والمتابعة", styles)

kpi_data = [
    [Paragraph(ar("المؤشر"), styles['table_header']),
     Paragraph(ar("الوضع الحالي"), styles['table_header']),
     Paragraph(ar("المستهدف 2027"), styles['table_header']),
     Paragraph(ar("المستهدف 2030"), styles['table_header']),
     Paragraph(ar("آلية القياس"), styles['table_header'])],
    [Paragraph(ar("عدد المستفيدين السنويين"), styles['table_cell']),
     Paragraph(ar("20,000"), styles['table_cell']),
     Paragraph(ar("80,000"), styles['table_cell']),
     Paragraph(ar("200,000"), styles['table_cell']),
     Paragraph(ar("تقارير دورية"), styles['table_cell'])],
    [Paragraph(ar("عدد البرامج الدعوية"), styles['table_cell']),
     Paragraph(ar("30 برنامجاً"), styles['table_cell']),
     Paragraph(ar("80 برنامجاً"), styles['table_cell']),
     Paragraph(ar("150 برنامجاً"), styles['table_cell']),
     Paragraph(ar("سجل البرامج"), styles['table_cell'])],
    [Paragraph(ar("الكوادر المدربة"), styles['table_cell']),
     Paragraph(ar("40 داعية"), styles['table_cell']),
     Paragraph(ar("200 داعية"), styles['table_cell']),
     Paragraph(ar("500 داعية"), styles['table_cell']),
     Paragraph(ar("قاعدة البيانات"), styles['table_cell'])],
    [Paragraph(ar("التواجد الرقمي (متابع)"), styles['table_cell']),
     Paragraph(ar("5,000"), styles['table_cell']),
     Paragraph(ar("50,000"), styles['table_cell']),
     Paragraph(ar("150,000"), styles['table_cell']),
     Paragraph(ar("تقارير المنصات"), styles['table_cell'])],
    [Paragraph(ar("الشراكات الفاعلة"), styles['table_cell']),
     Paragraph(ar("5"), styles['table_cell']),
     Paragraph(ar("20"), styles['table_cell']),
     Paragraph(ar("40"), styles['table_cell']),
     Paragraph(ar("سجل الاتفاقيات"), styles['table_cell'])],
    [Paragraph(ar("رضا المستفيدين"), styles['table_cell']),
     Paragraph(ar("70%"), styles['table_cell']),
     Paragraph(ar("85%"), styles['table_cell']),
     Paragraph(ar("95%"), styles['table_cell']),
     Paragraph(ar("استبانات دورية"), styles['table_cell'])],
    [Paragraph(ar("نسبة الاستدامة المالية"), styles['table_cell']),
     Paragraph(ar("10%"), styles['table_cell']),
     Paragraph(ar("25%"), styles['table_cell']),
     Paragraph(ar("40%"), styles['table_cell']),
     Paragraph(ar("التقرير المالي"), styles['table_cell'])],
]
kpi_table = Table(kpi_data, colWidths=[4*cm, 2.5*cm, 3*cm, 3*cm, 4.5*cm])
kpi_table.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), DARK_GREEN),
    ('ROWBACKGROUNDS', (0,1), (-1,-1), [LIGHT_GREEN, WHITE]),
    ('ALIGN', (0,0), (-1,-1), 'CENTER'),
    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ('TOPPADDING', (0,0), (-1,-1), 7),
    ('BOTTOMPADDING', (0,0), (-1,-1), 7),
    ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
    ('FONTSIZE', (0,0), (-1,-1), 9),
]))
story.append(kpi_table)
story.append(PageBreak())

# ══════════════════════════════════════════════════════════════
# CHAPTER 7: BUDGET
# ══════════════════════════════════════════════════════════════
story += chapter_header("الفصل السابع: الميزانية التقديرية", styles)

story += section_title("توزيع الميزانية على المحاور الاستراتيجية", styles)

budget_data = [
    [Paragraph(ar("المحور الاستراتيجي"), styles['table_header']),
     Paragraph(ar("النسبة"), styles['table_header']),
     Paragraph(ar("المبلغ التقديري (ريال)"), styles['table_header'])],
    [Paragraph(ar("التمكين المؤسسي والبنية التحتية"), styles['table_cell']),
     Paragraph(ar("15%"), styles['table_cell']),
     Paragraph(ar("5,250,000"), styles['table_cell'])],
    [Paragraph(ar("البرامج الدعوية والتوعية الدينية"), styles['table_cell']),
     Paragraph(ar("30%"), styles['table_cell']),
     Paragraph(ar("10,500,000"), styles['table_cell'])],
    [Paragraph(ar("الدعوة الرقمية والإعلامية"), styles['table_cell']),
     Paragraph(ar("20%"), styles['table_cell']),
     Paragraph(ar("7,000,000"), styles['table_cell'])],
    [Paragraph(ar("التعليم والتأهيل الشرعي"), styles['table_cell']),
     Paragraph(ar("18%"), styles['table_cell']),
     Paragraph(ar("6,300,000"), styles['table_cell'])],
    [Paragraph(ar("خدمة المجتمع والشراكات"), styles['table_cell']),
     Paragraph(ar("12%"), styles['table_cell']),
     Paragraph(ar("4,200,000"), styles['table_cell'])],
    [Paragraph(ar("الاستدامة المالية والتطوير"), styles['table_cell']),
     Paragraph(ar("5%"), styles['table_cell']),
     Paragraph(ar("1,750,000"), styles['table_cell'])],
    [Paragraph(ar("الإجمالي"), ParagraphStyle(
        'bt', fontName='ArabicBold', fontSize=11, textColor=WHITE,
        alignment=TA_CENTER, leading=18)),
     Paragraph(ar("100%"), ParagraphStyle(
        'bt2', fontName='ArabicBold', fontSize=11, textColor=WHITE,
        alignment=TA_CENTER, leading=18)),
     Paragraph(ar("35,000,000"), ParagraphStyle(
        'bt3', fontName='ArabicBold', fontSize=11, textColor=GOLD,
        alignment=TA_CENTER, leading=18))],
]
budget_table = Table(budget_data, colWidths=[8*cm, 3*cm, 6*cm])
budget_table.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), DARK_GREEN),
    ('ROWBACKGROUNDS', (0,1), (-1,-2), [LIGHT_GREEN, WHITE]),
    ('BACKGROUND', (0,-1), (-1,-1), DARK_GREEN),
    ('ALIGN', (0,0), (-1,-1), 'CENTER'),
    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ('TOPPADDING', (0,0), (-1,-1), 9),
    ('BOTTOMPADDING', (0,0), (-1,-1), 9),
    ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
]))
story.append(budget_table)
story.append(Spacer(1, 0.5*cm))

story += section_title("مصادر التمويل المتوقعة", styles)
funding_items = [
    "الدعم الحكومي من وزارة الشؤون الإسلامية والدعوة والإرشاد: 40%",
    "التبرعات والمنح من المحسنين ورجال الأعمال: 30%",
    "عوائد الأوقاف والاستثمارات الخيرية: 15%",
    "رسوم البرامج والخدمات التدريبية: 10%",
    "الرعايات والشراكات مع القطاع الخاص: 5%",
]
for item in funding_items:
    story.append(bullet_item(item, styles))
story.append(PageBreak())

# ══════════════════════════════════════════════════════════════
# CHAPTER 8: RISKS
# ══════════════════════════════════════════════════════════════
story += chapter_header("الفصل الثامن: إدارة المخاطر", styles)

story += section_title("المخاطر الرئيسية وخطط المواجهة", styles)

risks_data = [
    [Paragraph(ar("المخاطرة"), styles['table_header']),
     Paragraph(ar("الاحتمالية"), styles['table_header']),
     Paragraph(ar("الأثر"), styles['table_header']),
     Paragraph(ar("خطة المواجهة"), styles['table_header'])],
    [Paragraph(ar("شُح التمويل"), styles['table_cell']),
     Paragraph(ar("متوسطة"), styles['table_cell']),
     Paragraph(ar("عالٍ"), styles['table_cell']),
     Paragraph(ar("تنويع المصادر وبناء الاحتياطي المالي"), styles['table_cell'])],
    [Paragraph(ar("نقص الكوادر المؤهلة"), styles['table_cell']),
     Paragraph(ar("متوسطة"), styles['table_cell']),
     Paragraph(ar("عالٍ"), styles['table_cell']),
     Paragraph(ar("برامج تدريب مستمرة وخطط تعاقب وظيفي"), styles['table_cell'])],
    [Paragraph(ar("التحولات الاجتماعية السريعة"), styles['table_cell']),
     Paragraph(ar("عالية"), styles['table_cell']),
     Paragraph(ar("متوسط"), styles['table_cell']),
     Paragraph(ar("مرونة البرامج وإعادة التصميم الدوري"), styles['table_cell'])],
    [Paragraph(ar("المنافسة الرقمية السلبية"), styles['table_cell']),
     Paragraph(ar("عالية"), styles['table_cell']),
     Paragraph(ar("عالٍ"), styles['table_cell']),
     Paragraph(ar("تطوير المحتوى الجذاب وتوظيف الذكاء الاصطناعي"), styles['table_cell'])],
    [Paragraph(ar("التغييرات التنظيمية"), styles['table_cell']),
     Paragraph(ar("منخفضة"), styles['table_cell']),
     Paragraph(ar("متوسط"), styles['table_cell']),
     Paragraph(ar("المتابعة المستمرة للأنظمة والتعديل الفوري"), styles['table_cell'])],
]
risks_table = Table(risks_data, colWidths=[4.5*cm, 2.5*cm, 2.5*cm, 7.5*cm])
risks_table.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), DARK_GREEN),
    ('ROWBACKGROUNDS', (0,1), (-1,-1), [LIGHT_GREEN, WHITE]),
    ('ALIGN', (0,0), (-1,-1), 'CENTER'),
    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ('TOPPADDING', (0,0), (-1,-1), 8),
    ('BOTTOMPADDING', (0,0), (-1,-1), 8),
    ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
]))
story.append(risks_table)
story.append(PageBreak())

# ══════════════════════════════════════════════════════════════
# CHAPTER 9: GOVERNANCE
# ══════════════════════════════════════════════════════════════
story += chapter_header("الفصل التاسع: الحوكمة والمتابعة", styles)

story += section_title("هيكل الحوكمة الاستراتيجية", styles)
gov_items = [
    "مجلس الإدارة: مسؤول عن اعتماد الخطة ومتابعة تنفيذها بصفة ربع سنوية",
    "اللجنة الاستراتيجية: تراجع مؤشرات الأداء شهرياً وترفع التوصيات للإدارة",
    "فرق تنفيذ المحاور: مسؤولة عن التنفيذ اليومي وإعداد التقارير الأسبوعية",
    "وحدة الجودة والتقييم: تُجري المراجعات الدورية والتدقيق في الأداء",
    "المراجع الخارجي: يُقيّم مدى تحقق الأهداف سنوياً ويُقدّم تقريراً مستقلاً",
]
for item in gov_items:
    story.append(bullet_item(item, styles))
story.append(Spacer(1, 0.3*cm))

story += section_title("دورة المراجعة والتقييم", styles)
review_items = [
    "التقارير الأسبوعية: رصد التقدم الميداني ومعالجة العقبات الآنية",
    "التقارير الشهرية: مقارنة الأداء الفعلي بالمستهدفات وتحليل الفجوات",
    "التقارير الربع سنوية: مراجعة شاملة للمحاور وتعديل الخطط التنفيذية",
    "التقارير السنوية: تقييم استراتيجي شامل وإعادة ضبط الأهداف",
    "المراجعة الاستراتيجية المنتصفية: عام 2027م لإعادة تقييم الخطة بالكامل",
]
for item in review_items:
    story.append(bullet_item(item, styles))
story.append(PageBreak())

# ══════════════════════════════════════════════════════════════
# CLOSING
# ══════════════════════════════════════════════════════════════
story += chapter_header("خاتمة وتوصيات", styles)

story.append(Paragraph(ar(
    "إن نجاح هذه الخطة الاستراتيجية مرهون بالتزام جميع أصحاب المصلحة بمضمونها، "
    "وتوافر الإرادة المؤسسية على التنفيذ الفعلي، والمرونة في التكيف مع المتغيرات. "
    "ونؤمن بأن جمعية الدعوة الإسلامية في نجران قادرة على أن تكون نموذجاً ريادياً "
    "يُحتذى به في مجال العمل الدعوي المؤسسي على المستوى الوطني."
), styles['body']))
story.append(Spacer(1, 0.4*cm))

recommendations = [
    "إطلاق حملة توعية داخلية لتبني الخطة وزرع ثقافتها في نفوس العاملين",
    "تشكيل فريق قيادة التغيير لإدارة مرحلة التحول الاستراتيجي",
    "الاستثمار المبكر في التقنية والبنية التحتية الرقمية قبل انطلاق البرامج",
    "بناء قاعدة بيانات شاملة للمستفيدين والمتطوعين والشركاء",
    "تعزيز التواصل الدوري مع الجمهور المستهدف لقياس الأثر الحقيقي",
    "الاستفادة من تجارب الجمعيات الدعوية الناجحة محلياً وإقليمياً",
    "تضمين مفاهيم الاستدامة والمسؤولية الاجتماعية في جميع برامج الجمعية",
]
for item in recommendations:
    story.append(bullet_item(item, styles))

story.append(Spacer(1, 0.8*cm))
final_box = Table([[Paragraph(ar(
    "نسأل الله التوفيق والسداد، وأن يجعل هذا العمل خالصاً لوجهه الكريم،"
    " وأن ينفع به الإسلام والمسلمين في منطقة نجران وسائر البلاد"
), ParagraphStyle('fb', fontName='ArabicBold', fontSize=13, textColor=WHITE,
    alignment=TA_CENTER, leading=24))]], colWidths=[17*cm])
final_box.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,-1), DARK_GREEN),
    ('TOPPADDING', (0,0), (-1,-1), 16),
    ('BOTTOMPADDING', (0,0), (-1,-1), 16),
    ('ROUNDEDCORNERS', [8]),
]))
story.append(final_box)

# ── Build PDF ──────────────────────────────────────────────────────────────────
doc.build(story)
print(f"PDF created: {output_path}")
