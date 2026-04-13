#!/usr/bin/env python3
"""
Premium Arabic Corporate Report Template Generator
McKinsey/BCG/Deloitte Style - Top 1% Global Corporate Level
A4 Print-Ready PDF with Arabic Typography
"""

import os
import math
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
import arabic_reshaper
from bidi.algorithm import get_display

# ─────────────────────────────────────────────
#  FONTS
# ─────────────────────────────────────────────
USER_FONTS = "C:/Users/mtare/AppData/Local/Microsoft/Windows/Fonts/"
WIN_FONTS  = "C:/Windows/Fonts/"

def reg(name, path):
    pdfmetrics.registerFont(TTFont(name, path))

reg("Cairo-Regular",   USER_FONTS + "Cairo-Regular.ttf")
reg("Cairo-Medium",    USER_FONTS + "Cairo-Medium.ttf")
reg("Cairo-SemiBold",  USER_FONTS + "Cairo-SemiBold.ttf")
reg("Cairo-Bold",      USER_FONTS + "Cairo-Bold.ttf")
reg("Cairo-ExtraBold", USER_FONTS + "Cairo-ExtraBold.ttf")
reg("Cairo-Black",     USER_FONTS + "Cairo-Black.ttf")
reg("DIN-Regular",     USER_FONTS + "ArbFONTS-DINNextLTArabic-Regular-3.ttf")
reg("DIN-Bold",        USER_FONTS + "ArbFONTS-DINNextLTArabic-Bold-4.ttf")
reg("DIN-Light",       USER_FONTS + "ArbFONTS-DINNEXTLTARABIC-LIGHT-2-2.ttf")

# ─────────────────────────────────────────────
#  PALETTE
# ─────────────────────────────────────────────
NAVY        = colors.HexColor("#0D1B2A")
NAVY_MID    = colors.HexColor("#1B2E4B")
NAVY_LIGHT  = colors.HexColor("#253F63")
DARK_GREEN  = colors.HexColor("#0B3D2E")
MID_GREEN   = colors.HexColor("#145A3E")
GOLD        = colors.HexColor("#C9A84C")
GOLD_LIGHT  = colors.HexColor("#E8D5A3")
GOLD_PALE   = colors.HexColor("#F5EDD6")
WHITE       = colors.HexColor("#FFFFFF")
OFF_WHITE   = colors.HexColor("#F7F8FA")
GRAY_LIGHT  = colors.HexColor("#EEF0F4")
GRAY_MID    = colors.HexColor("#9AA3B2")
GRAY_DARK   = colors.HexColor("#4A5568")
TEXT_DARK   = colors.HexColor("#0D1B2A")
TEXT_BODY   = colors.HexColor("#2D3748")

# ─────────────────────────────────────────────
#  DIMENSIONS (A4 with 3mm bleed)
# ─────────────────────────────────────────────
W, H   = A4                      # 595.28 x 841.89 pt
BLEED  = 3 * mm
MARGIN = 20 * mm
GRID_L = MARGIN
GRID_R = W - MARGIN
GRID_T = H - MARGIN
GRID_B = MARGIN
CONTENT_W = GRID_R - GRID_L

# ─────────────────────────────────────────────
#  ARABIC TEXT HELPER
# ─────────────────────────────────────────────
def ar(text):
    """Reshape and apply BiDi to Arabic text for proper display."""
    reshaped = arabic_reshaper.reshape(text)
    return get_display(reshaped)

# ─────────────────────────────────────────────
#  DRAWING HELPERS
# ─────────────────────────────────────────────
def draw_text_rtl(c, text, x, y, font, size, color=WHITE, anchor="right"):
    """Draw RTL Arabic text at position."""
    c.setFont(font, size)
    c.setFillColor(color)
    txt = ar(text)
    if anchor == "center":
        c.drawCentredString(x, y, txt)
    elif anchor == "right":
        c.drawRightString(x, y, txt)
    else:
        c.drawString(x, y, txt)

def draw_rect(c, x, y, w, h, fill=None, stroke=None, stroke_width=0.5):
    if fill:
        c.setFillColor(fill)
    if stroke:
        c.setStrokeColor(stroke)
        c.setLineWidth(stroke_width)
    if fill and stroke:
        c.rect(x, y, w, h, fill=1, stroke=1)
    elif fill:
        c.rect(x, y, w, h, fill=1, stroke=0)
    else:
        c.rect(x, y, w, h, fill=0, stroke=1)

def draw_line(c, x1, y1, x2, y2, color=GOLD, width=0.5):
    c.setStrokeColor(color)
    c.setLineWidth(width)
    c.line(x1, y1, x2, y2)

# ─────────────────────────────────────────────
#  ISLAMIC GEOMETRIC PATTERN (16-point star)
# ─────────────────────────────────────────────
def draw_islamic_star(c, cx, cy, r_outer, r_inner, n=16, alpha=0.06, color=GOLD):
    """Draw a subtle n-pointed Islamic star."""
    c.saveState()
    c.setStrokeColor(color)
    c.setFillColor(colors.Color(color.red, color.green, color.blue, alpha))
    c.setLineWidth(0.3)
    points = []
    for i in range(n * 2):
        angle = math.pi / n * i - math.pi / 2
        r = r_outer if i % 2 == 0 else r_inner
        points.append((cx + r * math.cos(angle), cy + r * math.sin(angle)))
    path = c.beginPath()
    path.moveTo(*points[0])
    for pt in points[1:]:
        path.lineTo(*pt)
    path.close()
    c.drawPath(path, fill=1, stroke=1)
    c.restoreState()

def draw_geometric_grid(c, cx, cy, size, alpha=0.04):
    """Draw a subtle Islamic-inspired geometric grid tile."""
    c.saveState()
    c.setStrokeColor(GOLD)
    c.setLineWidth(0.25)
    # Outer circle
    c.setFillColor(colors.Color(GOLD.red, GOLD.green, GOLD.blue, 0))
    c.setStrokeAlpha(alpha * 2)
    c.circle(cx, cy, size, fill=0, stroke=1)
    # Inner hexagonal lines
    for i in range(6):
        angle = math.pi / 3 * i
        x1 = cx + size * math.cos(angle)
        y1 = cy + size * math.sin(angle)
        x2 = cx + size * math.cos(angle + math.pi / 3)
        y2 = cy + size * math.sin(angle + math.pi / 3)
        c.line(x1, y1, x2, y2)
    c.restoreState()

def draw_cover_background(c):
    """Full dark navy background with sophisticated design elements."""
    # Full bleed background
    draw_rect(c, -BLEED, -BLEED, W + 2*BLEED, H + 2*BLEED, fill=NAVY)

    # Dark green left panel
    panel_w = W * 0.42
    draw_rect(c, -BLEED, -BLEED, panel_w + BLEED, H + 2*BLEED, fill=DARK_GREEN)

    # Gold diagonal accent line separating panels
    c.saveState()
    c.setStrokeColor(GOLD)
    c.setLineWidth(2.5)
    c.line(panel_w - 5*mm, H + BLEED, panel_w + 15*mm, -BLEED)
    c.restoreState()

    # Thin gold lines on dark green panel
    for i, x_off in enumerate([8*mm, 12*mm, 15*mm]):
        alpha = 0.5 - i * 0.12
        c.saveState()
        c.setStrokeColor(GOLD)
        c.setLineWidth(0.4)
        c.setStrokeAlpha(alpha)
        c.line(panel_w - 5*mm + x_off, H + BLEED,
               panel_w + 15*mm + x_off, -BLEED)
        c.restoreState()

    # Islamic geometric patterns (subtle)
    draw_islamic_star(c, panel_w * 0.45, H * 0.75, 55*mm, 25*mm, n=12, alpha=0.07)
    draw_islamic_star(c, panel_w * 0.45, H * 0.75, 38*mm, 18*mm, n=12, alpha=0.05)
    draw_islamic_star(c, panel_w * 0.6,  H * 0.18, 35*mm, 16*mm, n=8,  alpha=0.06)

    # Small accent stars
    draw_islamic_star(c, W * 0.78, H * 0.88, 28*mm, 13*mm, n=8, alpha=0.04,
                      color=colors.HexColor("#C9A84C"))

    # Horizontal gold accent lines (right side header area)
    for i in range(3):
        y = H - (35 + i * 5) * mm
        x_start = panel_w + 15*mm
        alpha = 0.6 - i * 0.15
        c.saveState()
        c.setStrokeColor(GOLD)
        c.setLineWidth(0.6 if i == 0 else 0.3)
        c.setStrokeAlpha(alpha)
        c.line(x_start, y, W - 15*mm, y)
        c.restoreState()

    # Bottom gold bar (thick)
    draw_rect(c, -BLEED, -BLEED, W + 2*BLEED, 18*mm, fill=GOLD)
    # Thin white line above gold bar
    draw_line(c, -BLEED, 18*mm, W + BLEED, 18*mm, color=WHITE, width=0.5)

    # Top-right corner decorative bracket
    c.saveState()
    c.setStrokeColor(GOLD)
    c.setLineWidth(1.2)
    c.setStrokeAlpha(0.7)
    bx, by = W - 22*mm, H - 22*mm
    c.line(bx, by, bx, H - 10*mm)
    c.line(bx, H - 10*mm, W - 10*mm, H - 10*mm)
    c.restoreState()

