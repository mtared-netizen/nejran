# -*- coding: utf-8 -*-
"""
تقرير تشخيص واقع جمعية بصائر - إعداد د. مطارد بن دخيل العنزي - إبريل 2026
"""
import math, sys
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import arabic_reshaper, unicodedata
from bidi.algorithm import get_display

# ─── FONTS ───────────────────────────────────────────────────────────────────
UF  = "C:/Users/mtare/AppData/Local/Microsoft/Windows/Fonts/"
WF  = "C:/Windows/Fonts/"
def reg(name, path):
    try: pdfmetrics.registerFont(TTFont(name, path))
    except: pass

reg("Cairo-Regular",   UF+"Cairo-Regular.ttf")
reg("Cairo-Medium",    UF+"Cairo-Medium.ttf")
reg("Cairo-SemiBold",  UF+"Cairo-SemiBold.ttf")
reg("Cairo-Bold",      UF+"Cairo-Bold.ttf")
reg("Cairo-ExtraBold", UF+"Cairo-ExtraBold.ttf")
reg("Cairo-Black",     UF+"Cairo-Black.ttf")
reg("DIN-Regular",     UF+"ArbFONTS-DINNextLTArabic-Regular-3.ttf")
reg("DIN-Bold",        UF+"ArbFONTS-DINNextLTArabic-Bold-3.ttf")
reg("DIN-Light",       UF+"ArbFONTS-DINNextLTArabic-Light-3.ttf")
reg("DIN-Medium",      UF+"ArbFONTS-DINNextLTArabic-Medium-3.ttf")
reg("TradArabic",      WF+"trado.ttf")
reg("TradArabic-Bold", WF+"tradbdo.ttf")

# ─── COLOURS ─────────────────────────────────────────────────────────────────
NAVY      = colors.HexColor("#0D1B2A")
DKGREEN   = colors.HexColor("#0B3D2E")
GOLD      = colors.HexColor("#C9A84C")
LTGOLD    = colors.HexColor("#E8D5A3")
WHITE     = colors.HexColor("#FFFFFF")
LTGRAY    = colors.HexColor("#F4F5F7")
MIDGRAY   = colors.HexColor("#8A9BB0")
DKGRAY    = colors.HexColor("#2C3E50")
RED       = colors.HexColor("#C0392B")
TEAL      = colors.HexColor("#1A6B72")
AMBER     = colors.HexColor("#D4830A")

# ─── PAGE SETUP ──────────────────────────────────────────────────────────────
W, H  = A4
BLEED = 3*mm
MARGIN= 18*mm
CW    = W - 2*MARGIN
PW    = W
PH    = H

# ─── ARABIC TEXT HELPER ──────────────────────────────────────────────────────
# Cairo has no isolated presentation forms (FE8x/FExx isolated).
# Map every missing isolated form → its base Unicode character.
_ISO_FB = {
    '\uFE80':'\u0621','\uFE81':'\u0622','\uFE83':'\u0623',
    '\uFE85':'\u0624','\uFE87':'\u0625','\uFE89':'\u0626',
    '\uFE8D':'\u0627','\uFE8F':'\u0628','\uFE93':'\u0629',
    '\uFE95':'\u062A','\uFE99':'\u062B','\uFE9D':'\u062C',
    '\uFEA1':'\u062D','\uFEA5':'\u062E','\uFEA9':'\u062F',
    '\uFEAB':'\u0630','\uFEAD':'\u0631','\uFEAF':'\u0632',
    '\uFEB1':'\u0633','\uFEB5':'\u0634','\uFEB9':'\u0635',
    '\uFEBD':'\u0636','\uFEC1':'\u0637','\uFEC5':'\u0638',
    '\uFEC9':'\u0639','\uFECD':'\u063A','\uFED1':'\u0641',
    '\uFED5':'\u0642','\uFED9':'\u0643','\uFEDD':'\u0644',
    '\uFEE1':'\u0645','\uFEE5':'\u0646','\uFEE9':'\u0647',
    '\uFEED':'\u0648','\uFEEF':'\u0649','\uFEF1':'\u064A',
}

def ar(t):
    reshaped  = arabic_reshaper.reshape(str(t))
    displayed = get_display(reshaped)
    out = []
    for c in displayed:
        if unicodedata.category(c) in ('Cc', 'Cf'):
            continue
        out.append(_ISO_FB.get(c, c))
    return ''.join(out)

def txt(c, text, x, y, font="Cairo-Regular", size=10, color=WHITE, anchor="right"):
    c.setFont(font, size)
    c.setFillColor(color)
    s = ar(text)
    if   anchor=="right":  c.drawRightString(x, y, s)
    elif anchor=="center": c.drawCentredString(x, y, s)
    elif anchor=="left":   c.drawString(x, y, s)

def rect(c, x, y, w, h, fill=None, stroke=None, sw=0.5):
    c.setLineWidth(sw)
    if fill:   c.setFillColor(fill)
    if stroke: c.setStrokeColor(stroke)
    c.rect(x, y, w, h, fill=1 if fill else 0, stroke=1 if stroke else 0)

def line(c, x1, y1, x2, y2, color=GOLD, w=0.5):
    c.setStrokeColor(color)
    c.setLineWidth(w)
    c.line(x1, y1, x2, y2)

def islamic_star(c, cx, cy, r_out, r_in, n=12, alpha=0.05, col=GOLD):
    from reportlab.graphics.shapes import Polygon
    pts = []
    for i in range(2*n):
        a = math.pi/n * i - math.pi/2
        r = r_out if i%2==0 else r_in
        pts += [cx + r*math.cos(a), cy + r*math.sin(a)]
    c.saveState()
    c.setFillColor(col)
    c.setFillAlpha(alpha)
    c.setStrokeColor(col)
    c.setStrokeAlpha(alpha*0.5)
    c.setLineWidth(0.2)
    p = c.beginPath()
    p.moveTo(pts[0], pts[1])
    for i in range(2, len(pts), 2):
        p.lineTo(pts[i], pts[i+1])
    p.close()
    c.drawPath(p, fill=1, stroke=0)
    c.restoreState()

# ─── WRAPPED TEXT ────────────────────────────────────────────────────────────
def wrap_ar(c, text, x, y, w, font="Cairo-Regular", size=11, color=WHITE,
            line_h=None, align="right"):
    if line_h is None: line_h = size * 1.8
    words = text.split()
    lines, cur = [], []
    c.setFont(font, size)
    for word in words:
        test = " ".join(cur + [word])
        if c.stringWidth(ar(test), font, size) <= w:
            cur.append(word)
        else:
            if cur: lines.append(" ".join(cur))
            cur = [word]
    if cur: lines.append(" ".join(cur))
    cy = y
    for l in lines:
        txt(c, l, x, cy, font, size, color, align)
        cy -= line_h
    return cy  # bottom y after last line

# ─── HEADER / FOOTER ─────────────────────────────────────────────────────────
def header_footer(c, page_num, section=""):
    # top bar
    rect(c, 0, H-14*mm, W, 14*mm, fill=NAVY)
    # gold left accent
    rect(c, 0, H-14*mm, 4*mm, 14*mm, fill=GOLD)
    # association name right
    txt(c, "جمعية بصائر للدعوة والإرشاد وتوعية الجاليات — نجران",
        W-MARGIN, H-8.5*mm, "Cairo-SemiBold", 7.5, WHITE, "right")
    # section centre
    if section:
        txt(c, section, W/2, H-8.5*mm, "Cairo-Regular", 7, LTGOLD, "center")
    # year left
    txt(c, "2026م", MARGIN+10, H-8.5*mm, "Cairo-Regular", 7, MIDGRAY, "left")

    # bottom bar
    rect(c, 0, 0, W, 10*mm, fill=NAVY)
    rect(c, 0, 0, 4*mm, 10*mm, fill=GOLD)
    txt(c, f"إعداد: د. مطارد بن دخيل العنزي  |  إبريل 2026",
        W-MARGIN, 3.5*mm, "Cairo-Regular", 6.5, MIDGRAY, "right")
    txt(c, f"{page_num}", MARGIN+10, 3.5*mm, "Cairo-SemiBold", 7, GOLD, "left")
    line(c, 4*mm, 10*mm, W, 10*mm, GOLD, 0.4)

# ─── SECTION DIVIDER ─────────────────────────────────────────────────────────
def section_div(c, num_str, title_ar, sub_ar, page_num):
    rect(c, 0, 0, W, H, fill=NAVY)
    rect(c, 0, 0, W, H*0.35, fill=DKGREEN)
    islamic_star(c, W*0.15, H*0.65, 60, 30, 16, 0.08)
    islamic_star(c, W*0.85, H*0.35, 80, 40, 16, 0.06)
    islamic_star(c, W*0.5,  H*0.5,  40, 20, 12, 0.04)
    # big number
    c.setFont("Cairo-Black", 100)
    c.setFillColor(GOLD)
    c.setFillAlpha(0.12)
    c.drawCentredString(W/2, H*0.4, num_str)
    c.setFillAlpha(1)
    # gold rule
    rect(c, MARGIN, H*0.58, CW, 1.5, fill=GOLD)
    rect(c, MARGIN, H*0.56, 40, 3, fill=GOLD)
    # title
    txt(c, title_ar, W-MARGIN, H*0.65, "Cairo-Black", 28, WHITE, "right")
    txt(c, sub_ar,   W-MARGIN, H*0.55, "Cairo-Regular", 12, LTGOLD, "right")
    # page num
    txt(c, str(page_num), MARGIN+5, 15*mm, "Cairo-Regular", 9, MIDGRAY, "left")
    c.showPage()

# ─────────────────────────────────────────────────────────────────────────────
#  PAGE 1 — COVER
# ─────────────────────────────────────────────────────────────────────────────
def page_cover(c):
    LOGO_PATH = "c:/Users/mtare/Desktop/ابو عثمان/شعار بصائر.png"
    rect(c, 0, 0, W, H, fill=NAVY)
    # green lower band
    rect(c, 0, 0, W, H*0.36, fill=DKGREEN)
    # geometric patterns
    for cx_, cy_, ro, ri, nn in [
        (W*0.08, H*0.88, 60, 30, 16),
        (W*0.92, H*0.78, 50, 25, 14),
        (W*0.5,  H*0.94, 35, 18, 12),
        (W*0.05, H*0.44, 40, 20, 12),
        (W*0.95, H*0.27, 45, 22, 14),
    ]:
        islamic_star(c, cx_, cy_, ro, ri, nn, 0.07)

    # ── LOGO ──────────────────────────────────────────────────────
    logo_s  = 46*mm          # logo square size
    logo_x  = W/2 - logo_s/2
    logo_y  = H*0.725        # bottom of logo
    logo_cy = logo_y + logo_s/2

    # white circle frame behind logo
    c.saveState()
    c.setFillColor(WHITE)
    c.setStrokeColor(GOLD)
    c.setLineWidth(2)
    c.circle(W/2, logo_cy, logo_s/2 + 4*mm, fill=1, stroke=1)
    c.restoreState()

    # actual logo image
    try:
        c.drawImage(LOGO_PATH, logo_x, logo_y, logo_s, logo_s,
                    preserveAspectRatio=True, anchor='c', mask='auto')
    except Exception:
        txt(c, "بصائر", W/2, logo_cy, "Cairo-Black", 22, GOLD, "center")

    # ── TITLE BLOCK ───────────────────────────────────────────────
    # decorative gold lines framing the title block
    title_top = H*0.645
    line_gap  = 19*mm          # equal spacing between each line baseline

    rect(c, MARGIN+10*mm, title_top + 12*mm, CW-20*mm, 1.2, fill=GOLD)
    rect(c, MARGIN+10*mm, title_top - 3*line_gap - 10*mm, CW-20*mm, 1.2, fill=GOLD)

    txt(c, "تشخيص الواقع الحالي",
        W/2, title_top,              "TradArabic-Bold", 30, WHITE, "center")
    txt(c, "لجمعية الدعوة والإرشاد وتوعية",
        W/2, title_top - line_gap,   "TradArabic-Bold", 24, GOLD,  "center")
    txt(c, "الجاليات في نجران (بصائر)",
        W/2, title_top - 2*line_gap, "TradArabic-Bold", 24, GOLD,  "center")

    # gold rule
    rect(c, MARGIN, H*0.455, CW, 0.8, fill=GOLD)

    # ── AUTHOR & DATE ─────────────────────────────────────────────
    txt(c, "إعداد", W-MARGIN, H*0.415, "Cairo-Regular", 9, LTGOLD, "right")
    txt(c, "د. مطارد بن دخيل العنزي", W-MARGIN, H*0.36, "Cairo-Bold", 16, WHITE, "right")
    txt(c, "مستشار استراتيجي", W-MARGIN, H*0.315, "Cairo-Regular", 10, LTGOLD, "right")
    txt(c, "إبريل 2026م  |  المملكة العربية السعودية", W-MARGIN, H*0.265, "Cairo-Regular", 9, MIDGRAY, "right")

    # confidentiality badge
    rect(c, MARGIN, 18*mm, 60*mm, 12*mm, fill=GOLD)
    txt(c, "التقرير التشخيصي — المرحلة الأولى", MARGIN+59*mm, 22.5*mm, "Cairo-SemiBold", 7.5, NAVY, "right")

    c.showPage()

# ─────────────────────────────────────────────────────────────────────────────
#  TABLE OF CONTENTS
# ─────────────────────────────────────────────────────────────────────────────
def page_toc(c, pg):
    header_footer(c, pg, "فهرس المحتويات")
    rect(c, 0, H-14*mm-8*mm, W, 8*mm, fill=LTGRAY)
    txt(c, "فهرس المحتويات", W-MARGIN, H-18.5*mm, "Cairo-Bold", 16, NAVY, "right")
    line(c, MARGIN, H-24*mm, W-MARGIN, H-24*mm, GOLD, 1)

    entries = [
        ("01", "تمهيد وملخص تنفيذي",                        "3"),
        ("02", "لمحة عن الجمعية — الهوية والأهداف",          "5"),
        ("03", "الواقع الحالي — مؤشرات الجاليات والمسلمون الجدد", "7"),
        ("04", "برنامج متون — الإنجاز الأبرز",              "10"),
        ("05", "البرامج الدعوية والعلمية",                   "13"),
        ("06", "المشاريع الرمضانية والتطوع",                 "16"),
        ("07", "الإعلام والحضور الرقمي",                    "19"),
        ("08", "الحوكمة المؤسسية",                           "21"),
        ("09", "تحليل SWOT الموسع — 44 نقطة",               "23"),
        ("10", "التشخيص المعمق — الفجوات الست الحرجة",      "28"),
        ("11", "مقارنة البرامج بأهداف الجمعية",             "32"),
        ("12", "الخلاصة التشخيصية",                         "35"),
    ]

    y = H-28*mm
    for i, (num, title, p) in enumerate(entries):
        bg = LTGRAY if i%2==0 else WHITE
        rect(c, MARGIN, y-7*mm, CW, 9*mm, fill=bg)
        # number badge
        rect(c, W-MARGIN-13*mm, y-6*mm, 11*mm, 7*mm, fill=NAVY)
        txt(c, num, W-MARGIN-7.5*mm, y-3*mm, "Cairo-Bold", 8, GOLD, "center")
        # title
        txt(c, title, W-MARGIN-16*mm, y-2*mm, "Cairo-Regular", 11, DKGRAY, "right")
        # dots and page number
        txt(c, p, MARGIN+8*mm, y-2*mm, "Cairo-SemiBold", 11, NAVY, "left")
        # dot line
        line(c, MARGIN+14*mm, y-0.5*mm, W-MARGIN-17*mm, y-0.5*mm, LTGOLD, 0.3)
        # thin gold underline below entry
        line(c, MARGIN, y-7*mm, W-MARGIN, y-7*mm, GOLD, 0.4)
        y -= 10.5*mm

    # bottom KPI strip
    kpis = [
        ("931", "مسلم جديد منذ التأسيس"),
        ("2,559", "طالب متون 2025"),
        ("21,129", "ساعة تطوعية 2025"),
        ("93.08%", "نتيجة الحوكمة"),
    ]
    bw = CW/4
    bx = MARGIN
    by = 18*mm
    bh = 14*mm
    for val, label in kpis:
        rect(c, bx, by, bw-2, bh, fill=NAVY)
        txt(c, val,   bx+bw/2-1, by+bh-5.5*mm, "Cairo-Bold", 11, GOLD, "center")
        txt(c, label, bx+bw/2-1, by+2*mm,      "Cairo-Regular", 6, WHITE, "center")
        bx += bw

    c.showPage()

# ─────────────────────────────────────────────────────────────────────────────
#  EXECUTIVE SUMMARY
# ─────────────────────────────────────────────────────────────────────────────
def page_exec_summary(c, pg):
    header_footer(c, pg, "الملخص التنفيذي")
    rect(c, 0, H-14*mm-10*mm, W, 10*mm, fill=LTGRAY)
    txt(c, "الملخص التنفيذي", W-MARGIN, H-21*mm, "Cairo-Black", 18, NAVY, "right")
    line(c, MARGIN, H-24*mm, W-MARGIN, H-24*mm, GOLD, 1.2)

    intro = ("الحمد لله رب العالمين، والصلاة والسلام على أشرف الأنبياء والمرسلين نبينا محمد، "
             "وعلى آله وصحبه أجمعين، أما بعد: يأتي هذا التقرير التشخيصي لواقع جمعية الدعوة "
             "والإرشاد وتوعية الجاليات بنجران (بصائر) كخطوة تأسيسية تمثل المرحلة الأولى في مسار "
             "إعداد الخطة الاستراتيجية للجمعية. وقد استند هذا التشخيص إلى منهجية تحليل SWOT، "
             "التي تهدف إلى تحديد وتحليل نقاط القوة والضعف الداخلية، إلى جانب الفرص والتحديات "
             "الخارجية التي تؤثر على أداء الجمعية. كما تم بناء هذا التقرير اعتمادًا على مراجعة "
             "وتحليل البيانات والتقارير الرسمية المنشورة خلال الفترة من عام 2019م إلى 2025م.")
    wrap_ar(c, intro, W-MARGIN, H-31*mm, CW, "Cairo-Regular", 10, DKGRAY, 18, "right")

    # OVERALL VERDICT BOX
    rect(c, MARGIN, H*0.61, CW, 32*mm, fill=NAVY)
    rect(c, MARGIN, H*0.61, 4, 32*mm, fill=GOLD)
    txt(c, "الحكم التشخيصي الإجمالي", W-MARGIN-4, H*0.61+27*mm,
        "Cairo-Bold", 10, GOLD, "right")
    verdict = ("جمعية بصائر في مرحلة التحول الهوياتي غير المُعلن — من جمعية دعوة مباشرة "
               "للجاليات إلى مؤسسة تعليمية علمية. هذا التحول يُقلّص إسلام الجاليات 85% "
               "لكنه يُضاعف طلاب متون 891%. الجمعية تمتلك مقومات استثنائية لكنها لا تُحوِّل "
               "إنجازها إلى أثر مقيس — ولا تعرف بالضبط أين تريد أن تكون بعد خمس سنوات.")
    wrap_ar(c, verdict, W-MARGIN-6, H*0.61+21*mm, CW-10, "Cairo-Regular", 10, WHITE, 18, "right")

    # KPI GRID
    kpi_data = [
        (DKGREEN,  "11",     "مسلم جديد 2025",      "↓ 85% منذ 2019"),
        (NAVY,     "2,559",  "طالب متون 2025",       "↑ 891% منذ 2019"),
        (TEAL,     "21,129", "ساعة تطوعية 2025",     "↑ مستمر منذ 2022"),
        (AMBER,    "58,000", "مستفيد تفطير 2024",    "↑ الذروة"),
        (DKGREEN,  "93.08%", "الحوكمة المؤسسية",     "متميز ومستدام"),
        (NAVY,     "931",    "مسلم منذ التأسيس",     "11 جنسية"),
    ]
    cols, rows = 3, 2
    kw = CW/cols - 2*mm
    kh = 22*mm
    kx0 = MARGIN
    ky0 = H*0.38
    for i, (col, val, lbl, sub) in enumerate(kpi_data):
        r, c_ = divmod(i, cols)
        kx = kx0 + c_*(kw+2*mm)
        ky = ky0 - r*(kh+2*mm)
        rect(c, kx, ky, kw, kh, fill=col)
        rect(c, kx, ky+kh-2, kw, 2, fill=GOLD)
        txt(c, val, kx+kw/2, ky+kh-10*mm, "Cairo-Black", 15, WHITE, "center")
        txt(c, lbl, kx+kw/2, ky+3.5*mm,   "Cairo-SemiBold", 7,  WHITE, "center")
        txt(c, sub, kx+kw/2, ky+1*mm,     "Cairo-Regular",  6,  LTGOLD,"center")

    # bottom quote
    rect(c, MARGIN, 12*mm, CW, 12*mm, fill=LTGRAY)
    rect(c, MARGIN, 12*mm, 3,  12*mm, fill=GOLD)
    wrap_ar(c, "الجمعية ليست ضعيفة الأداء — هي ضعيفة القصد الاستراتيجي الواعي.",
            W-MARGIN-5, 20*mm, CW-10, "Cairo-Bold", 10.5, DKGRAY, 17, "right")

    c.showPage()

# ─────────────────────────────────────────────────────────────────────────────
#  ORGANIZATION OVERVIEW
# ─────────────────────────────────────────────────────────────────────────────
def page_org_overview(c, pg):
    header_footer(c, pg, "لمحة عن الجمعية")
    txt(c, "لمحة عن جمعية بصائر — الهوية والأهداف", W-MARGIN, H-19*mm,
        "Cairo-Black", 15, NAVY, "right")
    line(c, MARGIN, H-24*mm, W-MARGIN, H-24*mm, GOLD, 1)

    # Identity cards row
    info = [
        ("الاسم الرسمي", "جمعية الدعوة والإرشاد وتوعية الجاليات بنجران"),
        ("الاسم المختصر", "بصائر"),
        ("رقم التسجيل", "3138"),
        ("المقر الرئيسي", "شارع الملك عبد العزيز، نجران"),
        ("الهاتف", "0175233139"),
        ("المنطقة", "منطقة نجران — الحد الجنوبي"),
    ]
    iw = CW/2 - 2*mm
    ix = [MARGIN, MARGIN+iw+2*mm]
    iy = H-27*mm
    for i, (lbl, val) in enumerate(info):
        col = i%2
        row = i//2
        bx = ix[col]
        by = iy - row*12*mm
        rect(c, bx, by-9*mm, iw, 10*mm, fill=LTGRAY)
        rect(c, bx, by-9*mm, 3,  10*mm, fill=GOLD)
        txt(c, lbl, bx+iw-3, by-2.5*mm, "Cairo-Regular", 8.5, MIDGRAY, "right")
        txt(c, val, bx+iw-3, by-6.5*mm, "Cairo-SemiBold", 10, NAVY,  "right")

    # المادة الخامسة
    y5 = H-62*mm
    rect(c, MARGIN, y5-5*mm, CW, 8*mm, fill=NAVY)
    txt(c, "المادة الخامسة — أهداف الجمعية الأساسية (اللائحة المعتمدة)",
        W-MARGIN-4, y5-2.5*mm, "Cairo-Bold", 10, GOLD, "right")

    objectives = [
        ("الهدف الأول",
         "نشر العلم الشرعي، وتبصير المسلمين بأمور دينهم عقيدةً وعبادةً ومعاملةً وأخلاقاً، "
         "مع العمل على تأهيل الدعاة القادرين على تبليغِ ذلك."),
        ("الهدف الثاني",
         "دعوة الوافدين غير المسلمين للإسلام وتعريفهم به، وتبصير الوافدين المسلمين "
         "بأمور دينهم وتصحيح مخالفاتهم العقدية، عبر البرامج والأنشطة كالحج والعمرة "
         "وإفطار الصائم ومعايدة الجاليات وكسوة الشتاء وما في حكمها."),
        ("الهدف الثالث",
         "ربط الناس بمنهج السلف الصالح، ونشر الوسطية والاعتدال، وتعزيز الأمن الفكري، "
         "وحماية المجتمع من الغلو والتطرف، وتعزيز اللحمة الوطنية والانتماء والمواطنة."),
        ("الهدف الرابع",
         "استخدام التقنية الحديثة بجميع أنواعها في نشر العلم الشرعي، وفي الدعوة إلى الله "
         "عزّ وجلّ في جميع مجالاتها، وفي تحقيق جميع أهداف الجمعية."),
    ]
    cy = y5 - 8*mm
    for i, (title, desc) in enumerate(objectives):
        bg = LTGRAY if i%2==0 else WHITE
        rect(c, MARGIN, cy-18*mm, CW, 19*mm, fill=bg)
        # number circle
        c.setFillColor(NAVY)
        c.circle(MARGIN+7*mm, cy-9*mm, 5*mm, fill=1, stroke=0)
        c.setFillColor(GOLD)
        c.setFont("Cairo-Bold", 7)
        c.drawCentredString(MARGIN+7*mm, cy-10.5*mm, str(i+1))
        txt(c, title, W-MARGIN-4, cy-4*mm,  "Cairo-Bold", 8.5, NAVY, "right")
        wrap_ar(c, desc, W-MARGIN-4, cy-10*mm, CW-16*mm, "Cairo-Regular", 9.5, DKGRAY, 17, "right")
        cy -= 21*mm

    # governance quick stats
    rect(c, MARGIN, 12*mm, CW, 14*mm, fill=DKGREEN)
    stats = [("تأسست","2016م"),("الموظفون","محدودون"),("المتطوعون","164 نشط"),
             ("الحوكمة","93.08%"),("الجنسيات المخدومة","11 جنسية")]
    sw = CW/len(stats)
    for i,(l,v) in enumerate(stats):
        sx = MARGIN + i*sw
        line(c, sx+sw, 12*mm, sx+sw, 26*mm, WHITE, 0.3)
        txt(c, v, sx+sw/2, 21*mm, "Cairo-Bold", 10, GOLD, "center")
        txt(c, l, sx+sw/2, 14*mm, "Cairo-Regular", 8, WHITE, "center")

    c.showPage()