# ─────────────────────────────────────────────
#  HEADER & FOOTER (inner pages)
# ─────────────────────────────────────────────
def draw_header(c, section_title="", page_num=None, is_dark=False):
    bg = NAVY if is_dark else WHITE
    line_color = GOLD
    txt_color  = WHITE if is_dark else NAVY

    if is_dark:
        draw_rect(c, 0, H - 22*mm, W, 22*mm, fill=NAVY)

    # Top colored stripe
    draw_rect(c, 0, H - 3*mm, W, 3*mm, fill=GOLD)

    # Gold horizontal rule below header
    draw_line(c, MARGIN, H - 22*mm, W - MARGIN, H - 22*mm, color=GOLD, width=0.8)

    # Section title (RTL)
    if section_title:
        draw_text_rtl(c, section_title,
                      W - MARGIN, H - 15*mm,
                      "Cairo-SemiBold", 9, color=txt_color, anchor="right")

    # Logo placeholder (left side of header)
    lx, ly = MARGIN, H - 18*mm
    lw, lh = 32*mm, 10*mm
    draw_rect(c, lx, ly, lw, lh, stroke=GOLD, stroke_width=0.5)
    c.setFont("Cairo-Regular", 6)
    c.setFillColor(GRAY_MID)
    c.drawCentredString(lx + lw/2, ly + lh/2 - 2, ar("شعار الجهة"))

def draw_footer(c, page_num=1, section_title=""):
    # Bottom gold line
    draw_line(c, MARGIN, 18*mm, W - MARGIN, 18*mm, color=GOLD, width=0.8)

    # Thin navy rule
    draw_line(c, MARGIN, 15*mm, W - MARGIN, 15*mm, color=NAVY, width=0.25)

    # Page number (centered)
    c.setFont("Cairo-Medium", 8)
    c.setFillColor(NAVY)
    c.drawCentredString(W/2, 10*mm, str(page_num))

    # Gold dot on each side of page number
    c.setFillColor(GOLD)
    c.circle(W/2 - 10*mm, 10.5*mm, 1*mm, fill=1, stroke=0)
    c.circle(W/2 + 10*mm, 10.5*mm, 1*mm, fill=1, stroke=0)

    # Section label right
    if section_title:
        draw_text_rtl(c, section_title,
                      W - MARGIN, 10*mm,
                      "Cairo-Regular", 7, color=GRAY_DARK, anchor="right")

    # Year left
    c.setFont("Cairo-Regular", 7)
    c.setFillColor(GRAY_DARK)
    c.drawString(MARGIN, 10*mm, ar("2026"))

    # Thin gold bottom strip
    draw_rect(c, 0, 0, W, 4*mm, fill=NAVY)

# ─────────────────────────────────────────────
#  PLACEHOLDER BOXES
# ─────────────────────────────────────────────
def placeholder_box(c, x, y, w, h, label="", style="default"):
    """Draw a styled placeholder box."""
    styles = {
        "default":    (GRAY_LIGHT, GRAY_MID, 0.5),
        "chart":      (GOLD_PALE,  GOLD,     0.8),
        "image":      (GRAY_LIGHT, NAVY_MID, 0.5),
        "highlight":  (NAVY,       GOLD,     1.0),
        "table":      (OFF_WHITE,  NAVY_MID, 0.5),
        "infographic":(GOLD_PALE,  GOLD,     0.8),
    }
    fill, border, bw = styles.get(style, styles["default"])
    draw_rect(c, x, y, w, h, fill=fill, stroke=border, stroke_width=bw)

    # Diagonal cross pattern for visual placeholder
    c.saveState()
    c.setStrokeColor(border)
    c.setLineWidth(0.3)
    c.setStrokeAlpha(0.3)
    c.line(x, y, x+w, y+h)
    c.line(x+w, y, x, y+h)
    c.restoreState()

    if label:
        txt_color = WHITE if style == "highlight" else GRAY_DARK
        c.setFont("Cairo-Regular", 7)
        c.setFillColor(txt_color)
        c.drawCentredString(x + w/2, y + h/2 - 3, ar(label))

def kpi_card(c, x, y, w, h, number_text="٠٠٠", label="مؤشر", accent=GOLD):
    """Draw a KPI metric card."""
    draw_rect(c, x, y, w, h, fill=WHITE, stroke=GRAY_LIGHT, stroke_width=0.5)
    # Top accent bar
    draw_rect(c, x, y + h - 2.5*mm, w, 2.5*mm, fill=accent)
    # Number
    draw_text_rtl(c, number_text, x + w/2, y + h*0.45,
                  "Cairo-Black", 20, color=NAVY, anchor="center")
    # Label
    draw_text_rtl(c, label, x + w/2, y + h*0.22,
                  "Cairo-Regular", 7, color=GRAY_DARK, anchor="center")

# ─────────────────────────────────────────────
#  PAGE 1: COVER
# ─────────────────────────────────────────────
def page_cover(c):
    c.setPageSize(A4)
    draw_cover_background(c)

    panel_w = W * 0.42
    right_x = panel_w + 18*mm

    # ── LOGO AREA (top-left on green panel) ──
    lx, ly = 15*mm, H - 38*mm
    lw, lh = panel_w - 30*mm, 18*mm
    c.saveState()
    c.setStrokeColor(colors.Color(GOLD.red, GOLD.green, GOLD.blue, 0.5))
    c.setLineWidth(0.6)
    c.setFillColor(colors.Color(1, 1, 1, 0.05))
    c.roundRect(lx, ly, lw, lh, 2*mm, fill=1, stroke=1)
    c.restoreState()
    draw_text_rtl(c, "شعار الجهة / Organization Logo",
                  lx + lw/2, ly + lh/2 - 3,
                  "Cairo-Regular", 6.5, color=GOLD_LIGHT, anchor="center")

    # ── MAIN TITLE (right panel) ──
    title_y = H * 0.68
    draw_text_rtl(c, "عنوان التقرير الرئيسي",
                  W - 18*mm, title_y + 10*mm,
                  "Cairo-Black", 22, color=WHITE, anchor="right")
    draw_text_rtl(c, "يُكتب هنا العنوان الفرعي للتقرير بشكل واضح",
                  W - 18*mm, title_y - 8*mm,
                  "Cairo-Regular", 11, color=GOLD_LIGHT, anchor="right")

    # Gold divider under title
    draw_line(c, right_x, title_y - 14*mm, W - 18*mm, title_y - 14*mm,
              color=GOLD, width=1.5)

    # ── REPORT TYPE TAG ──
    tag_y = title_y + 30*mm
    draw_text_rtl(c, "تقرير استراتيجي  |  Strategic Report",
                  W - 18*mm, tag_y,
                  "DIN-Light", 8.5, color=GOLD, anchor="right")

    # ── AUTHOR / ENTITY ──
    auth_y = title_y - 30*mm
    draw_text_rtl(c, "اسم الجهة / الباحث",
                  W - 18*mm, auth_y,
                  "Cairo-SemiBold", 10, color=WHITE, anchor="right")
    draw_text_rtl(c, "المسمى الوظيفي أو القسم",
                  W - 18*mm, auth_y - 8*mm,
                  "Cairo-Regular", 8, color=GOLD_LIGHT, anchor="right")

    # ── DATE & VERSION ──
    draw_text_rtl(c, "الإصدار الأول  |  يناير 2026",
                  W - 18*mm, auth_y - 20*mm,
                  "DIN-Light", 8, color=GRAY_MID, anchor="right")

    # ── CONFIDENTIALITY BADGE ──
    bx, by = right_x, auth_y - 35*mm
    bw, bh = 42*mm, 8*mm
    draw_rect(c, bx, by, bw, bh, fill=GOLD)
    draw_text_rtl(c, "سري  •  CONFIDENTIAL",
                  bx + bw/2, by + 2*mm,
                  "Cairo-Bold", 7, color=NAVY, anchor="center")

    # ── BOTTOM GOLD BAR CONTENT ──
    draw_text_rtl(c, "جميع الحقوق محفوظة © 2026  •  لا يُعاد توزيع هذه الوثيقة دون إذن مسبق",
                  W/2, 5*mm,
                  "Cairo-Regular", 6, color=NAVY, anchor="center")

    # ── LEFT PANEL TAGLINE ──
    draw_text_rtl(c, "نحو مستقبل أفضل",
                  panel_w/2, H * 0.12,
                  "Cairo-Bold", 13, color=WHITE, anchor="center")
    draw_text_rtl(c, "Towards a Better Future",
                  panel_w/2, H * 0.12 - 10*mm,
                  "DIN-Light", 8, color=GOLD_LIGHT, anchor="center")
    draw_line(c, 20*mm, H * 0.12 - 14*mm, panel_w - 20*mm, H * 0.12 - 14*mm,
              color=GOLD, width=0.5)

    c.showPage()