# ─────────────────────────────────────────────────────────────────────────────
#  BAR CHART HELPER
# ─────────────────────────────────────────────────────────────────────────────
def bar_chart(c, x, y, w, h, years, values, title,
              bar_col=DKGREEN, highlight_col=GOLD,
              show_trend=False, y_label=""):
    mx = max(v for v in values if v is not None and v > 0) if values else 1
    if mx == 0: mx = 1
    bw = w / (len(years)*1.6)
    gap = w / len(years) - bw
    cx = x

    # title
    txt(c, title, x+w, y+h+5*mm, "Cairo-Bold", 9, NAVY, "right")
    # axes
    line(c, x, y, x, y+h, MIDGRAY, 0.5)
    line(c, x, y, x+w, y, MIDGRAY, 0.5)
    # horizontal grid lines
    for gi in range(1, 5):
        gy = y + h*gi/4
        line(c, x, gy, x+w, gy, LTGRAY, 0.3)
        gv = mx*gi/4
        lbl = f"{gv:,.0f}"
        txt(c, lbl, x-1*mm, gy-1.5*mm, "Cairo-Regular", 5.5, MIDGRAY, "right")

    bar_xs = []
    bar_ys = []
    for i, (yr, val) in enumerate(zip(years, values)):
        bx = x + i*(bw+gap) + gap/2
        if val is None or val == 0:
            bar_xs.append(bx+bw/2); bar_ys.append(y)
            txt(c, str(yr)[-2:], bx+bw/2, y-4*mm, "Cairo-Regular", 5.5, MIDGRAY, "center")
            continue
        bh2 = (val/mx)*h
        col = highlight_col if val == max(v for v in values if v) else bar_col
        rect(c, bx, y, bw, bh2, fill=col)
        # value label
        txt(c, f"{val:,}", bx+bw/2, y+bh2+1*mm, "Cairo-Regular", 5.5, NAVY, "center")
        txt(c, str(yr)[-2:], bx+bw/2, y-4*mm, "Cairo-Regular", 5.5, DKGRAY, "center")
        bar_xs.append(bx+bw/2); bar_ys.append(y+bh2)

    if show_trend and len(bar_xs) >= 2:
        c.setStrokeColor(RED)
        c.setLineWidth(0.8)
        c.setLineCap(1)
        p = c.beginPath()
        first = True
        for bx, bys in zip(bar_xs, bar_ys):
            if first: p.moveTo(bx, bys); first=False
            else: p.lineTo(bx, bys)
        c.drawPath(p, fill=0, stroke=1)

# ─────────────────────────────────────────────────────────────────────────────
#  LINE CHART HELPER
# ─────────────────────────────────────────────────────────────────────────────
def line_chart(c, x, y, w, h, years, series, title):
    """series = list of (label, values, color)"""
    all_vals = [v for s in series for v in s[1] if v is not None and v > 0]
    mx = max(all_vals) if all_vals else 1
    if mx == 0: mx = 1
    n = len(years)
    step = w / (n - 1) if n > 1 else w
    txt(c, title, x+w, y+h+5*mm, "Cairo-Bold", 9, NAVY, "right")
    line(c, x, y, x, y+h, MIDGRAY, 0.5)
    line(c, x, y, x+w, y, MIDGRAY, 0.5)
    for gi in range(1, 5):
        gy = y + h*gi/4
        line(c, x, gy, x+w, gy, LTGRAY, 0.3)
        gv = mx*gi/4
        txt(c, f"{gv:,.0f}", x-1*mm, gy-1.5*mm, "Cairo-Regular", 5.5, MIDGRAY, "right")
    for yr, i in zip(years, range(n)):
        px = x + i*step
        txt(c, str(yr)[-2:], px, y-4*mm, "Cairo-Regular", 5.5, DKGRAY, "center")
    for lbl, vals, col in series:
        pts = []
        for i, val in enumerate(vals):
            if val is None or val == 0:
                if pts:
                    draw_line_pts(c, pts, col)
                    pts = []
            else:
                px = x + i*step
                py = y + (val/mx)*h
                pts.append((px, py))
        if pts: draw_line_pts(c, pts, col)
    # legend
    lx = x + w
    for i, (lbl, _, col) in enumerate(series):
        rect(c, lx - 35*mm, y+h - i*7*mm - 5*mm, 4*mm, 3*mm, fill=col)
        txt(c, lbl, lx - 32*mm + 4*mm, y+h - i*7*mm - 4*mm, "Cairo-Regular", 6, DKGRAY, "left")

def draw_line_pts(c, pts, col):
    if len(pts) < 2:
        if pts:
            c.setFillColor(col)
            c.circle(pts[0][0], pts[0][1], 1.5*mm, fill=1, stroke=0)
        return
    c.setStrokeColor(col)
    c.setLineWidth(1.2)
    p = c.beginPath()
    p.moveTo(pts[0][0], pts[0][1])
    for px, py in pts[1:]: p.lineTo(px, py)
    c.drawPath(p, fill=0, stroke=1)
    for px, py in pts:
        c.setFillColor(col)
        c.circle(px, py, 1.5*mm, fill=1, stroke=0)

# ─────────────────────────────────────────────────────────────────────────────
#  ANALYSIS BOX
# ─────────────────────────────────────────────────────────────────────────────
def analysis_box(c, x, y, w, text, title="التحليل", max_h=None):
    lines_est = len(text)//55 + 4
    bh = min(lines_est*14*mm, max_h or 75*mm)
    rect(c, x, y-bh, w, bh, fill=LTGRAY)
    rect(c, x+w-3, y-bh, 3, bh, fill=DKGREEN)
    rect(c, x, y-8*mm, w, 8*mm, fill=DKGREEN)
    txt(c, title, x+w-5, y-5*mm, "Cairo-Bold", 10.5, WHITE, "right")
    wrap_ar(c, text, x+w-5, y-13*mm, w-10, "Cairo-Regular", 10, DKGRAY, 18, "right")
    return y - bh

# ─────────────────────────────────────────────────────────────────────────────
#  SECTION 3 — NEW MUSLIMS
# ─────────────────────────────────────────────────────────────────────────────
def page_new_muslims(c, pg):
    header_footer(c, pg, "مؤشر المسلمون الجدد")
    txt(c, "محور الجاليات — المسلمون الجدد 2019–2025",
        W-MARGIN, H-21*mm, "Cairo-Black", 15, NAVY, "right")
    line(c, MARGIN, H-24*mm, W-MARGIN, H-24*mm, GOLD, 1)

    years  = [2019,2020,2021,2022,2023,2024,2025]
    muslims= [72, 49, 34, 42, 55, 14, 11]

    # Main bar chart
    bar_chart(c, MARGIN, H-100*mm, CW*0.62, 62*mm,
              years, muslims,
              "المسلمون الجدد سنوياً (2019–2025)",
              bar_col=DKGREEN, highlight_col=GOLD, show_trend=True)

    # Stat boxes right side
    st_data = [
        ("72", "أعلى قيمة\n2019"),
        ("11", "أدنى قيمة\n2025"),
        ("85%", "نسبة التراجع"),
        ("931", "إجمالي منذ\nالتأسيس"),
    ]
    sbx = MARGIN + CW*0.65
    sby = H-40*mm
    sbw = CW*0.33
    sbh = 13*mm
    for val, lbl in st_data:
        rect(c, sbx, sby, sbw, sbh, fill=NAVY)
        txt(c, val, sbx+sbw/2, sby+sbh-5.5*mm, "Cairo-Black", 14, GOLD, "center")
        txt(c, lbl.replace("\n"," "), sbx+sbw/2, sby+1.5*mm, "Cairo-Regular", 6, WHITE, "center")
        sby -= sbh+2*mm

    # DATA TABLE
    ty = H-108*mm
    rect(c, MARGIN, ty-7*mm, CW, 7*mm, fill=NAVY)
    headers = ["2025","2024","2023","2022","2021","2020","2019","السنة"]
    col_w = CW/len(headers)
    for i, h_ in enumerate(headers):
        tx = MARGIN + (len(headers)-1-i)*col_w + col_w/2
        txt(c, h_, tx, ty-4.5*mm, "Cairo-Bold", 7, GOLD, "center")
    ty -= 7*mm
    values_row = ["11","14","55","42","34","49","72","المسلمون الجدد"]
    rect(c, MARGIN, ty-7*mm, CW, 7*mm, fill=LTGRAY)
    for i, v in enumerate(values_row):
        tx = MARGIN + (len(values_row)-1-i)*col_w + col_w/2
        color = RED if v in ["11","14"] else DKGREEN if v in ["72","55"] else DKGRAY
        if v == "المسلمون الجدد": color = NAVY
        txt(c, v, tx, ty-4.5*mm, "Cairo-SemiBold", 8.5, color, "center")
    ty -= 7*mm

    # beneficiaries row
    rect(c, MARGIN, ty-7*mm, CW, 7*mm, fill=WHITE)
    ben = ["2,598","2,294","1,182","300","—","1,538","800","مستفيدو البرامج"]
    for i, v in enumerate(ben):
        tx = MARGIN + (len(ben)-1-i)*col_w + col_w/2
        col_ = DKGRAY if v != "مستفيدو البرامج" else NAVY
        txt(c, v, tx, ty-4.5*mm, "Cairo-Regular", 8.5, col_, "center")
    ty -= 8*mm

    # Analysis
    analysis = ("يُعدّ تراجع أعداد المسلمين الجدد من 72 عام 2019 إلى 11 عام 2025 — بنسبة انخفاض "
                "بلغت 85% — المؤشرَ الأكثر حساسية وخطورة في أداء الجمعية. "
                "إذ إن هذا المؤشر يمثل الهوية التأسيسية للجمعية، وهو المحور الذي يُسوَّغ به وجودها. "
                "والملاحظ أن المسار لم يكن تراجعاً خطياً مستمراً؛ بل شهد ارتداداً إيجابياً في 2022-2023 "
                "وصل إلى 55، قبل أن ينهار بشكل حاد إلى 14 في 2024 و11 في 2025. "
                "هذا التذبذب يكشف بجلاء أن الأثر مرتبط بجهود أشخاص بعينهم، لا بمنظومة مؤسسية "
                "مستدامة. حين يكون الشخص نشيطاً ترتفع الأرقام، وحين يغيب تنهار — وهذا هو تعريف "
                "الهشاشة المؤسسية بدقة. في المقابل، بلغ إجمالي المسلمين الجدد منذ التأسيس 931 "
                "مسلماً ومسلمة من 11 جنسية، وهو رصيد تراكمي يستحق التوثيق والبناء عليه.")
    analysis_box(c, MARGIN, ty-2*mm, CW, analysis, "التحليل التشخيصي")

    c.showPage()

# ─────────────────────────────────────────────────────────────────────────────
#  SECTION 4 — MUTUN PROGRAM
# ─────────────────────────────────────────────────────────────────────────────
def page_mutun(c, pg):
    header_footer(c, pg, "برنامج متون")
    txt(c, "برنامج متون — الإنجاز الأبرز 2019–2025",
        W-MARGIN, H-21*mm, "Cairo-Black", 15, NAVY, "right")
    line(c, MARGIN, H-24*mm, W-MARGIN, H-24*mm, GOLD, 1)

    years   = [2019,2020,2021,2022,2023,2024,2025]
    students= [258, 358, 610, 438, 373, 858, 2559]
    lessons = [22,  270, 270, 69,  127, 366, 185]

    # Bar chart — students
    bar_chart(c, MARGIN, H-100*mm, CW*0.6, 62*mm,
              years, students,
              "الطلاب المسجلون في برنامج متون (2019–2025)",
              bar_col=TEAL, highlight_col=GOLD)

    # Line chart — lessons right
    lx = MARGIN + CW*0.64
    lw = CW*0.34
    line_chart(c, lx, H-100*mm, lw, 62*mm,
               years,
               [("الدروس العلمية", lessons, DKGREEN)],
               "الدروس العلمية")

    # Data table
    ty = H-108*mm
    rect(c, MARGIN, ty-7*mm, CW, 7*mm, fill=NAVY)
    headers = ["2025","2024","2023","2022","2021","2020","2019","المؤشر"]
    cw_ = CW/len(headers)
    for i, h_ in enumerate(headers):
        tx = MARGIN+(len(headers)-1-i)*cw_+cw_/2
        txt(c, h_, tx, ty-4.5*mm, "Cairo-Bold", 7, GOLD, "center")
    rows_data = [
        ("الطلاب",  ["2,559","858","373","438","610","358","258"]),
        ("الدروس",  ["185","366","127","69","270","270","22"]),
        ("المجالس (مستفيد)", ["17,140","18,571","3,688","—","—","—","—"]),
    ]
    for ri, (label, vals) in enumerate(rows_data):
        ty -= 7*mm
        bg = LTGRAY if ri%2==0 else WHITE
        rect(c, MARGIN, ty-7*mm, CW, 7*mm, fill=bg)
        for i, v in enumerate([*vals, label]):
            tx = MARGIN+(len(vals))*cw_ - i*cw_ + cw_/2
            col_ = NAVY if i==len(vals) else DKGRAY
            if v in ["2,559","858"]: col_ = DKGREEN
            txt(c, v, tx, ty-4.5*mm, "Cairo-SemiBold", 8.5, col_, "center")
    ty -= 9*mm

    # growth badge
    rect(c, MARGIN, ty-12*mm, CW, 12*mm, fill=DKGREEN)
    txt(c, "نمو استثنائي: من 258 طالباً (2019) إلى 2,559 طالباً (2025) — نمو 891% خلال 6 سنوات",
        W-MARGIN-5, ty-4.5*mm, "Cairo-Bold", 10, GOLD, "right")
    txt(c, "مجالس علمية 2025: 17,140 مستفيداً  |  دروس علمية: 185 درساً",
        W-MARGIN-5, ty-9*mm, "Cairo-Regular", 8, WHITE, "right")
    ty -= 14*mm

    analysis = ("يمثل برنامج متون النجاح الأبرز والأكثر استدامة في مسيرة الجمعية. "
                "القفزة من 258 طالباً عام 2019 إلى 2,559 طالباً عام 2025 تعني نمواً "
                "بنسبة 891% خلال ست سنوات. غير أن المسار لم يكن خطياً؛ بل شهد تذبذباً "
                "واضحاً (610 ثم انخفاض إلى 438 ثم 373)، قبل أن يقفز قفزة غير مسبوقة عام 2025. "
                "هذه القفزة من 858 إلى 2,559 تستوجب تفسيراً: هل هي نتيجة تغيير في آلية الإحصاء "
                "وإدراج الحلقات الإلكترونية، أم تحول منهجي حقيقي في التوسع؟ "
                "في كلا الحالين، برنامج متون يُعيد رسم هوية الجمعية من جمعية دعوة للجاليات "
                "إلى مرجعية علمية للمجتمع — وهذا التحول يستحق قراراً استراتيجياً واعياً.")
    analysis_box(c, MARGIN, ty-2*mm, CW, analysis, "التحليل التشخيصي")

    c.showPage()

# ─────────────────────────────────────────────────────────────────────────────
#  MUTUN MILESTONES — الدورات العلمية والمسابقات
# ─────────────────────────────────────────────────────────────────────────────
def page_mutun_milestones(c, pg):
    header_footer(c, pg, "برنامج متون")
    txt(c, "مسيرة متون — الدورات العلمية والمسابقات 1435–1444هـ",
        W-MARGIN, H-21*mm, "Cairo-Black", 14, NAVY, "right")
    line(c, MARGIN, H-24*mm, W-MARGIN, H-24*mm, GOLD, 1)

    # ── milestones timeline ──────────────────────────────────────
    milestones = [
        ("1435هـ", DKGREEN,  "انطلاق برنامج متون",
         "انطلق برنامج متون لتحفيظ المتون العلمية الشرعية في نجران بفرعين اثنين."),
        ("1437–38هـ", TEAL,  "أول تقرير سنوي",
         "صدر التقرير السنوي الأول لبرنامج متون 1437–1438هـ موثِّقاً المنهجية والبنية التنظيمية."),
        ("1439هـ", NAVY,  "4,894 مستفيداً تراكمياً",
         "أعداد المستفيدين التراكمية 4,894 | 890 طالب تحفيظ | 15 دورة علمية | 9 رحلات علمية | مسابقة الأمن الفكري 3,405 مشارك."),
        ("1442هـ", AMBER, "التوسع إلى شرورة",
         "امتد متون إلى محافظة شرورة لأول مرة، وانطلقت الدورة العلمية الـ24 ثم الـ25 في شرورة لطلاب الجمعية."),
        ("1443–44هـ", RED,  "مشروع مفاتيح الخير",
         "أطلقت الجمعية مشروع مفاتيح الخير في شرورة: 207 طلاب متون | 576 متابعاً | مجموع مستفيدي 1444هـ تجاوز 33,000 مستفيد."),
    ]
    cy = H-29*mm
    mh = 18*mm
    for year, col, title, desc in milestones:
        rect(c, MARGIN, cy-mh, CW, mh, fill=LTGRAY)
        rect(c, MARGIN, cy-mh, 18*mm, mh, fill=col)
        txt(c, year, MARGIN+9*mm, cy-mh/2-2*mm, "Cairo-Bold", 8, WHITE, "center")
        txt(c, title, W-MARGIN-4, cy-5*mm, "Cairo-Bold", 9, col, "right")
        txt(c, desc, W-MARGIN-4, cy-11*mm, "Cairo-Regular", 7.5, DKGRAY, "right")
        cy -= mh + 1*mm

    # ── الدورات العلمية table ──────────────────────────────────
    cy -= 3*mm
    txt(c, "الدورات العلمية لبرنامج متون — إحصاءات مفصّلة", W-MARGIN-4, cy,
        "Cairo-Bold", 9, NAVY, "right")
    cy -= 5*mm

    # header
    rect(c, MARGIN, cy-6*mm, CW, 6*mm, fill=NAVY)
    cols_w2 = [CW*0.12, CW*0.30, CW*0.18, CW*0.18, CW*0.22]
    cols_x2 = [MARGIN + sum(cols_w2[:i]) for i in range(len(cols_w2))]
    hdrs2 = ["الشهادات", "الحضور (ر+ن)", "المجالس", "الكتاب المشروح", "الدورة"]
    for i, h_ in enumerate(hdrs2):
        cx2 = cols_x2[len(hdrs2)-1-i] + cols_w2[len(hdrs2)-1-i]/2
        txt(c, h_, cx2, cy-4*mm, "Cairo-Bold", 7, GOLD, "center")

    courses = [
        ("الدورة الثانية (1439هـ)",    "الوسطية العقدية + الأربعون النووية", "7 مجالس", "256 (211ر+45ن)", "253"),
        ("الدورة الثالثة (1439هـ)",   "عمدة الأحكام — الطهارة",            "8 مجالس", "227 (194ر+33ن)", "227"),
        ("الدورة الرابعة (1439هـ)",   "البيقونية + الأصول الثلاثة + فضل الإسلام", "8 مجالس", "45+142 إلكتروني", "26+19"),
        ("دورة أساس العلم (1439هـ)", "10 متون علمية — المستوى الأول",     "20 مجلساً", "712 (642ر+70ن)", "—"),
        ("الدورة 24 في شرورة (1442هـ)", "جدول متون شرورة",                  "متعدد",   "طلاب المبتعثين",  "—"),
        ("الدورة 30 في شرورة (1444هـ)", "الجدول الشامل",                    "12 مجلساً", "576 مستفيداً",   "—"),
    ]
    for ri, row in enumerate(courses):
        cy -= 6*mm
        bg = LTGRAY if ri%2==0 else WHITE
        rect(c, MARGIN, cy-6*mm, CW, 6*mm, fill=bg)
        row_rev = list(reversed(row))
        for ci, val in enumerate(row_rev):
            cx2 = cols_x2[ci] + cols_w2[ci]/2
            txt(c, val, cx2, cy-4*mm, "Cairo-Regular", 7, DKGRAY, "center")

    # ── مسابقة الأمن الفكري ──────────────────────────────────
    cy -= 9*mm
    rect(c, MARGIN, cy-14*mm, CW, 14*mm, fill=NAVY)
    txt(c, "مسابقة الأمن الفكري الثانية 1439هـ — 3,405 مشاركًا من 30+ مدينة سعودية ودول عربية",
        W-MARGIN-5, cy-4*mm, "Cairo-Bold", 9, GOLD, "right")
    txt(c, "2,129 مشاركًا ذكورًا  |  1,276 مشاركةً  |  شملت: الرياض، جدة، الدمام، الطائف، أبها، تبوك، والمغرب، اليمن، مصر، باكستان",
        W-MARGIN-5, cy-10*mm, "Cairo-Regular", 7.5, WHITE, "right")

    c.showPage()

# ─────────────────────────────────────────────────────────────────────────────
#  MAFATEEH AL-KHAYR — شرورة
# ─────────────────────────────────────────────────────────────────────────────
def page_mafateeh_sharurah(c, pg):
    header_footer(c, pg, "برنامج متون")
    txt(c, "مشروع مفاتيح الخير — التوسع إلى شرورة 1443–1444هـ",
        W-MARGIN, H-21*mm, "Cairo-Black", 14, NAVY, "right")
    line(c, MARGIN, H-24*mm, W-MARGIN, H-24*mm, GOLD, 1)

    # ── intro box ──
    rect(c, MARGIN, H-38*mm, CW, 12*mm, fill=DKGREEN)
    txt(c, "مشروع مفاتيح الخير في شرورة: امتداد جغرافي لبرنامج متون خارج نجران",
        W-MARGIN-5, H-29*mm, "Cairo-Bold", 10, WHITE, "right")
    txt(c, "يُنفَّذ بالتعاون مع إمارة منطقة نجران | يستهدف الأئمة والمساجد والمتعلمين في محافظة شرورة",
        W-MARGIN-5, H-34*mm, "Cairo-Regular", 8, GOLD, "right")

    # ── 1443هـ stats ──
    txt(c, "مؤشرات برنامج متون في شرورة — 1443هـ", W-MARGIN-4, H-42*mm,
        "Cairo-Bold", 9, NAVY, "right")

    kpi43 = [
        (DKGREEN,  "207",   "طالب تحفيظ",      "120 ذكراً + 87 أنثى"),
        (TEAL,     "576",   "متابع متون",        "المتابعون في المجالس"),
        (NAVY,     "205",   "مشارك في المسابقة","83% نسبة الاستفادة"),
        (AMBER,    "60",    "جائزة توزّعت",      "على المتميزين في المسابقة"),
    ]
    bw43 = CW/len(kpi43)
    by43 = H-60*mm
    for i, (col, val, lbl, sub) in enumerate(kpi43):
        bx = MARGIN + i*bw43
        rect(c, bx+1, by43-20*mm, bw43-2, 20*mm, fill=col)
        txt(c, val, bx+bw43/2, by43-7*mm,  "Cairo-Black",   15, WHITE,  "center")
        txt(c, lbl, bx+bw43/2, by43-13*mm, "Cairo-SemiBold", 7, WHITE,  "center")
        txt(c, sub, bx+bw43/2, by43-18*mm, "Cairo-Regular",  6, GOLD,   "center")

    # ── 1444هـ stats ──
    txt(c, "مؤشرات مشروع مفاتيح الخير شرورة — 1444هـ (الأشمل)", W-MARGIN-4, H-84*mm,
        "Cairo-Bold", 9, NAVY, "right")

    programs44 = [
        ("الدورة العلمية الـ30",          "576",    "مستفيداً", "12 مجلساً"),
        ("الكلمات والمحاضرات",           "10,000", "مستفيداً", "121 كلمة ومحاضرة"),
        ("الدروس العلمية المصاحبة",      "1,612",  "مستفيداً", "18 درساً"),
        ("دورة الأئمة والمؤذنين",        "118",    "مستفيداً", "6 دورات"),
        ("ندوات الأئمة والخطباء",        "500",    "مستفيداً", "ندوتان"),
        ("المسابقات الفكرية",            "1,824",  "مستفيداً", "مسابقة واحدة"),
        ("خطب الجمعة",                   "15,000", "مستفيداً", "22 خطبة"),
        ("البرنامج النسائي",             "3,605",  "مستفيدةً", "16 برنامجاً"),
    ]
    # 2-column layout
    col_w44 = CW/2 - 1*mm
    cy44 = H-89*mm
    for ri, (prog, val, unit, detail) in enumerate(programs44):
        ci_ = ri % 2
        ri_ = ri // 2
        px_ = MARGIN + ci_*(col_w44+2*mm)
        py_ = cy44 - ri_*8*mm
        bg_ = LTGRAY if (ri_+ci_)%2==0 else WHITE
        rect(c, px_, py_-7*mm, col_w44, 7*mm, fill=bg_)
        txt(c, prog,          px_+col_w44-3, py_-3*mm, "Cairo-SemiBold", 7,   NAVY,   "right")
        txt(c, f"{val} {unit}", px_+col_w44-3, py_-6*mm, "Cairo-Bold",  7.5, DKGREEN, "right")
        txt(c, detail,        px_+3,         py_-4.5*mm, "Cairo-Regular", 6.5, DKGRAY, "left")

    # total + economic return
    rect(c, MARGIN, H-136*mm, CW, 10*mm, fill=DKGREEN)
    txt(c, "إجمالي المستفيدين في شرورة 1444هـ: أكثر من 33,000 مستفيد ومستفيدة",
        W-MARGIN-5, H-129*mm, "Cairo-Bold", 9.5, WHITE, "right")
    txt(c, "العائد الاقتصادي للتطوع: 35,200 ريال  |  عدد المتطوعين: 26 متطوعًا",
        W-MARGIN-5, H-134*mm, "Cairo-Regular", 8, GOLD, "right")

    # analysis
    analysis_txt = ("مشروع مفاتيح الخير في شرورة يُثبت قابلية برنامج متون للتوسع الجغرافي خارج نجران. "
                    "الأرقام الاستثنائية في 1444هـ — أكثر من 33,000 مستفيد في محافظة واحدة — تعكس "
                    "إمكانية هائلة لو أُسّست لها منظومة مؤسسية مستقلة لا تعتمد على جهود فردية. "
                    "غير أن الملاحظة الحرجة تبقى: الجمعية تُوسّع نطاقها الجغرافي دون أن تملك بُنية "
                    "موارد بشرية وإدارية كافية، وهو ما يُرسّخ نمط الاعتماد على الشخص لا على النظام.")
    analysis_box(c, MARGIN, H-139*mm, CW, analysis_txt, "التحليل التشخيصي")

    c.showPage()