# ─────────────────────────────────────────────
#  PAGE 2: TABLE OF CONTENTS
# ─────────────────────────────────────────────
def page_toc(c, page_num=2):
    c.setPageSize(A4)
    draw_rect(c, 0, 0, W, H, fill=OFF_WHITE)

    draw_header(c, "فهرس المحتويات")
    draw_footer(c, page_num, "فهرس المحتويات")

    # ── TITLE BLOCK ──
    title_y = H - 38*mm
    draw_rect(c, MARGIN, title_y - 4*mm, CONTENT_W, 16*mm, fill=NAVY)
    draw_text_rtl(c, "فهرس المحتويات",
                  W - MARGIN - 5*mm, title_y + 4*mm,
                  "Cairo-Bold", 15, color=WHITE, anchor="right")
    draw_text_rtl(c, "Table of Contents",
                  MARGIN + 5*mm, title_y + 4*mm,
                  "DIN-Light", 8, color=GOLD_LIGHT, anchor="left")

    # Gold strip on left of title block
    draw_rect(c, MARGIN, title_y - 4*mm, 4*mm, 16*mm, fill=GOLD)

    # ── TOC ENTRIES ──
    sections = [
        ("01", "الملخص التنفيذي",         "Executive Summary",      "03"),
        ("02", "السياق والمنهجية",         "Context & Methodology",  "07"),
        ("03", "نتائج التحليل والبيانات",  "Analysis & Data",        "12"),
        ("04", "المحاور الاستراتيجية",     "Strategic Pillars",      "18"),
        ("05", "خارطة الطريق والتنفيذ",    "Roadmap & Execution",    "25"),
        ("06", "المؤشرات والأهداف",        "KPIs & Targets",         "31"),
        ("07", "الملاحق والمراجع",         "Appendices",             "38"),
    ]

    entry_h = 14*mm
    start_y = title_y - 16*mm
    colors_alt = [WHITE, GRAY_LIGHT]

    for i, (num, ar_title, en_title, pg) in enumerate(sections):
        ey = start_y - i * entry_h
        bg = WHITE if i % 2 == 0 else GRAY_LIGHT
        draw_rect(c, MARGIN, ey - entry_h + 2*mm, CONTENT_W, entry_h - 1*mm, fill=bg)

        # Number circle
        cx_ = MARGIN + 8*mm
        cy_ = ey - entry_h/2 + 2*mm
        c.setFillColor(GOLD if i == 0 else NAVY)
        c.circle(cx_, cy_, 5*mm, fill=1, stroke=0)
        c.setFont("Cairo-Bold", 8)
        c.setFillColor(WHITE)
        c.drawCentredString(cx_, cy_ - 2.5, num)

        # Arabic title
        draw_text_rtl(c, ar_title,
                      W - MARGIN - 5*mm, ey - entry_h*0.38,
                      "Cairo-SemiBold", 10, color=TEXT_DARK, anchor="right")
        # English subtitle
        draw_text_rtl(c, en_title,
                      W - MARGIN - 5*mm, ey - entry_h*0.72,
                      "DIN-Light", 7, color=GRAY_MID, anchor="right")

        # Dotted line
        c.saveState()
        c.setStrokeColor(GRAY_MID)
        c.setLineWidth(0.3)
        c.setDash([1, 3])
        c.line(MARGIN + 20*mm, cy_, W - MARGIN - 20*mm, cy_)
        c.restoreState()

        # Page number
        c.setFont("Cairo-Bold", 9)
        c.setFillColor(GOLD if i == 0 else NAVY)
        c.drawString(MARGIN + 5*mm, ey - entry_h*0.55, pg)

    c.showPage()

# ─────────────────────────────────────────────
#  PAGE 3: SECTION DIVIDER
# ─────────────────────────────────────────────
def page_section_divider(c, section_num="01", section_title="الملخص التنفيذي",
                          section_en="Executive Summary", page_num=3):
    c.setPageSize(A4)

    # Full dark background
    draw_rect(c, 0, 0, W, H, fill=NAVY)

    # Left gold stripe
    draw_rect(c, 0, 0, 8*mm, H, fill=GOLD)

    # Decorative large number (watermark style)
    c.saveState()
    c.setFont("Cairo-Black", 140)
    c.setFillColor(colors.Color(GOLD.red, GOLD.green, GOLD.blue, 0.07))
    c.drawCentredString(W/2, H*0.25, section_num)
    c.restoreState()

    # Islamic star pattern (center-right)
    draw_islamic_star(c, W*0.75, H*0.55, 80*mm, 38*mm, n=12, alpha=0.08)
    draw_islamic_star(c, W*0.75, H*0.55, 58*mm, 27*mm, n=12, alpha=0.06)
    draw_islamic_star(c, W*0.75, H*0.55, 38*mm, 18*mm, n=12, alpha=0.05)

    # Small accent circle
    c.saveState()
    c.setFillColor(colors.Color(GOLD.red, GOLD.green, GOLD.blue, 0.15))
    c.circle(W*0.75, H*0.55, 90*mm, fill=1, stroke=0)
    c.restoreState()

    # Section number
    draw_text_rtl(c, f"القسم {section_num}",
                  W - 18*mm, H*0.72,
                  "DIN-Light", 10, color=GOLD, anchor="right")

    # Horizontal gold line
    draw_line(c, 18*mm, H*0.65, W - 18*mm, H*0.65, color=GOLD, width=1.0)

    # Section title
    draw_text_rtl(c, section_title,
                  W - 18*mm, H*0.57,
                  "Cairo-Black", 28, color=WHITE, anchor="right")

    # English subtitle
    draw_text_rtl(c, section_en,
                  W - 18*mm, H*0.49,
                  "DIN-Light", 12, color=GOLD_LIGHT, anchor="right")

    # Short description placeholder
    draw_text_rtl(c, "يتضمن هذا القسم عرضاً شاملاً للنتائج والتوصيات الرئيسية",
                  W - 18*mm, H*0.42,
                  "Cairo-Regular", 9, color=GRAY_MID, anchor="right")

    # Bottom left: page number
    c.setFont("Cairo-Bold", 11)
    c.setFillColor(GOLD)
    c.drawString(18*mm, 20*mm, str(page_num))
    c.setFont("Cairo-Regular", 7)
    c.setFillColor(GRAY_MID)
    c.drawString(18*mm, 14*mm, ar("رقم الصفحة"))

    c.showPage()

# ─────────────────────────────────────────────
#  PAGE 4: TEXT CONTENT PAGE
# ─────────────────────────────────────────────
def page_text_content(c, page_num=4):
    c.setPageSize(A4)
    draw_rect(c, 0, 0, W, H, fill=WHITE)

    draw_header(c, "الملخص التنفيذي")
    draw_footer(c, page_num, "الملخص التنفيذي")

    content_top = H - 30*mm
    content_bot = 25*mm

    # ── PAGE TITLE ──
    draw_text_rtl(c, "الملخص التنفيذي",
                  W - MARGIN, content_top,
                  "Cairo-Black", 18, color=NAVY, anchor="right")
    draw_text_rtl(c, "Executive Summary",
                  W - MARGIN, content_top - 8*mm,
                  "DIN-Light", 9, color=GOLD, anchor="right")

    # Gold underline
    draw_line(c, MARGIN, content_top - 13*mm, W - MARGIN, content_top - 13*mm,
              color=GOLD, width=1.2)

    # Gold dot accent on line
    c.setFillColor(GOLD)
    c.circle(W - MARGIN, content_top - 13*mm, 2*mm, fill=1, stroke=0)

    # ── TWO-COLUMN LAYOUT ──
    col_gap = 8*mm
    col_w = (CONTENT_W - col_gap) / 2
    left_x  = MARGIN
    right_x = MARGIN + col_w + col_gap
    text_top = content_top - 22*mm

    # ── RIGHT COLUMN (primary) ──
    # Subheader
    draw_text_rtl(c, "مقدمة وخلفية الموضوع",
                  right_x + col_w, text_top,
                  "Cairo-Bold", 11, color=NAVY, anchor="right")
    draw_line(c, right_x, text_top - 4*mm, right_x + col_w, text_top - 4*mm,
              color=NAVY_MID, width=0.3)

    # Body text placeholder rows
    para_y = text_top - 10*mm
    line_h = 5.8*mm
    for i in range(8):
        line_w = col_w if i < 7 else col_w * 0.6
        draw_rect(c, right_x + col_w - line_w, para_y - i*line_h,
                  line_w, 3.5*mm, fill=GRAY_LIGHT)

    # Second sub-section
    sub2_y = para_y - 9*line_h - 8*mm
    draw_text_rtl(c, "أهداف التقرير ونطاقه",
                  right_x + col_w, sub2_y,
                  "Cairo-Bold", 11, color=NAVY, anchor="right")
    draw_line(c, right_x, sub2_y - 4*mm, right_x + col_w, sub2_y - 4*mm,
              color=NAVY_MID, width=0.3)

    # Bullet list placeholder
    bullets = ["النقطة الأولى من أهداف التقرير الرئيسية",
               "النقطة الثانية والتوجه الاستراتيجي",
               "النقطة الثالثة والمنهجية المتبعة",
               "النقطة الرابعة والنتائج المتوقعة"]
    for j, bullet in enumerate(bullets):
        by = sub2_y - 10*mm - j*8*mm
        c.setFillColor(GOLD)
        c.circle(right_x + col_w - 2*mm, by + 2*mm, 1.5*mm, fill=1, stroke=0)
        draw_rect(c, right_x, by, col_w - 6*mm, 3.5*mm, fill=GRAY_LIGHT)

    # ── LEFT COLUMN (callout / statistics) ──
    # Navy callout box
    box_h = 52*mm
    draw_rect(c, left_x, text_top - box_h, col_w, box_h, fill=NAVY)
    draw_rect(c, left_x, text_top - 3*mm, 3*mm, box_h + 3*mm, fill=GOLD)
    draw_text_rtl(c, "الرقم الرئيسي",
                  left_x + col_w - 5*mm, text_top - 10*mm,
                  "Cairo-Bold", 9, color=GOLD, anchor="right")
    draw_text_rtl(c, "٩٥٪",
                  left_x + col_w/2, text_top - 28*mm,
                  "Cairo-Black", 32, color=WHITE, anchor="center")
    draw_text_rtl(c, "معدل الإنجاز العام",
                  left_x + col_w - 5*mm, text_top - 45*mm,
                  "Cairo-Regular", 8, color=GOLD_LIGHT, anchor="right")

    # Info box below
    info_y = text_top - box_h - 8*mm
    draw_rect(c, left_x, info_y - 30*mm, col_w, 30*mm,
              fill=GOLD_PALE, stroke=GOLD, stroke_width=0.5)
    draw_text_rtl(c, "ملاحظة مهمة",
                  left_x + col_w - 5*mm, info_y - 7*mm,
                  "Cairo-Bold", 9, color=NAVY, anchor="right")
    for k in range(3):
        draw_rect(c, left_x + 3*mm, info_y - 14*mm - k*6*mm,
                  col_w - 6*mm, 3.5*mm, fill=GOLD_LIGHT)

    # Quote / Highlight box
    q_y = info_y - 45*mm
    draw_rect(c, left_x, q_y - 28*mm, col_w, 28*mm, fill=DARK_GREEN)
    draw_rect(c, left_x + col_w - 3*mm, q_y - 28*mm, 3*mm, 28*mm, fill=GOLD)
    c.setFont("Cairo-Bold", 22)
    c.setFillColor(colors.Color(GOLD.red, GOLD.green, GOLD.blue, 0.3))
    c.drawString(left_x + 4*mm, q_y - 12*mm, "\u201c")
    draw_text_rtl(c, "الاستدامة والتميز",
                  left_x + col_w - 5*mm, q_y - 14*mm,
                  "Cairo-Bold", 10, color=WHITE, anchor="right")
    draw_text_rtl(c, "هدفنا الاستراتيجي",
                  left_x + col_w - 5*mm, q_y - 22*mm,
                  "Cairo-Regular", 8, color=GOLD_LIGHT, anchor="right")

    c.showPage()

# ─────────────────────────────────────────────
#  PAGE 5: CHARTS & DATA
# ─────────────────────────────────────────────
def draw_bar_chart(c, x, y, w, h, title="مخطط بياني"):
    """Draw a placeholder styled bar chart."""
    draw_rect(c, x, y, w, h, fill=WHITE, stroke=GRAY_LIGHT, stroke_width=0.5)
    draw_rect(c, x, y + h - 7*mm, w, 7*mm, fill=NAVY)
    draw_text_rtl(c, title, x + w - 5*mm, y + h - 5*mm,
                  "Cairo-Bold", 8, color=WHITE, anchor="right")

    bar_data = [0.45, 0.70, 0.55, 0.85, 0.60, 0.90, 0.40, 0.75]
    bar_colors = [NAVY, GOLD, NAVY_MID, GOLD, NAVY, GOLD, NAVY_MID, NAVY]
    n = len(bar_data)
    pad = 5*mm
    chart_w = w - 2*pad
    chart_h = h - 20*mm
    bar_w = (chart_w / n) * 0.65
    gap = (chart_w / n) * 0.35

    # Horizontal grid lines
    for gi in range(5):
        gy = y + pad + gi * (chart_h / 4)
        c.saveState()
        c.setStrokeColor(GRAY_LIGHT)
        c.setLineWidth(0.3)
        c.line(x + pad, gy, x + w - pad, gy)
        c.restoreState()

    for i, (val, col) in enumerate(zip(bar_data, bar_colors)):
        bx = x + pad + i * (chart_w / n)
        bh_val = val * chart_h
        by = y + pad
        draw_rect(c, bx, by, bar_w, bh_val, fill=col)
        # Value label
        c.setFont("Cairo-Bold", 6)
        c.setFillColor(GRAY_DARK)
        c.drawCentredString(bx + bar_w/2, by + bh_val + 1.5*mm, f"{int(val*100)}٪")

    # X-axis
    draw_line(c, x + pad, y + pad, x + w - pad, y + pad, color=NAVY, width=0.5)