# ─────────────────────────────────────────────────────────────────────────────
#  SECTION 5 — DA'WA PROGRAMS
# ─────────────────────────────────────────────────────────────────────────────
def page_dawa(c, pg):
    header_footer(c, pg, "البرامج الدعوية")
    txt(c, "البرامج الدعوية والعلمية 2019–2025",
        W-MARGIN, H-21*mm, "Cairo-Black", 15, NAVY, "right")
    line(c, MARGIN, H-24*mm, W-MARGIN, H-24*mm, GOLD, 1)

    years  = [2019,2020,2021,2022,2023,2024,2025]
    kalmat = [529, 211, 270,  91, 191,  89, 168]
    lectures=[15,   67,  13,   9,  59,  19,  17]
    durus  = [10,  135,  25,   3,3033, 151,  46]

    # Two charts side by side
    bar_chart(c, MARGIN, H-100*mm, CW*0.47, 62*mm,
              years, kalmat,
              "الكلمات الدعوية سنوياً",
              bar_col=AMBER, highlight_col=GOLD, show_trend=True)

    bar_chart(c, MARGIN+CW*0.52, H-100*mm, CW*0.46, 62*mm,
              years, lectures,
              "المحاضرات الدعوية سنوياً",
              bar_col=TEAL, highlight_col=GOLD)

    # Table
    ty = H-108*mm
    rect(c, MARGIN, ty-7*mm, CW, 7*mm, fill=NAVY)
    headers = ["2025","2024","2023","2022","2021","2020","2019","البرنامج"]
    cw_ = CW/len(headers)
    for i, h_ in enumerate(headers):
        txt(c, h_, MARGIN+(len(headers)-1-i)*cw_+cw_/2, ty-4.5*mm, "Cairo-Bold", 7, GOLD, "center")
    rows_d = [
        ("الكلمات الدعوية", ["168","89","191","91","270","211","529"]),
        ("المحاضرات",       ["17","19","59","9","13","67","15"]),
        ("الدروس العلمية",  ["46","151","3,033","3","25","135","10"]),
    ]
    for ri, (label, vals) in enumerate(rows_d):
        ty -= 7*mm
        bg = LTGRAY if ri%2==0 else WHITE
        rect(c, MARGIN, ty-7*mm, CW, 7*mm, fill=bg)
        for i, v in enumerate([*vals, label]):
            tx = MARGIN+(len(vals))*cw_ - i*cw_ + cw_/2
            col_ = NAVY if i==len(vals) else DKGRAY
            txt(c, v, tx, ty-4.5*mm, "Cairo-SemiBold", 8.5, col_, "center")
    ty -= 9*mm

    # Note box about 2023 durus spike
    rect(c, MARGIN, ty-12*mm, CW, 12*mm, fill=colors.HexColor("#FFF3CD"))
    rect(c, MARGIN, ty-12*mm, 3, 12*mm, fill=AMBER)
    txt(c, "ملاحظة: ارتفعت الدروس العلمية عام 2023 إلى 3,033 — ارتفاع استثنائي يرتبط بتوسع "
           "برنامج متون وإدراج الدروس الإلكترونية، ثم تراجعت إلى 46 عام 2025.",
        W-MARGIN-5, ty-4*mm, "Cairo-Regular", 8, DKGRAY, "right")
    ty -= 14*mm

    analysis = ("تكشف بيانات البرامج الدعوية عن مسار متذبذب وغير مستقر خلال الفترة 2019-2025. "
                "فالكلمات الدعوية التي بلغت ذروتها 529 عام 2019 تراجعت بنسبة 68% لتصل إلى 168 "
                "عام 2025. وتشير هذه الأرقام إلى أن النشاط الدعوي الميداني يفقد زخمه تدريجياً "
                "مقابل توسع البرامج العلمية كمتون. ويُسجَّل عام 2023 استثناءً واضحاً "
                "بارتفاع الدروس العلمية إلى 3,033، غير أنها انهارت إلى 46 عام 2025، مما يكشف "
                "غياب التخطيط متعدد السنوات واعتماد البرامج على دورات ظرفية. "
                "يُشير هذا النمط إلى فجوة جوهرية: الجمعية تُنفذ برامج دعوية لكنها لا تملك "
                "منهجية ثابتة ومؤسسية لضمان استمرارها وتنميتها سنة بعد سنة.")
    analysis_box(c, MARGIN, ty-2*mm, CW, analysis, "التحليل التشخيصي")

    c.showPage()

# ─────────────────────────────────────────────────────────────────────────────
#  SECTION 6 — RAMADAN & VOLUNTEERING
# ─────────────────────────────────────────────────────────────────────────────
def page_ramadan(c, pg):
    header_footer(c, pg, "المشاريع الرمضانية والتطوع")
    txt(c, "المشاريع الرمضانية والتطوع 2019–2025",
        W-MARGIN, H-21*mm, "Cairo-Black", 15, NAVY, "right")
    line(c, MARGIN, H-24*mm, W-MARGIN, H-24*mm, GOLD, 1)

    years   = [2019,2020,2021,2022,2023,2024,2025]
    iftar   = [525, 28000, 0, 17094, 47328, 58000, 38918]
    comp    = [0, 0, 9653, 14272, 19588, 45000, 9766]
    vol_hrs = [0, 0, 0, 4976, 12839, 14282, 21129]
    vol_act = [0, 0, 0, 328, 295, 0, 164]

    # Iftar chart
    bar_chart(c, MARGIN, H-96*mm, CW*0.47, 58*mm,
              years, iftar,
              "مستفيدو تفطير الصائمين",
              bar_col=DKGREEN, highlight_col=GOLD)

    # Volunteer hours chart
    bar_chart(c, MARGIN+CW*0.52, H-96*mm, CW*0.46, 58*mm,
              years, vol_hrs,
              "الساعات التطوعية",
              bar_col=TEAL, highlight_col=GOLD)

    # Table
    ty = H-104*mm
    rect(c, MARGIN, ty-7*mm, CW, 7*mm, fill=NAVY)
    headers = ["2025","2024","2023","2022","2021","2020","2019","المؤشر"]
    cw_ = CW/len(headers)
    for i, h_ in enumerate(headers):
        txt(c, h_, MARGIN+(len(headers)-1-i)*cw_+cw_/2, ty-4.5*mm, "Cairo-Bold", 7, GOLD, "center")
    rows_d = [
        ("تفطير الصائمين",  ["38,918","58,000","47,328","17,094","—","28,000","525"]),
        ("المسابقة الرمضانية",["9,766","45,000","19,588","14,272","9,653","—","—"]),
        ("الساعات التطوعية", ["21,129","14,282","12,839","4,976","—","—","—"]),
        ("المتطوعون النشطون",["164","—","295","328","—","—","—"]),
    ]
    for ri, (label, vals) in enumerate(rows_d):
        ty -= 7*mm
        bg = LTGRAY if ri%2==0 else WHITE
        rect(c, MARGIN, ty-7*mm, CW, 7*mm, fill=bg)
        for i, v in enumerate([*vals, label]):
            tx = MARGIN+(len(vals))*cw_ - i*cw_ + cw_/2
            col_ = NAVY if i==len(vals) else DKGRAY
            txt(c, v, tx, ty-4.5*mm, "Cairo-SemiBold", 8, col_, "center")
    ty -= 10*mm

    # volunteer paradox highlight
    rect(c, MARGIN, ty-14*mm, CW, 14*mm, fill=colors.HexColor("#E8F4E8"))
    rect(c, MARGIN, ty-14*mm, 3, 14*mm, fill=DKGREEN)
    txt(c, "المفارقة التطوعية", W-MARGIN-4, ty-3*mm, "Cairo-Bold", 9, DKGREEN, "right")
    txt(c, "الساعات التطوعية ترتفع من 4,976 (2022) إلى 21,129 (2025) — نمو 325%",
        W-MARGIN-4, ty-8*mm, "Cairo-Regular", 8, DKGRAY, "right")
    txt(c, "لكن عدد المتطوعين النشطين يتراجع من 328 (2022) إلى 164 (2025) — تراجع 50%",
        W-MARGIN-4, ty-13*mm, "Cairo-Regular", 8, RED, "right")
    ty -= 16*mm

    analysis = ("تبرز ظاهرتان متناقضتان في بيانات التطوع: الأولى إيجابية، وهي النمو المستمر "
                "في الساعات التطوعية من 4,976 ساعة عام 2022 إلى 21,129 ساعة عام 2025، وهو "
                "المؤشر الوحيد الذي لم يتراجع مرة واحدة خلال أربع سنوات. والثانية مقلقة: "
                "تراجع عدد المتطوعين النشطين من 328 إلى 164 في الفترة ذاتها، مما يعني أن "
                "قلة من الناس باتت تحمل أعباء أكثر — وهو مؤشر إجهاد مؤسسي وليس نمواً حقيقياً. "
                "أما مشروع تفطير الصائمين، فقد بلغ ذروته 58,000 مستفيد عام 2024، ثم تراجع "
                "إلى 38,918 عام 2025، مما يعكس تذبذباً في الموارد والتنظيم. "
                "وعلى صعيد المسابقة الرمضانية، فإن الارتفاع إلى 45,000 مشارك عام 2024 "
                "ثم التراجع إلى 9,766 عام 2025 يكشف اعتماداً على برامج ظرفية لا على "
                "استراتيجية رقمية مستدامة.")
    analysis_box(c, MARGIN, ty-2*mm, CW, analysis, "التحليل التشخيصي")

    c.showPage()