def draw_pie_chart(c, cx, cy, r, title=""):
    """Draw a placeholder styled pie chart."""
    segments = [
        (0.35, NAVY,       "35٪"),
        (0.25, GOLD,       "25٪"),
        (0.20, MID_GREEN,  "20٪"),
        (0.12, NAVY_LIGHT, "12٪"),
        (0.08, GRAY_MID,   "8٪"),
    ]
    start = 90
    for val, col, label in segments:
        deg = val * 360
        end = start - deg
        c.setFillColor(col)
        c.setStrokeColor(WHITE)
        c.setLineWidth(1)
        path = c.beginPath()
        path.moveTo(cx, cy)
        steps = max(int(deg / 5), 2)
        for s in range(steps + 1):
            angle = math.radians(start - s * deg / steps)
            path.lineTo(cx + r * math.cos(angle), cy + r * math.sin(angle))
        path.close()
        c.drawPath(path, fill=1, stroke=1)

        # Label on segment
        mid_angle = math.radians((start + end) / 2)
        lx = cx + (r * 0.65) * math.cos(mid_angle)
        ly = cy + (r * 0.65) * math.sin(mid_angle)
        c.setFont("Cairo-Bold", 6.5)
        c.setFillColor(WHITE)
        c.drawCentredString(lx, ly - 2, label)
        start = end

    # Center hole (donut)
    c.setFillColor(WHITE)
    c.circle(cx, cy, r * 0.42, fill=1, stroke=0)
    if title:
        draw_text_rtl(c, title, cx, cy + 2*mm,
                      "Cairo-Bold", 7, color=NAVY, anchor="center")

def draw_line_chart(c, x, y, w, h, title=""):
    """Draw a placeholder styled line chart."""
    draw_rect(c, x, y, w, h, fill=WHITE, stroke=GRAY_LIGHT, stroke_width=0.5)
    draw_rect(c, x, y + h - 7*mm, w, 7*mm, fill=DARK_GREEN)
    if title:
        draw_text_rtl(c, title, x + w - 4*mm, y + h - 5*mm,
                      "Cairo-Bold", 8, color=WHITE, anchor="right")

    pad = 7*mm
    ch = h - 20*mm
    cw = w - 2*pad
    points1 = [0.2, 0.35, 0.3, 0.55, 0.5, 0.7, 0.65, 0.85]
    points2 = [0.5, 0.45, 0.6, 0.5, 0.7, 0.65, 0.8, 0.75]

    # Grid
    for gi in range(5):
        gy = y + pad + gi * ch / 4
        c.saveState(); c.setStrokeColor(GRAY_LIGHT); c.setLineWidth(0.3)
        c.line(x+pad, gy, x+w-pad, gy); c.restoreState()

    # Lines
    for pts, col, dash in [(points1, NAVY, []), (points2, GOLD, [4, 2])]:
        n = len(pts)
        coords = [(x + pad + i*cw/(n-1), y + pad + pts[i]*ch) for i in range(n)]
        c.saveState()
        c.setStrokeColor(col); c.setLineWidth(1.2)
        if dash: c.setDash(*dash)
        path = c.beginPath()
        path.moveTo(*coords[0])
        for pt in coords[1:]: path.lineTo(*pt)
        c.drawPath(path, fill=0, stroke=1)
        # Dots
        c.setFillColor(col)
        for pt in coords: c.circle(*pt, 1.5*mm, fill=1, stroke=0)
        c.restoreState()

    # X-axis
    draw_line(c, x+pad, y+pad, x+w-pad, y+pad, color=NAVY, width=0.5)

    # Legend
    lx = x + pad; ly = y + 4*mm
    c.setFillColor(NAVY); c.rect(lx, ly, 8*mm, 2*mm, fill=1, stroke=0)
    c.setFont("Cairo-Regular", 6); c.setFillColor(GRAY_DARK)
    c.drawString(lx + 10*mm, ly, ar("السنة الحالية"))
    c.saveState(); c.setStrokeColor(GOLD); c.setDash(4,2); c.setLineWidth(1.2)
    c.line(lx + 38*mm, ly + 1*mm, lx + 46*mm, ly + 1*mm); c.restoreState()
    c.setFont("Cairo-Regular", 6); c.setFillColor(GRAY_DARK)
    c.drawString(lx + 48*mm, ly, ar("السنة السابقة"))

def page_charts(c, page_num=5):
    c.setPageSize(A4)
    draw_rect(c, 0, 0, W, H, fill=OFF_WHITE)

    draw_header(c, "نتائج التحليل والبيانات")
    draw_footer(c, page_num, "نتائج التحليل")

    content_top = H - 30*mm

    # ── PAGE TITLE ──
    draw_text_rtl(c, "تحليل البيانات والمؤشرات",
                  W - MARGIN, content_top,
                  "Cairo-Black", 16, color=NAVY, anchor="right")
    draw_line(c, MARGIN, content_top - 6*mm, W - MARGIN, content_top - 6*mm,
              color=GOLD, width=1.0)

    # ── KPI CARDS ROW ──
    kpi_y = content_top - 20*mm
    kpi_w = (CONTENT_W - 3*4*mm) / 4
    kpis = [
        ("٩٥٪", "نسبة الإنجاز", GOLD),
        ("١٢٠", "عدد المستفيدين (ألف)", NAVY),
        ("٣٨", "مشروع منجز", MID_GREEN),
        ("٤.٨", "مؤشر الرضا / ٥", GOLD),
    ]
    for i, (num, label, accent) in enumerate(kpis):
        kx = MARGIN + i * (kpi_w + 4*mm)
        kpi_card(c, kx, kpi_y - 20*mm, kpi_w, 20*mm, num, label, accent)

    # ── BAR CHART (full width) ──
    bar_y = kpi_y - 28*mm - 55*mm
    draw_bar_chart(c, MARGIN, bar_y, CONTENT_W, 55*mm,
                   "المقارنة السنوية للأداء  |  Annual Performance Comparison")

    # ── PIE + LINE CHARTS (side by side) ──
    chart_y = bar_y - 8*mm - 65*mm
    pie_w = CONTENT_W * 0.42
    line_w = CONTENT_W - pie_w - 6*mm

    # Pie chart container
    draw_rect(c, MARGIN, chart_y, pie_w, 65*mm,
              fill=WHITE, stroke=GRAY_LIGHT, stroke_width=0.5)
    draw_rect(c, MARGIN, chart_y + 65*mm - 7*mm, pie_w, 7*mm, fill=GOLD)
    draw_text_rtl(c, "توزيع الفئات",
                  MARGIN + pie_w - 4*mm, chart_y + 65*mm - 5*mm,
                  "Cairo-Bold", 8, color=NAVY, anchor="right")
    draw_pie_chart(c, MARGIN + pie_w/2, chart_y + 30*mm, 22*mm, "التوزيع")

    # Legend for pie
    leg_items = [("35٪", "الفئة الأولى", NAVY), ("25٪", "الفئة الثانية", GOLD),
                 ("20٪", "الفئة الثالثة", MID_GREEN)]
    for li, (pct, lbl, col) in enumerate(leg_items):
        lly = chart_y + 12*mm - li*6*mm
        c.setFillColor(col)
        c.rect(MARGIN + 3*mm, lly, 5*mm, 3*mm, fill=1, stroke=0)
        draw_text_rtl(c, f"{lbl}  {pct}",
                      MARGIN + pie_w - 3*mm, lly,
                      "Cairo-Regular", 6, color=GRAY_DARK, anchor="right")

    # Line chart
    draw_line_chart(c, MARGIN + pie_w + 6*mm, chart_y, line_w, 65*mm,
                    "الاتجاه الزمني للمؤشرات  |  Trend Analysis")

    c.showPage()

# ─────────────────────────────────────────────
#  PAGE 6: INFOGRAPHIC PAGE
# ─────────────────────────────────────────────
def page_infographic(c, page_num=6):
    c.setPageSize(A4)
    draw_rect(c, 0, 0, W, H, fill=WHITE)

    draw_header(c, "المحاور الاستراتيجية")
    draw_footer(c, page_num, "المحاور الاستراتيجية")

    content_top = H - 30*mm

    draw_text_rtl(c, "المحاور الاستراتيجية الخمسة",
                  W - MARGIN, content_top,
                  "Cairo-Black", 16, color=NAVY, anchor="right")
    draw_text_rtl(c, "Five Strategic Pillars",
                  W - MARGIN, content_top - 8*mm,
                  "DIN-Light", 9, color=GOLD, anchor="right")
    draw_line(c, MARGIN, content_top - 13*mm, W - MARGIN, content_top - 13*mm,
              color=GOLD, width=1.0)

    # ── CENTRAL CIRCLE (hub) ──
    hub_cx = W / 2
    hub_cy = H * 0.48
    hub_r  = 25*mm

    # Spoke lines first
    pillars = [
        ("التميز المؤسسي",     "Institutional Excellence", NAVY,       135),
        ("التحول الرقمي",      "Digital Transformation",   GOLD,       63),
        ("الشراكات الاستراتيجية","Strategic Partnerships", MID_GREEN,  -9),
        ("التنمية البشرية",    "Human Development",        NAVY_MID,  -81),
        ("الاستدامة",          "Sustainability",           DARK_GREEN,-153),
    ]

    for ar_t, en_t, col, angle_deg in pillars:
        angle = math.radians(angle_deg)
        sx = hub_cx + hub_r * math.cos(angle)
        sy = hub_cy + hub_r * math.sin(angle)
        ex = hub_cx + 68*mm * math.cos(angle)
        ey = hub_cy + 68*mm * math.sin(angle)
        draw_line(c, sx, sy, ex, ey, color=col, width=1.0)

        # Outer node
        c.setFillColor(col)
        c.circle(ex, ey, 12*mm, fill=1, stroke=0)
        # White inner
        c.setFillColor(WHITE)
        c.circle(ex, ey, 9.5*mm, fill=1, stroke=0)
        c.setFillColor(col)
        c.circle(ex, ey, 7.5*mm, fill=1, stroke=0)

        # Label box near node
        lx = hub_cx + 85*mm * math.cos(angle)
        ly = hub_cy + 85*mm * math.sin(angle)
        bw, bh = 38*mm, 18*mm
        draw_rect(c, lx - bw/2, ly - bh/2, bw, bh, fill=col)
        draw_text_rtl(c, ar_t, lx, ly + 2*mm,
                      "Cairo-Bold", 7.5, color=WHITE, anchor="center")
        draw_text_rtl(c, en_t, lx, ly - 5*mm,
                      "DIN-Light", 6, color=GOLD_LIGHT if col != GOLD else NAVY,
                      anchor="center")

    # Hub circle
    c.setFillColor(NAVY)
    c.circle(hub_cx, hub_cy, hub_r + 2*mm, fill=1, stroke=0)
    c.setFillColor(GOLD)
    c.circle(hub_cx, hub_cy, hub_r, fill=1, stroke=0)
    c.setFillColor(NAVY)
    c.circle(hub_cx, hub_cy, hub_r - 4*mm, fill=1, stroke=0)
    draw_text_rtl(c, "الرؤية", hub_cx, hub_cy + 2.5*mm,
                  "Cairo-Black", 11, color=GOLD, anchor="center")
    draw_text_rtl(c, "2030", hub_cx, hub_cy - 6*mm,
                  "Cairo-Bold", 9, color=WHITE, anchor="center")

    # ── BOTTOM TIMELINE ──
    tl_y = 35*mm
    tl_x1 = MARGIN + 5*mm
    tl_x2 = W - MARGIN - 5*mm
    draw_line(c, tl_x1, tl_y, tl_x2, tl_y, color=NAVY, width=1.5)

    phases = [
        ("المرحلة الأولى", "2026", GOLD),
        ("المرحلة الثانية", "2027", NAVY),
        ("المرحلة الثالثة", "2028", MID_GREEN),
        ("المرحلة الرابعة", "2030", GOLD),
    ]
    n_phases = len(phases)
    for i, (ph, yr, col) in enumerate(phases):
        px = tl_x1 + i * (tl_x2 - tl_x1) / (n_phases - 1)
        c.setFillColor(col)
        c.circle(px, tl_y, 4*mm, fill=1, stroke=0)
        c.setFillColor(WHITE)
        c.circle(px, tl_y, 2.5*mm, fill=1, stroke=0)
        draw_text_rtl(c, ph, px, tl_y + 7*mm,
                      "Cairo-Bold", 7, color=NAVY, anchor="center")
        draw_text_rtl(c, yr, px, tl_y - 9*mm,
                      "Cairo-SemiBold", 8, color=col, anchor="center")

    c.showPage()

# ─────────────────────────────────────────────
#  PAGE 7: TABLE PAGE
# ─────────────────────────────────────────────
def page_table(c, page_num=7):
    c.setPageSize(A4)
    draw_rect(c, 0, 0, W, H, fill=OFF_WHITE)

    draw_header(c, "المؤشرات والأهداف")
    draw_footer(c, page_num, "المؤشرات والأهداف")

    content_top = H - 30*mm

    draw_text_rtl(c, "جدول مؤشرات الأداء الرئيسية",
                  W - MARGIN, content_top,
                  "Cairo-Black", 16, color=NAVY, anchor="right")
    draw_text_rtl(c, "Key Performance Indicators (KPIs)",
                  W - MARGIN, content_top - 8*mm,
                  "DIN-Light", 9, color=GOLD, anchor="right")
    draw_line(c, MARGIN, content_top - 13*mm, W - MARGIN, content_top - 13*mm,
              color=GOLD, width=1.0)

    # ── TABLE ──
    table_top = content_top - 20*mm
    col_widths = [10*mm, 55*mm, 25*mm, 25*mm, 25*mm, 22*mm, 25*mm]
    headers = ["#", "المؤشر", "الهدف", "الفعلي", "الفجوة", "التقييم", "الإجراءات"]
    row_h   = 10*mm
    header_h = 12*mm

    # Table header
    tx = MARGIN
    draw_rect(c, tx, table_top - header_h, CONTENT_W, header_h, fill=NAVY)
    cx_ = tx
    for i, (hdr, cw) in enumerate(zip(headers, col_widths)):
        draw_text_rtl(c, hdr, cx_ + cw/2, table_top - header_h*0.55,
                      "Cairo-Bold", 8, color=WHITE, anchor="center")
        if i < len(col_widths) - 1:
            draw_line(c, cx_ + cw, table_top, cx_ + cw, table_top - header_h,
                      color=NAVY_LIGHT, width=0.3)
        cx_ += cw

    # Gold left accent on header
    draw_rect(c, tx, table_top - header_h, 3*mm, header_h, fill=GOLD)

    # Table rows
    rows = [
        ["01", "نسبة تنفيذ الخطة الاستراتيجية",     "100٪", "95٪",  "+5٪", "✓", "مستمر"],
        ["02", "عدد المستفيدين من البرامج",           "١٢٠٠٠", "١١٥٠٠", "٥٠٠-", "○", "متابعة"],
        ["03", "معدل رضا المستفيدين",                "٩٠٪",  "٩٢٪",  "+2٪", "✓", "محقق"],
        ["04", "نسبة إنجاز المشاريع في موعدها",       "٨٥٪",  "٧٨٪",  "٧٪-", "△", "مراجعة"],
        ["05", "نسبة توظيف الكوادر المؤهلة",          "٩٥٪",  "٩٧٪",  "+2٪", "✓", "محقق"],
        ["06", "الميزانية المنفذة من الإجمالية",      "١٠٠٪", "٨٨٪",  "١٢٪-","○", "متابعة"],
        ["07", "عدد الشراكات المنعقدة",               "٢٠",   "٢٣",   "+3",  "✓", "محقق"],
        ["08", "مؤشر التحول الرقمي",                  "٨٠٪",  "٧٥٪",  "٥٪-", "△", "مراجعة"],
    ]

    status_colors = {"✓": MID_GREEN, "○": GOLD, "△": colors.HexColor("#E53E3E")}

    for ri, row in enumerate(rows):
        ry = table_top - header_h - (ri + 1) * row_h
        bg = WHITE if ri % 2 == 0 else GRAY_LIGHT
        draw_rect(c, tx, ry, CONTENT_W, row_h, fill=bg)

        # Left accent strip on first col
        if ri % 2 == 0:
            draw_rect(c, tx, ry, 3*mm, row_h, fill=GOLD_PALE)

        rx_ = tx
        for ci, (cell, cw) in enumerate(zip(row, col_widths)):
            font = "Cairo-Bold" if ci == 0 else "Cairo-Regular"
            size = 7.5
            if ci == 5:  # Status
                col_s = status_colors.get(cell, GRAY_MID)
                c.setFillColor(col_s)
                c.circle(rx_ + cw/2, ry + row_h/2, 3*mm, fill=1, stroke=0)
            else:
                draw_text_rtl(c, cell, rx_ + cw/2, ry + row_h*0.32,
                              font, size, color=TEXT_DARK, anchor="center")
            # Column separator
            if ci < len(col_widths) - 1:
                draw_line(c, rx_ + cw, ry, rx_ + cw, ry + row_h,
                          color=GRAY_LIGHT, width=0.3)
            rx_ += cw

        # Row bottom rule
        draw_line(c, tx, ry, tx + CONTENT_W, ry, color=GRAY_LIGHT, width=0.3)

    # Table border
    table_h = header_h + len(rows) * row_h
    draw_rect(c, tx, table_top - table_h, CONTENT_W, table_h,
              stroke=GRAY_MID, stroke_width=0.5)

    # ── LEGEND ──
    leg_y = table_top - table_h - 10*mm
    draw_text_rtl(c, "مفتاح التقييم:", W - MARGIN, leg_y,
                  "Cairo-Bold", 8, color=NAVY, anchor="right")
    legends = [("✓ محقق", MID_GREEN), ("○ متابعة", GOLD),
               ("△ مراجعة", colors.HexColor("#E53E3E"))]
    for li, (lbl, col) in enumerate(legends):
        lx_ = W - MARGIN - 35*mm - li * 35*mm
        c.setFillColor(col)
        c.circle(lx_, leg_y - 4*mm, 3*mm, fill=1, stroke=0)
        draw_text_rtl(c, lbl, lx_ - 5*mm, leg_y - 6*mm,
                      "Cairo-Regular", 7, color=GRAY_DARK, anchor="right")

    c.showPage()