# ─────────────────────────────────────────────────────────────────────────────
#  SECTION 7 — MEDIA
# ─────────────────────────────────────────────────────────────────────────────
def page_media(c, pg):
    header_footer(c, pg, "الإعلام والحضور الرقمي")
    txt(c, "الإعلام والحضور الرقمي 2023–2025",
        W-MARGIN, H-21*mm, "Cairo-Black", 15, NAVY, "right")
    line(c, MARGIN, H-24*mm, W-MARGIN, H-24*mm, GOLD, 1)

    years_m = [2023, 2024, 2025]
    x_views = [23895, 2310900, 222583]
    yt_views = [10953, 0, 12523]

    # X views bar chart
    bar_chart(c, MARGIN, H-92*mm, CW*0.6, 56*mm,
              years_m, x_views,
              "مشاهدات منصة X سنوياً",
              bar_col=NAVY, highlight_col=GOLD, show_trend=True)

    # Platform stats right
    platdata = [
        (NAVY,    "2,310,900", "مشاهدات X\n2024 — الذروة"),
        (RED,     "222,583",   "مشاهدات X\n2025 — انخفاض 90%"),
        (TEAL,    "12,523",    "مشاهدات يوتيوب\n2025"),
        (DKGREEN, "1,169,000", "مشاهدات بصائر\nللناس 2024"),
    ]
    px = MARGIN + CW*0.64
    py = H-36*mm
    pw = CW*0.34
    ph = 13*mm
    for col_, val, lbl in platdata:
        rect(c, px, py, pw, ph, fill=col_)
        txt(c, val, px+pw/2, py+ph-5*mm, "Cairo-Black", 10, WHITE, "center")
        txt(c, lbl.replace("\n"," "), px+pw/2, py+1.5*mm, "Cairo-Regular", 5.5, LTGOLD, "center")
        py -= ph+2*mm

    # Table
    ty = H-100*mm
    rect(c, MARGIN, ty-7*mm, CW, 7*mm, fill=NAVY)
    media_rows = [
        ("مشاهدات X",           ["222,583","2,310,900","23,895"]),
        ("مشاهدات يوتيوب",      ["12,523","—","10,953"]),
        ("بث مباشر رمضاني",     ["—","—","29 حلقة"]),
        ("مشاهدات بصائر للناس", ["—","1,169,000","50,652"]),
        ("المشاركة الرقمية",    ["9,766","45,000","19,588"]),
    ]
    headers_m = ["2025","2024","2023","المؤشر"]
    cw_m = CW/len(headers_m)
    for i, h_ in enumerate(headers_m):
        tx = MARGIN+(len(headers_m)-1-i)*cw_m+cw_m/2
        txt(c, h_, tx, ty-4.5*mm, "Cairo-Bold", 7, GOLD, "center")
    for ri, (label, vals) in enumerate(media_rows):
        ty -= 7*mm
        bg = LTGRAY if ri%2==0 else WHITE
        rect(c, MARGIN, ty-7*mm, CW, 7*mm, fill=bg)
        for i, v in enumerate([*vals, label]):
            tx = MARGIN+(len(vals))*cw_m - i*cw_m + cw_m/2
            col_ = NAVY if i==len(vals) else DKGRAY
            txt(c, v, tx, ty-4.5*mm, "Cairo-SemiBold", 8.5, col_, "center")
    ty -= 10*mm

    # Wohj box
    rect(c, MARGIN, ty-12*mm, CW, 12*mm, fill=colors.HexColor("#1A2744"))
    txt(c, "2024 — سنة الوهج الرقمي غير المستدام",
        W-MARGIN-5, ty-4*mm, "Cairo-Bold", 10, GOLD, "right")
    txt(c, "2,310,900 مشاهدة في 2024 انهارت إلى 222,583 في 2025 — تراجع 90% في سنة واحدة",
        W-MARGIN-5, ty-9*mm, "Cairo-Regular", 8, WHITE, "right")
    ty -= 14*mm

    analysis = ("يُعدّ الملف الرقمي من أكثر الملفات تناقضاً في مسيرة الجمعية. "
                "ففي عام 2024 حققت الجمعية 2,310,900 مشاهدة على منصة X، وهو رقم استثنائي "
                "يُثبت قدرتها الرقمية الحقيقية. لكن هذا الوهج انهار في 2025 إلى 222,583 مشاهدة "
                "— تراجع بنسبة 90% في سنة واحدة. التحليل يكشف أن هذا الوهج كان مرتبطاً "
                "ببرنامج رمضاني واحد (بصائر للناس) لا باستراتيجية رقمية مستدامة. "
                "المفارقة أن الجمعية تُنتج محتوى علمياً رصيناً بالغ الجودة — 168 كلمة دعوية، "
                "46 درساً، 17 محاضرة في 2025 وحده — لكن هذا المحتوى لا يُحوَّل إلى حضور رقمي "
                "يعكس حجمه الفعلي. الفجوة بين الإنجاز الميداني والحضور الرقمي "
                "هي فرصة ضخمة غير مستثمرة.")
    analysis_box(c, MARGIN, ty-2*mm, CW, analysis, "التحليل التشخيصي")

    c.showPage()

# ─────────────────────────────────────────────────────────────────────────────
#  SECTION 8 — GOVERNANCE
# ─────────────────────────────────────────────────────────────────────────────
def page_governance(c, pg):
    header_footer(c, pg, "الحوكمة المؤسسية")
    txt(c, "الحوكمة المؤسسية — نتائج التقييم",
        W-MARGIN, H-21*mm, "Cairo-Black", 15, NAVY, "right")
    line(c, MARGIN, H-24*mm, W-MARGIN, H-24*mm, GOLD, 1)

    # Overall score
    rect(c, MARGIN, H-65*mm, CW, 35*mm, fill=DKGREEN)
    islamic_star(c, MARGIN+18*mm, H-47*mm, 25*mm, 12*mm, 12, 0.08, GOLD)
    txt(c, "93.08%", W-MARGIN-4, H-38*mm, "Cairo-Black", 42, GOLD, "right")
    txt(c, "النتيجة الإجمالية للحوكمة المؤسسية",
        W-MARGIN-4, H-50*mm, "Cairo-Bold", 11, WHITE, "right")
    txt(c, "تقييم المركز الوطني لتنمية القطاع غير الربحي | 2021–2024",
        W-MARGIN-4, H-57*mm, "Cairo-Regular", 8, LTGOLD, "right")
    txt(c, "تميز مؤسسي مستدام على مدى 4 سنوات متتالية",
        W-MARGIN-4, H-63*mm, "Cairo-Regular", 8, LTGOLD, "right")

    # Three criteria bars
    criteria = [
        ("السلامة المالية",   88.71, RED,    "الأدنى — يحتاج مراجعة"),
        ("الالتزام والامتثال", 94.00, DKGREEN,"ممتاز"),
        ("الشفافية والإفصاح", 93.00, TEAL,  "متميز"),
    ]
    cy = H-75*mm
    bw_total = CW - 50*mm
    for name, pct, col, note in criteria:
        rect(c, MARGIN, cy-8*mm, CW, 9*mm, fill=LTGRAY)
        bw = bw_total * pct/100
        rect(c, MARGIN+28*mm, cy-6.5*mm, bw, 6*mm, fill=col)
        txt(c, name, MARGIN+26*mm, cy-3.5*mm, "Cairo-SemiBold", 8, NAVY, "right")
        txt(c, f"{pct}%", MARGIN+28*mm+3, cy-3.5*mm, "Cairo-Bold", 8, WHITE, "left")
        txt(c, note, W-MARGIN, cy-3.5*mm, "Cairo-Regular", 6.5, MIDGRAY, "right")
        cy -= 11*mm

    # Historical table
    ty = cy - 4*mm
    rect(c, MARGIN, ty-7*mm, CW, 7*mm, fill=NAVY)
    gov_headers = ["2024","2023","2022","2021","المعيار"]
    cw_g = CW/len(gov_headers)
    for i, h_ in enumerate(gov_headers):
        txt(c, h_, MARGIN+(len(gov_headers)-1-i)*cw_g+cw_g/2,
            ty-4.5*mm, "Cairo-Bold", 7.5, GOLD, "center")
    gov_rows = [
        ("الالتزام والامتثال",  ["94.00%","94.00%","—","—"]),
        ("الشفافية والإفصاح",  ["88.71%","93.00%","—","—"]),
        ("السلامة المالية",     ["100%","64.45%","—","—"]),
        ("النتيجة الإجمالية",   ["93.08%","93.67%","—","—"]),
    ]
    for ri, (label, vals) in enumerate(gov_rows):
        ty -= 7*mm
        bg = LTGRAY if ri%2==0 else WHITE
        rect(c, MARGIN, ty-7*mm, CW, 7*mm, fill=bg)
        for i, v in enumerate([*vals, label]):
            tx = MARGIN+(len(vals))*cw_g - i*cw_g + cw_g/2
            col_ = NAVY if i==len(vals) else DKGRAY
            if "93" in v or "94" in v or "100" in v: col_ = DKGREEN
            if "64" in v or "88" in v: col_ = AMBER
            txt(c, v, tx, ty-4.5*mm, "Cairo-SemiBold", 8.5, col_, "center")
    ty -= 10*mm

    # Financial assets
    rect(c, MARGIN, ty-14*mm, CW, 14*mm, fill=NAVY)
    txt(c, "الأصول والموارد المالية", W-MARGIN-5, ty-3.5*mm, "Cairo-Bold", 9, GOLD, "right")
    assets = [("330,000 ريال","إيراد عقاري سنوي ثابت"),
              ("237,000 ريال","عائد اقتصادي للتطوع 2025"),
              ("أرض المطار","أصل استثماري غير مُفعَّل")]
    aw = CW/len(assets)
    for i, (v, l) in enumerate(assets):
        ax = MARGIN + i*aw
        line(c, ax+aw, ty-14*mm, ax+aw, ty, WHITE, 0.3)
        txt(c, v, ax+aw/2, ty-7*mm, "Cairo-Bold", 9, GOLD, "center")
        txt(c, l, ax+aw/2, ty-12*mm, "Cairo-Regular", 6.5, WHITE, "center")
    ty -= 16*mm

    analysis = ("تُعدّ نتيجة الحوكمة المؤسسية 93.08% من أبرز نقاط قوة الجمعية وأكثرها موثوقية. "
                "وما يميز هذه النتيجة أنها مستدامة ومتكررة على مدى أربع سنوات متتالية، "
                "مما يعكس انضباطاً مؤسسياً حقيقياً. لكن الملاحظة الجوهرية هي أن معيار "
                "السلامة المالية — الذي بلغ 88.71% — هو الحلقة الأضعف في منظومة الحوكمة، "
                "وهو ما يستوجب مراجعة في السياسات المالية والإجراءات المحاسبية. "
                "كما تجدر الإشارة إلى القفزة في السلامة المالية من 64.45% (2023) إلى 100% (2024)، "
                "وهو تحسن ملحوظ ينبغي توثيق العوامل المؤدية إليه للحفاظ عليه. "
                "الإيراد العقاري الثابت 330,000 ريال سنوياً يمثل ركيزة استقرار مالي حقيقية "
                "تُميّز الجمعية عن كثير من نظيراتها.")
    analysis_box(c, MARGIN, ty-2*mm, CW, analysis, "التحليل التشخيصي")

    c.showPage()