# ─────────────────────────────────────────────
#  PAGE 8: IMAGE + TEXT LAYOUT
# ─────────────────────────────────────────────
def page_image_text(c, page_num=8):
    c.setPageSize(A4)
    draw_rect(c, 0, 0, W, H, fill=WHITE)

    draw_header(c, "خارطة الطريق والتنفيذ")
    draw_footer(c, page_num, "خارطة الطريق")

    content_top = H - 30*mm

    draw_text_rtl(c, "خارطة الطريق التنفيذية",
                  W - MARGIN, content_top,
                  "Cairo-Black", 16, color=NAVY, anchor="right")
    draw_line(c, MARGIN, content_top - 6*mm, W - MARGIN, content_top - 6*mm,
              color=GOLD, width=1.0)

    # ── FULL-WIDTH IMAGE PLACEHOLDER ──
    img_h = 72*mm
    img_y = content_top - 10*mm - img_h
    placeholder_box(c, MARGIN, img_y, CONTENT_W, img_h,
                    "صورة / رسم بياني / خريطة ذهنية - Image / Diagram / Mind Map",
                    style="image")
    # Image caption
    draw_text_rtl(c, "الشكل (١): خارطة الطريق الاستراتيجية للمرحلة الأولى 2026-2027",
                  W - MARGIN, img_y - 5*mm,
                  "Cairo-Regular", 7.5, color=GRAY_DARK, anchor="right")
    c.setFont("Cairo-Regular", 7.5)
    c.setFillColor(GRAY_MID)
    c.drawString(MARGIN, img_y - 5*mm, ar("المصدر: إدارة التخطيط والتطوير"))

    # ── TWO COLUMN TEXT BELOW IMAGE ──
    col_gap = 8*mm
    col_w = (CONTENT_W - col_gap) / 2
    text_y = img_y - 18*mm

    # RIGHT COLUMN
    rx = MARGIN + col_w + col_gap
    draw_rect(c, rx, text_y - 3*mm, 3*mm, 3*mm + 5*mm, fill=GOLD)
    draw_text_rtl(c, "الأهداف قصيرة المدى",
                  rx + col_w, text_y + 4*mm,
                  "Cairo-Bold", 10, color=NAVY, anchor="right")
    for i in range(5):
        by = text_y - 4*mm - i * 7*mm
        c.setFillColor(GOLD)
        c.circle(rx + col_w - 2*mm, by + 2.5*mm, 1.5*mm, fill=1, stroke=0)
        draw_rect(c, rx, by, col_w - 6*mm, 3.5*mm, fill=GRAY_LIGHT)

    # LEFT COLUMN
    lx = MARGIN
    draw_rect(c, lx, text_y - 3*mm, 3*mm, 3*mm + 5*mm, fill=NAVY)
    draw_text_rtl(c, "الأهداف بعيدة المدى",
                  lx + col_w, text_y + 4*mm,
                  "Cairo-Bold", 10, color=NAVY, anchor="right")
    for i in range(5):
        by = text_y - 4*mm - i * 7*mm
        c.setFillColor(NAVY)
        c.circle(lx + col_w - 2*mm, by + 2.5*mm, 1.5*mm, fill=1, stroke=0)
        draw_rect(c, lx, by, col_w - 6*mm, 3.5*mm, fill=GRAY_LIGHT)

    # ── PROGRESS BARS ──
    prog_y = text_y - 50*mm
    draw_text_rtl(c, "نسب الإنجاز",
                  W - MARGIN, prog_y + 6*mm,
                  "Cairo-Bold", 10, color=NAVY, anchor="right")
    draw_line(c, MARGIN, prog_y + 2*mm, W - MARGIN, prog_y + 2*mm,
              color=GRAY_LIGHT, width=0.3)

    prog_items = [
        ("المحور الأول: التميز المؤسسي", 0.88, NAVY),
        ("المحور الثاني: التحول الرقمي",  0.72, GOLD),
        ("المحور الثالث: الشراكات",        0.65, MID_GREEN),
        ("المحور الرابع: التنمية البشرية", 0.91, NAVY_MID),
    ]
    bar_total_w = CONTENT_W - 30*mm
    for pi, (label, pct, col) in enumerate(prog_items):
        py = prog_y - pi * 10*mm
        draw_text_rtl(c, label, W - MARGIN, py,
                      "Cairo-Regular", 8, color=TEXT_DARK, anchor="right")
        # Background bar
        draw_rect(c, MARGIN, py - 5*mm, bar_total_w, 4*mm, fill=GRAY_LIGHT)
        # Progress fill
        draw_rect(c, MARGIN, py - 5*mm, bar_total_w * pct, 4*mm, fill=col)
        # Percentage label
        c.setFont("Cairo-Bold", 7)
        c.setFillColor(col)
        c.drawString(MARGIN + bar_total_w + 3*mm, py - 4*mm,
                     f"{int(pct*100)}٪")

    c.showPage()

# ─────────────────────────────────────────────
#  PAGE 9: QUOTE / HIGHLIGHT PAGE
# ─────────────────────────────────────────────
def page_highlight(c, page_num=9):
    c.setPageSize(A4)

    # Dark gradient background
    draw_rect(c, 0, 0, W, H, fill=DARK_GREEN)

    # Islamic pattern overlay
    draw_islamic_star(c, W/2, H/2, 120*mm, 55*mm, n=16, alpha=0.05)
    draw_islamic_star(c, W/2, H/2, 90*mm, 42*mm,  n=16, alpha=0.04)
    draw_islamic_star(c, W/2, H/2, 60*mm, 28*mm,  n=16, alpha=0.06)
    draw_islamic_star(c, W/2, H/2, 32*mm, 15*mm,  n=12, alpha=0.07)

    # Top/bottom gold bars
    draw_rect(c, 0, H - 4*mm, W, 4*mm, fill=GOLD)
    draw_rect(c, 0, 0, W, 4*mm, fill=GOLD)

    # Left/right gold stripes
    draw_rect(c, 0, 0, 4*mm, H, fill=GOLD)
    draw_rect(c, W - 4*mm, 0, 4*mm, H, fill=GOLD)

    # Central quote box
    qbox_w = CONTENT_W * 0.85
    qbox_h = 80*mm
    qbox_x = (W - qbox_w) / 2
    qbox_y = (H - qbox_h) / 2

    # Subtle box background
    c.saveState()
    c.setFillColor(colors.Color(1, 1, 1, 0.05))
    c.roundRect(qbox_x, qbox_y, qbox_w, qbox_h, 3*mm, fill=1, stroke=0)
    c.restoreState()

    # Gold top border on quote box
    draw_rect(c, qbox_x, qbox_y + qbox_h - 2*mm, qbox_w, 2*mm, fill=GOLD)

    # Large decorative quote mark
    c.saveState()
    c.setFont("Cairo-Black", 80)
    c.setFillColor(colors.Color(GOLD.red, GOLD.green, GOLD.blue, 0.25))
    c.drawString(qbox_x + 5*mm, qbox_y + qbox_h - 30*mm, "\u201c")
    c.restoreState()

    # Quote text
    draw_text_rtl(c, "نص الاقتباس أو الرسالة الرئيسية يُكتب هنا",
                  qbox_x + qbox_w - 8*mm, qbox_y + qbox_h - 28*mm,
                  "Cairo-Black", 18, color=WHITE, anchor="right")
    draw_text_rtl(c, "بجملة داعمة أو توضيحية في السطر الثاني",
                  qbox_x + qbox_w - 8*mm, qbox_y + qbox_h - 42*mm,
                  "Cairo-Regular", 13, color=GOLD_LIGHT, anchor="right")

    # Divider
    draw_line(c, qbox_x + 10*mm, qbox_y + qbox_h - 50*mm,
              qbox_x + qbox_w - 10*mm, qbox_y + qbox_h - 50*mm,
              color=GOLD, width=0.5)

    # Attribution
    draw_text_rtl(c, "— اسم صاحب الاقتباس أو الجهة",
                  qbox_x + qbox_w - 8*mm, qbox_y + 12*mm,
                  "Cairo-SemiBold", 9.5, color=GOLD, anchor="right")
    draw_text_rtl(c, "المسمى الوظيفي أو السياق",
                  qbox_x + qbox_w - 8*mm, qbox_y + 5*mm,
                  "Cairo-Regular", 8, color=GOLD_LIGHT, anchor="right")

    # Three dots decorative
    for di in range(3):
        dx = W/2 - 8*mm + di*8*mm
        c.setFillColor(GOLD)
        c.circle(dx, qbox_y - 10*mm, 2*mm if di == 1 else 1.2*mm, fill=1, stroke=0)

    # Corner ornaments
    corner_size = 15*mm
    corners = [(8*mm, H-8*mm), (W-8*mm, H-8*mm), (8*mm, 8*mm), (W-8*mm, 8*mm)]
    for (cx_, cy_) in corners:
        c.saveState()
        c.setStrokeColor(GOLD)
        c.setLineWidth(0.8)
        c.setStrokeAlpha(0.5)
        c.circle(cx_, cy_, 5*mm, fill=0, stroke=1)
        c.circle(cx_, cy_, 3*mm, fill=0, stroke=1)
        c.restoreState()

    # Page number
    c.setFont("Cairo-Bold", 9)
    c.setFillColor(GOLD)
    c.drawCentredString(W/2, 8*mm, str(page_num))

    c.showPage()

# ─────────────────────────────────────────────
#  PAGE 10: BACK COVER
# ─────────────────────────────────────────────
def page_back_cover(c):
    c.setPageSize(A4)

    # Navy full background
    draw_rect(c, -BLEED, -BLEED, W + 2*BLEED, H + 2*BLEED, fill=NAVY)

    # Gold bottom band
    draw_rect(c, -BLEED, -BLEED, W + 2*BLEED, H*0.35 + BLEED, fill=DARK_GREEN)

    # Diagonal separator
    c.saveState()
    c.setStrokeColor(GOLD)
    c.setLineWidth(2)
    c.line(-BLEED, H*0.35 + 8*mm, W + BLEED, H*0.35 - 8*mm)
    c.restoreState()

    # Islamic pattern
    draw_islamic_star(c, W*0.82, H*0.72, 70*mm, 32*mm, n=12, alpha=0.06)
    draw_islamic_star(c, W*0.15, H*0.22, 50*mm, 23*mm, n=8,  alpha=0.05)

    # Top section: Thank you
    draw_text_rtl(c, "شكراً لاهتمامكم",
                  W/2, H*0.72,
                  "Cairo-Black", 28, color=WHITE, anchor="center")
    draw_text_rtl(c, "Thank You",
                  W/2, H*0.63,
                  "DIN-Light", 16, color=GOLD, anchor="center")
    draw_line(c, W*0.2, H*0.60, W*0.8, H*0.60, color=GOLD, width=0.8)

    # Contact info area
    draw_text_rtl(c, "للتواصل والاستفسار",
                  W/2, H*0.55,
                  "Cairo-SemiBold", 11, color=GOLD_LIGHT, anchor="center")

    contact_items = [
        ("البريد الإلكتروني:", "email@organization.com"),
        ("الهاتف:", "+966 XX XXX XXXX"),
        ("الموقع:", "www.organization.com.sa"),
        ("العنوان:", "المملكة العربية السعودية"),
    ]
    for ci, (label, val) in enumerate(contact_items):
        cy_ = H*0.48 - ci*8*mm
        draw_text_rtl(c, label, W/2 + 15*mm, cy_,
                      "Cairo-Bold", 8, color=GOLD, anchor="right")
        draw_text_rtl(c, val, W/2 - 2*mm, cy_,
                      "Cairo-Regular", 8, color=WHITE, anchor="left")

    # Logo area (bottom)
    lw, lh = 50*mm, 20*mm
    lx = (W - lw) / 2
    ly = H*0.18
    c.saveState()
    c.setStrokeColor(colors.Color(GOLD.red, GOLD.green, GOLD.blue, 0.5))
    c.setFillColor(colors.Color(1, 1, 1, 0.06))
    c.setLineWidth(0.7)
    c.roundRect(lx, ly, lw, lh, 2*mm, fill=1, stroke=1)
    c.restoreState()
    draw_text_rtl(c, "شعار الجهة",
                  lx + lw/2, ly + lh/2 - 3,
                  "Cairo-Regular", 8, color=GOLD_LIGHT, anchor="center")

    # Bottom copyright
    draw_text_rtl(c, "جميع الحقوق محفوظة  ©  2026  |  لا يُعاد نشر هذه الوثيقة دون إذن خطي",
                  W/2, H*0.08,
                  "Cairo-Regular", 6.5, color=GRAY_MID, anchor="center")

    c.showPage()

# ─────────────────────────────────────────────
#  MAIN
# ─────────────────────────────────────────────
def build_pdf():
    out_dir = r"c:/Users/mtare/Desktop/ابو عثمان"
    out_path = os.path.join(out_dir, "قالب_التقرير_الاحترافي_2026.pdf")

    c = canvas.Canvas(out_path, pagesize=A4)
    c.setTitle("قالب تقرير احترافي | Professional Report Template")
    c.setAuthor("Premium Report Generator")
    c.setSubject("Corporate Arabic Report Template - McKinsey Style")

    print("Building page 1: Cover...")
    page_cover(c)

    print("Building page 2: Table of Contents...")
    page_toc(c, page_num=2)

    print("Building page 3: Section Divider...")
    page_section_divider(c, "01", "الملخص التنفيذي", "Executive Summary", 3)

    print("Building page 4: Text Content...")
    page_text_content(c, page_num=4)

    print("Building page 5: Charts & Data...")
    page_charts(c, page_num=5)

    print("Building page 6: Infographic...")
    page_infographic(c, page_num=6)

    print("Building page 7: Table...")
    page_table(c, page_num=7)

    print("Building page 8: Image + Text...")
    page_image_text(c, page_num=8)

    print("Building page 9: Highlight / Quote...")
    page_highlight(c, page_num=9)

    print("Building page 10: Section Divider 2...")
    page_section_divider(c, "02", "التوصيات والخلاصة",
                         "Recommendations & Conclusion", 10)

    print("Building page 11: Back Cover...")
    page_back_cover(c)

    c.save()
    print(f"\n✓ PDF saved: {out_path}")
    return out_path

if __name__ == "__main__":
    build_pdf()