# ─────────────────────────────────────────────────────────────────────────────
#  SECTION 9 — SWOT
# ─────────────────────────────────────────────────────────────────────────────
def page_swot(c, pg):
    header_footer(c, pg, "تحليل SWOT")
    txt(c, "مصفوفة SWOT الموسعة — 45 نقطة", W-MARGIN, H-21*mm, "Cairo-Black", 15, NAVY, "right")
    line(c, MARGIN, H-24*mm, W-MARGIN, H-24*mm, GOLD, 1)

    hw = CW/2 - 1*mm
    hh = (H - 30*mm - 24*mm) / 2 - 2*mm

    quadrants = [
        (DKGREEN, "نقاط القوة (Strengths) — 14 نقطة", [
            "إيراد عقاري ثابت 330,000 ريال سنوياً — استقرار مالي مستدام",
            "قاعدة تطوعية متصاعدة: 164 متطوعاً، 21,129 ساعة، عائد 237,000 ريال",
            "برنامج متون: نمو 891% (258→2,559 طالب) في 6 سنوات",
            "أثر دعوي تراكمي موثق: 931 مسلماً من 11 جنسية منذ التأسيس",
            "حوكمة مؤسسية متميزة ومستدامة: 93.08% لأربع سنوات",
            "شبكة شراكات فاعلة: إحسان، تبرع، الراجحي، العطير، التطوع الوطني",
            "ثقة الدعاة والمشايخ: 168 كلمة دعوية، 46 درساً في 2025",
            "تجربة رقمية ناجحة: 1,169,000 مشاهدة لبرنامج بصائر للناس",
            "بنية تحتية جاهزة: مقر، أسطول سيارات، أنظمة مالية",
            "أرض استثمارية على طريق المطار — أصل تحويلي كبير",
            "موقع جغرافي استراتيجي: نجران حدود المملكة الجنوبية",
            "تجربة خدمة المرابطين — ميزة تنافسية فريدة",
            "مسابقة رمضانية: من 9,653 إلى 45,000 مشارك",
            "قيم الوسطية والاعتدال المنسجمة مع رؤية 2030",
        ]),
        (RED, "نقاط الضعف (Weaknesses) — 13 نقطة", [
            "تراجع المسلمين الجدد 85%: من 72 (2019) إلى 11 (2025)",
            "استنزاف الجمعية في برامج إغاثية (تفطير، سلال، مصليات) تتجاوز اختصاصها الدعوي وتُربك هويتها وتُرهق مواردها",
            "الأثر مرتبط بأشخاص لا بمنظومة — هشاشة بنيوية",
            "غياب تام لكوادر قسم الجاليات رغم أنه محور هوية الجمعية",
            "انعدام المترجمين لخدمة الجاليات غير الناطقة بالعربية",
            "المدير التنفيذي يحمل 22 مهمة — خطر وجودي على الاستمرارية",
            "غياب KPIs في جميع التوصيفات الوظيفية — تقييم ذاتي",
            "تذبذب حاد في المؤشرات يكشف غياب التخطيط متعدد السنوات",
            "الأثر الرقمي غير مستدام: انهيار 90% في مشاهدات X",
            "تراجع المتطوعين النشطين من 328 إلى 164 رغم نمو الساعات",
            "ضعف استراتيجية جمع التبرعات وانعدام قاعدة مانحين",
            "هيكل تنظيمي معطّل: إدارات على الورق مشلولة في الواقع",
            "السلامة المالية 88.71% — الأدنى في منظومة الحوكمة",
        ]),
        (TEAL, "الفرص (Opportunities) — 10 فرص", [
            "رؤية 2030: المجتمع المدني شريك استراتيجي وأبواب تمويل حكومي",
            "11 جنسية في نجران — ميدان دعوي واسع غير مخدوم مؤسسياً",
            "تجربة بصائر للناس قابلة للتكرار باستراتيجية ممنهجة",
            "الأرض على طريق المطار — حل جذري لمشكلة التمويل",
            "دعم المركز الوطني للجمعيات ذات الحوكمة العالية 93%+",
            "شُح المحتوى العلمي الوسطي رقمياً والطلب المتنامي عليه",
            "جامعة نجران — شراكة بحثية وموارد بشرية غير مستثمرة",
            "الحملات الوطنية لمكافحة التطرف تتوافق مع رسالة الجمعية",
            "التحول الرقمي الوطني يتيح تضخيم الأثر بتكلفة أقل",
            "التوسع الإقليمي في تدريب الدعاة بالمنطقة الجنوبية",
        ]),
        (AMBER, "التهديدات (Threats) — 8 تهديدات", [
            "تراجع المسلمين الجدد لـ11 يهدد الهوية التأسيسية للجمعية",
            "الاعتماد على أشخاص لا أنظمة — هشاشة بنيوية في النتائج",
            "تكاثر جمعيات مماثلة في نجران — تنافس على المتطوعين",
            "تراجع المتطوعين النشطين 50% مع غياب برامج تحفيز",
            "الشباب يتلقى تأثيره رقمياً — الحضور التقليدي يتراجع",
            "هشاشة التمويل: غياب قاعدة مانحين مؤسسية بعقود ثابتة",
            "شُح الكوادر الدعوية والمترجمين في سوق عمل نجران",
            "التغيرات التنظيمية للقطاع غير الربحي تستوجب يقظة",
        ]),
    ]

    positions = [
        (W-MARGIN-hw, H-26*mm),  # top-right: Strengths
        (MARGIN,       H-26*mm),  # top-left: Weaknesses
        (W-MARGIN-hw, H-26*mm-hh-4*mm),  # bottom-right: Opportunities
        (MARGIN,       H-26*mm-hh-4*mm),  # bottom-left: Threats
    ]

    for (col, title, pts), (bx, by) in zip(quadrants, positions):
        rect(c, bx, by-hh, hw, hh, fill=col)
        rect(c, bx, by-6*mm, hw, 6*mm, fill=colors.HexColor(
            "#0A2F21" if col==DKGREEN else
            "#8B1A1A" if col==RED else
            "#0D4448" if col==TEAL else "#8B5500"))
        txt(c, title, bx+hw-4, by-2.5*mm, "Cairo-Bold", 7, WHITE, "right")
        cy = by - 9*mm
        for pt in pts:
            if cy < by-hh+2*mm: break
            # bullet
            c.setFillColor(WHITE)
            c.setFillAlpha(0.9)
            c.circle(bx+hw-8, cy+1.5*mm, 1.2, fill=1, stroke=0)
            c.setFillAlpha(1)
            wrap_ar(c, pt, bx+hw-11, cy, hw-14, "Cairo-Regular", 7.5, WHITE, 13, "right")
            cy -= 11*mm

    c.showPage()

# ─────────────────────────────────────────────────────────────────────────────
#  SECTION 10 — GAP ANALYSIS
# ─────────────────────────────────────────────────────────────────────────────
def page_gaps(c, pg):
    header_footer(c, pg, "التشخيص المعمق — الفجوات الحرجة")
    txt(c, "التشخيص المعمق — الفجوات الست الحرجة",
        W-MARGIN, H-21*mm, "Cairo-Black", 15, NAVY, "right")
    line(c, MARGIN, H-24*mm, W-MARGIN, H-24*mm, GOLD, 1)

    gaps = [
        (RED,     "01", "فجوة الهوية الاستراتيجية — الأخطر والأعمق",
         "الجمعية مؤسسة للجاليات بالاسم، مؤسسة تعليمية بالواقع. لم يُتخذ قرار واعٍ بهذا التحول — "
         "هو انزياح تدريجي غير مخطط تراكم على مدى 6 سنوات. فضلاً عن ذلك أرهقت الجمعيةُ نفسَها "
         "ببرامج إغاثية وخيرية (تفطير الصائمين، السلال الغذائية، المصليات المتنقلة) ليست من صميم "
         "أهدافها اللائحية ولا تُحقق هدفها التأسيسي في خدمة الجاليات — وهي تستنزف الوقت والموارد "
         "والمتطوعين بعيداً عن البوصلة الدعوية الأصيلة."),
        (AMBER,   "02", "فجوة البنية والأشخاص — مصدر التذبذب",
         "التذبذب في المسلمين الجدد (42→55→14→11) يعكس أثراً مرتبطاً بشخص لا بنظام. "
         "المدير التنفيذي يحمل 22 مهمة — أي خروج طارئ يشل العمل المؤسسي كاملاً. "
         "الهيكل التنظيمي موجود على الورق، معطّل في الواقع. "
         "تراجع المتطوعين من 328 إلى 164 مع زيادة الساعات — إجهاد قلة تحمل عبء كثيرين."),
        (TEAL,    "03", "فجوة القياس والتوثيق — الأثر غير المنظور",
         "التقارير تقيس الحجم (عدد الكلمات والدروس) لا الأثر (ماذا تغيّر فعلاً؟). "
         "غياب KPIs في جميع التوصيفات الوظيفية يجعل التقييم ذاتياً وعشوائياً. "
         "القفزة في متون من 858 إلى 2,559 غير مُفسَّرة — قياس أم حقيقة؟"),
        (NAVY,    "04", "فجوة الرقمي المستدام — وهج بلا استراتيجية",
         "2024 أثبتت أن الجمعية قادرة رقمياً، لكن 2025 أثبتت أنها لا تستطيع الحفاظ على الأثر. "
         "مشاهدات X انهارت 90% في سنة واحدة — الوهج مرتبط ببرنامج موسمي لا بمنهج. "
         "الإنجاز الميداني لا يُحوَّل إلى حضور رقمي دائم."),
        (DKGREEN, "05", "فجوة الاستدامة المالية — أصول نائمة وتمويل هش",
         "الأرض الاستثمارية على طريق المطار لم تُطوَّر رغم إمكانيتها الكبيرة. "
         "غياب قاعدة مانحين مؤسسية يجعل الميزانية عرضة للتذبذب السنوي. "
         "السلامة المالية 88.71% تحتاج معالجة في السياسات والإجراءات."),
        (MIDGRAY, "06", "فجوة التحول الهوياتي — القرار المؤجَّل",
         "الجمعية بحاجة لإجابة صريحة: هل تريد الاستمرار كمؤسسة دعوة مباشرة للجاليات؟ "
         "أم تريد تثبيت هويتها كمرجعية علمية للمجتمع كاملاً؟ أم الجمع بينهما بهيكل يُفصل "
         "بين ذراع الجاليات وذراع التعليم العلمي؟ بدون قرار هوياتي تظل الخطة "
         "الاستراتيجية تسير في اتجاهين متعارضين."),
    ]

    cy = H-27*mm
    gh = (H-30*mm-14*mm) / len(gaps) - 1.5*mm

    for col, num, title, desc in gaps:
        rect(c, MARGIN, cy-gh, CW, gh, fill=LTGRAY)
        rect(c, MARGIN, cy-gh, 5, gh, fill=col)
        # num badge
        rect(c, MARGIN+7, cy-gh/2-4*mm, 10*mm, 8*mm, fill=col)
        txt(c, num, MARGIN+12, cy-gh/2-0.5*mm, "Cairo-Bold", 9, WHITE, "center")
        # title
        txt(c, title, W-MARGIN-4, cy-3.5*mm, "Cairo-Bold", 8.5, NAVY, "right")
        # desc
        wrap_ar(c, desc, W-MARGIN-4, cy-10*mm, CW-22*mm,
                "Cairo-Regular", 9, DKGRAY, 16, "right")
        cy -= gh + 1.5*mm

    c.showPage()

# ─────────────────────────────────────────────────────────────────────────────
#  SECTION 11 — PROGRAMS vs OBJECTIVES
# ─────────────────────────────────────────────────────────────────────────────
def page_programs_objectives(c, pg):
    header_footer(c, pg, "مقارنة البرامج بالأهداف")
    txt(c, "مقارنة البرامج الحالية بأهداف الجمعية (المادة الخامسة)",
        W-MARGIN, H-19*mm, "Cairo-Black", 14, NAVY, "right")
    line(c, MARGIN, H-24*mm, W-MARGIN, H-24*mm, GOLD, 1)

    # Alignment matrix
    # obj1=نشر العلم الشرعي | obj2=دعوة الوافدين وتبصيرهم | obj3=الوسطية والأمن الفكري | obj4=التقنية
    programs = [
        ("برنامج متون (تحفيظ المتون العلمية)",
         True, False, True, True,
         "يخدم الهدف الأول (نشر العلم) والثالث (منهج السلف) والرابع (منصات رقمية)"),
        ("مشروع تفطير الصائمين",
         False, True, False, False,
         "ورد في الهدف الثاني (إفطار الصائم للوافدين) — لكنه يُنفَّذ مستقلاً عن الغاية الدعوية"),
        ("الكلمات والمحاضرات الدعوية",
         True, True, True, False,
         "يخدم الأهداف الأول والثاني والثالث — نشر العلم ودعوة الوافدين والوسطية"),
        ("المسابقة الرمضانية الإلكترونية",
         True, False, True, True,
         "يخدم الهدف الأول والثالث والرابع (منصة إلكترونية دينية)"),
        ("برامج الجاليات الميدانية",
         False, True, False, False,
         "مباشر للهدف الثاني — دعوة الوافدين غير المسلمين وتبصير المسلمين منهم"),
        ("المجالس والدروس العلمية",
         True, False, True, False,
         "يخدم الهدف الأول (نشر العلم) والثالث (ربط الناس بمنهج السلف الصالح)"),
        ("توزيع المصاحف والمواد الدعوية",
         True, True, False, False,
         "يخدم الهدفين الأول والثاني — مواد علمية للمسلمين والوافدين"),
        ("برنامج يوم في الحرم",
         True, False, True, False,
         "يخدم الهدف الأول والثالث — تعزيز الهوية الدينية وربط بمنهج السلف"),
        ("مشروع المصليات المتنقلة",
         False, True, False, False,
         "يخدم الهدف الثاني — تبصير الوافدين المسلمين (المرابطون بالحد الجنوبي)"),
        ("السلال الغذائية والتمور",
         False, True, False, False,
         "مذكورة في الهدف الثاني (وما في حُكمها) — مع غياب الربط الدعوي الفعلي"),
    ]

    ty = H-26*mm
    # Header
    rect(c, MARGIN, ty-9*mm, CW, 9*mm, fill=NAVY)
    cols_w = [CW*0.38, CW*0.1, CW*0.1, CW*0.1, CW*0.1, CW*0.22]
    cols_x = [MARGIN]
    for w_ in cols_w[:-1]: cols_x.append(cols_x[-1]+w_)
    headers_p = ["البرنامج", "هدف 1", "هدف 2", "هدف 3", "هدف 4", "الملاحظة"]
    for i, (h_, cx_) in enumerate(zip(headers_p, cols_x)):
        txt(c, h_, cx_+cols_w[i]-2, ty-4.5*mm, "Cairo-Bold", 8, GOLD, "right")
    ty -= 9*mm

    for ri, (prog, o1, o2, o3, o4, note) in enumerate(programs):
        rh = 9*mm
        bg = LTGRAY if ri%2==0 else WHITE
        rect(c, MARGIN, ty-rh, CW, rh, fill=bg)
        # Program name
        txt(c, prog, cols_x[0]+cols_w[0]-2, ty-5*mm, "Cairo-SemiBold", 8, NAVY, "right")
        # Objectives checkmarks
        for j, (matched, cx_) in enumerate(zip([o1,o2,o3,o4], cols_x[1:5])):
            symbol = "✓" if matched else "—"
            col_ = DKGREEN if matched else MIDGRAY
            c.setFillColor(col_)
            c.setFont("Cairo-Bold", 8)
            c.drawCentredString(cx_+cols_w[j+1]/2, ty-5.5*mm, ar(symbol))
        # Note
        wrap_ar(c, note, cols_x[5]+cols_w[5]-2, ty-2*mm, cols_w[5]-4,
                "Cairo-Regular", 7, DKGRAY, 12, "right")
        ty -= rh

    # Alignment summary
    ty -= 4*mm
    rect(c, MARGIN, ty-72*mm, CW, 72*mm, fill=NAVY)
    txt(c, "خلاصة تحليل مدى توافق البرامج مع الأهداف", W-MARGIN-4, ty-4*mm,
        "Cairo-Bold", 10, GOLD, "right")
    findings = [
        (WHITE,
         "الهدف الأول — نشر العلم الشرعي:",
         "قوي الحضور: متون، الدروس، المجالس، المحاضرات، المسابقة الإلكترونية — "
         "الهدف الأكثر تمثيلاً في البرامج بفارق كبير عن بقية الأهداف."),
        (WHITE,
         "الهدف الثاني — دعوة الوافدين وتبصيرهم:",
         "أضعف الأهداف تحقيقاً قياساً بحجم الجاليات — برامج الجاليات الميدانية شبه مشلولة "
         "رغم أن الوافدين هم الفئة المستهدفة الأصيلة للجمعية."),
        (WHITE,
         "الهدف الثالث — الوسطية والأمن الفكري:",
         "حاضر في الكلمات والمجالس والمسابقة — لكن غير مقيس بمؤشرات واضحة "
         "تُثبت الأثر الفعلي في تعزيز الأمن الفكري ومقاومة الغلو."),
        (WHITE,
         "الهدف الرابع — استخدام التقنية:",
         "غائب عملياً — المسابقة الإلكترونية ومنصة متون الاستثنائان الوحيدان، "
         "ومعظم البرامج ميدانية تقليدية خالية من توظيف تقني منهجي وغياب استراتيجية رقمية مكتوبة."),
    ]
    cy2 = ty - 10*mm
    for col_f, title_f, desc_f in findings:
        txt(c, title_f, W-MARGIN-4, cy2, "Cairo-SemiBold", 8.5, GOLD, "right")
        wrap_ar(c, desc_f, W-MARGIN-4, cy2-5*mm, CW-8, "Cairo-Regular", 8, col_f, 13, "right")
        cy2 -= 14*mm
    # Critical finding — charitable burden
    rect(c, MARGIN+2, ty-69*mm, CW-4, 9*mm, fill=RED)
    wrap_ar(c,
        "تحذير: برامج التفطير والسلال الغذائية والمصليات المتنقلة لا تندرج في أهداف الجمعية اللائحية — "
        "هي تُرهق الجمعية بأعباء إغاثية تستنزف مواردها ومتطوعيها بعيداً عن بوصلتها الدعوية الأصيلة.",
        W-MARGIN-4, ty-62*mm, CW-8, "Cairo-Bold", 8, WHITE, 14, "right")

    c.showPage()

# ─────────────────────────────────────────────────────────────────────────────
#  CONCLUSION
# ─────────────────────────────────────────────────────────────────────────────
def page_conclusion(c, pg):
    header_footer(c, pg, "الخلاصة التشخيصية")
    txt(c, "الخلاصة التشخيصية النهائية", W-MARGIN, H-19*mm, "Cairo-Black", 16, NAVY, "right")
    line(c, MARGIN, H-24*mm, W-MARGIN, H-24*mm, GOLD, 1.2)

    # Big quote box — extra height so text has breathing room
    rect(c, MARGIN, H-80*mm, CW, 52*mm, fill=NAVY)
    rect(c, MARGIN, H-80*mm, 4, 52*mm, fill=GOLD)
    islamic_star(c, MARGIN+20*mm, H-57*mm, 25*mm, 12*mm, 12, 0.08)

    conclusion_text = ("بعد مراجعة سبع سنوات من البيانات الموثقة، الصورة أعمق وأكثر تعقيداً "
                       "مما تبدو عليه في التقارير السنوية المنفردة. جمعية بصائر ليست ضعيفة "
                       "الأداء — هي ضعيفة القصد الاستراتيجي الواعي. تمتلك مقومات نادرة: "
                       "برنامج علمي ينمو بقوة، ساعات تطوعية في تصاعد مستمر، حوكمة متميزة، "
                       "وتجربة رقمية أثبتت إمكانية الوصول لمليون مشاهد.")
    wrap_ar(c, conclusion_text, W-MARGIN-6, H-33*mm, CW-12,
            "Cairo-Bold", 10, WHITE, 18, "right")

    # Second part
    conclusion2 = ("لكنها في الوقت ذاته تسمح لأكثر مؤشراتها جوهرية — إسلام الجاليات — أن ينهار "
                   "85% دون قرار معالجة واضح، بينما تُرهق نفسها ببرامج إغاثية وخيرية ليست من "
                   "صميم أهدافها اللائحية — وهي تستنزف مواردها ومتطوعيها بعيداً عن بوصلتها الدعوية. "
                   "التحدي الأكبر: اتخاذ قرارات لم تُتخذ بعد — عن الهوية، عن الهيكل، عن الأولويات.")
    wrap_ar(c, conclusion2, W-MARGIN-6, H-59*mm, CW-12,
            "Cairo-Regular", 9.5, LTGOLD, 17, "right")

    # 4 Priority boxes
    priorities = [
        (RED,     "01", "القرار الهوياتي",
         "تحديد الهوية بوضوح وترك البرامج الإغاثية الخارجة عن التخصص الدعوي للجهات المعنية بها."),
        (AMBER,   "02", "إنقاذ مؤشر المسلمين الجدد",
         "تراجع من 72 إلى 11 في ست سنوات ليس قدراً — هو نتيجة غياب منظومة مؤسسية متكاملة."),
        (TEAL,    "03", "البناء المؤسسي الفعلي",
         "تفكيك مركزية المدير التنفيذي وبناء هيكل حقيقي بمسؤوليات وKPIs لكل إدارة."),
        (DKGREEN, "04", "الاستدامة المالية والرقمية",
         "تطوير الأرض الاستثمارية وبناء استراتيجية رقمية تُحوِّل وهج 2024 إلى نمو مستدام."),
    ]
    py = H-86*mm
    pw = CW/4 - 1.5*mm
    for i, (col, num, title_p, desc_p) in enumerate(priorities):
        px = MARGIN + i*(pw+2*mm)
        rect(c, px, py-34*mm, pw, 34*mm, fill=col)
        rect(c, px, py-34*mm, pw, 3, fill=WHITE)
        txt(c, num, px+pw/2, py-8*mm, "Cairo-Black", 18, WHITE, "center")
        txt(c, title_p, px+pw/2, py-16*mm, "Cairo-Bold", 8, WHITE, "center")
        wrap_ar(c, desc_p, px+pw-3, py-21*mm, pw-6,
                "Cairo-Regular", 8, WHITE, 14, "right")

    # Author signature
    rect(c, MARGIN, 22*mm, CW, 18*mm, fill=LTGRAY)
    line(c, MARGIN, 40*mm, W-MARGIN, 40*mm, GOLD, 1)
    txt(c, "إعداد", W-MARGIN, 36*mm, "Cairo-Regular", 7, MIDGRAY, "right")
    txt(c, "د. مطارد بن دخيل بن ناصر العنزي",
        W-MARGIN, 30*mm, "Cairo-Bold", 12, NAVY, "right")
    txt(c, "مستشار استراتيجي  |  عقد الاستشارة الاستراتيجية — المرحلة الأولى",
        W-MARGIN, 25*mm, "Cairo-Regular", 8, DKGRAY, "right")
    txt(c, "إبريل 2026م", MARGIN+5, 29*mm, "Cairo-SemiBold", 10, GOLD, "left")
    txt(c, "نجران — المملكة العربية السعودية", MARGIN+5, 25*mm, "Cairo-Regular", 8, DKGRAY, "left")

    c.showPage()

# ─────────────────────────────────────────────────────────────────────────────
#  BACK COVER
# ─────────────────────────────────────────────────────────────────────────────
def page_back(c):
    rect(c, 0, 0, W, H, fill=NAVY)
    rect(c, 0, 0, W, H*0.3, fill=DKGREEN)
    for cx_, cy_, ro, ri, nn in [
        (W*0.15, H*0.7, 60, 30, 16),
        (W*0.85, H*0.65, 55, 28, 14),
        (W*0.5,  H*0.5,  40, 20, 12),
    ]:
        islamic_star(c, cx_, cy_, ro, ri, nn, 0.07)
    rect(c, MARGIN, H*0.5, CW, 1.5, fill=GOLD)

    txt(c, "جمعية بصائر", W/2, H*0.72, "Cairo-Black", 28, WHITE, "center")
    txt(c, "للدعوة والإرشاد وتوعية الجاليات — نجران",
        W/2, H*0.64, "Cairo-Regular", 12, LTGOLD, "center")
    txt(c, "التقرير التشخيصي الشامل — المرحلة الأولى",
        W/2, H*0.56, "Cairo-SemiBold", 10, GOLD, "center")

    txt(c, "0175233139", W/2, H*0.22, "Cairo-Regular", 10, WHITE, "center")
    txt(c, "شارع الملك عبد العزيز، نجران، المملكة العربية السعودية",
        W/2, H*0.17, "Cairo-Regular", 9, LTGOLD, "center")
    txt(c, "إبريل 2026م", W/2, H*0.12, "Cairo-Regular", 9, MIDGRAY, "center")

    c.showPage()

# ─────────────────────────────────────────────────────────────────────────────
#  MAIN
# ─────────────────────────────────────────────────────────────────────────────
OUT = r"c:/Users/mtare/Desktop/ابو عثمان/تشخيص_واقع_جمعية_بصائر_2026.pdf"
c = canvas.Canvas(OUT, pagesize=A4)
c.setTitle("تشخيص واقع جمعية بصائر 2026")
c.setAuthor("د. مطارد بن دخيل العنزي")

pg = 1
page_cover(c);          pg+=1
page_toc(c, pg);        pg+=1
page_exec_summary(c, pg); pg+=1

section_div(c, "01", "لمحة عن الجمعية", "الهوية والأهداف الأساسية", pg); pg+=1
page_org_overview(c, pg); pg+=1

section_div(c, "02", "الجاليات والمسلمون الجدد", "المؤشر الأكثر حساسية", pg); pg+=1
page_new_muslims(c, pg); pg+=1

section_div(c, "03", "برنامج متون", "الإنجاز الأبرز — نمو 891%", pg); pg+=1
page_mutun(c, pg); pg+=1
page_mutun_milestones(c, pg); pg+=1
page_mafateeh_sharurah(c, pg); pg+=1

section_div(c, "04", "البرامج الدعوية", "الكلمات والمحاضرات والدروس", pg); pg+=1
page_dawa(c, pg); pg+=1

section_div(c, "05", "برامج رمضان والتطوع", "التفطير والمسابقة والمتطوعون", pg); pg+=1
page_ramadan(c, pg); pg+=1

section_div(c, "06", "الإعلام الرقمي", "الوهج وغياب الاستراتيجية", pg); pg+=1
page_media(c, pg); pg+=1

section_div(c, "07", "الحوكمة المؤسسية", "93.08% — تميز مستدام", pg); pg+=1
page_governance(c, pg); pg+=1

section_div(c, "08", "تحليل SWOT", "44 نقطة — قوة وضعف وفرص وتهديدات", pg); pg+=1
page_swot(c, pg); pg+=1

section_div(c, "09", "الفجوات الحرجة", "التشخيص المعمق — ست فجوات", pg); pg+=1
page_gaps(c, pg); pg+=1

section_div(c, "10", "البرامج والأهداف", "مقارنة تحليلية بالمادة الخامسة", pg); pg+=1
page_programs_objectives(c, pg); pg+=1

section_div(c, "11", "الخلاصة التشخيصية", "الحكم النهائي وأولويات المرحلة القادمة", pg); pg+=1
page_conclusion(c, pg); pg+=1

page_back(c)

c.save()
print(f"PDF saved: {OUT}")
print(f"Total pages: {pg}")
