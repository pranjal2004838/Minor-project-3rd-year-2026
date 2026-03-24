#!/usr/bin/env python3
"""Generate a formatted PDF from the project markdown guide."""

from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

ROOT = Path(__file__).resolve().parents[1]
SOURCE_MD = ROOT / "docs" / "Ultimate_Guide_DSP_Extended_5Stage_RISC.md"
OUTPUT_PDF = ROOT / "docs" / "Ultimate_Guide_DSP_Extended_5Stage_RISC.pdf"


def build_styles():
    styles = getSampleStyleSheet()
    styles.add(
        ParagraphStyle(
            name="TitleCenter",
            parent=styles["Title"],
            alignment=TA_CENTER,
            fontSize=20,
            leading=24,
            spaceAfter=14,
        )
    )
    styles.add(
        ParagraphStyle(
            name="H1",
            parent=styles["Heading1"],
            fontSize=16,
            leading=20,
            spaceBefore=12,
            spaceAfter=8,
        )
    )
    styles.add(
        ParagraphStyle(
            name="H2",
            parent=styles["Heading2"],
            fontSize=13,
            leading=17,
            spaceBefore=10,
            spaceAfter=6,
        )
    )
    styles.add(
        ParagraphStyle(
            name="Body",
            parent=styles["BodyText"],
            fontSize=10.5,
            leading=15,
            spaceAfter=6,
        )
    )
    styles.add(
        ParagraphStyle(
            name="BulletItem",
            parent=styles["BodyText"],
            fontSize=10.5,
            leading=15,
            leftIndent=16,
            bulletIndent=8,
            spaceAfter=3,
        )
    )
    styles.add(
        ParagraphStyle(
            name="Mono",
            parent=styles["Code"],
            fontSize=9,
            leading=12,
            backColor=colors.whitesmoke,
            borderPadding=5,
            spaceBefore=4,
            spaceAfter=4,
        )
    )
    return styles


def add_page_number(canvas, _doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 9)
    canvas.setFillColor(colors.grey)
    canvas.drawRightString(19.5 * cm, 1.1 * cm, f"Page {canvas.getPageNumber()}")
    canvas.restoreState()


def escape(text: str) -> str:
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace("  ", "&nbsp;&nbsp;")
    )


def build_story(md_text: str):
    styles = build_styles()
    story = []

    # Cover header table for cleaner first-page presentation.
    cover = Table(
        [["ECE Minor Project Ultimate Guide"], ["5-Stage RISC + DSP MAC Extension"]],
        colWidths=[16.5 * cm],
    )
    cover.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (0, 0), colors.HexColor("#0f4c81")),
                ("BACKGROUND", (0, 1), (0, 1), colors.HexColor("#2f7fbf")),
                ("TEXTCOLOR", (0, 0), (0, 1), colors.white),
                ("ALIGN", (0, 0), (0, 1), "CENTER"),
                ("VALIGN", (0, 0), (0, 1), "MIDDLE"),
                ("FONTSIZE", (0, 0), (0, 0), 18),
                ("FONTSIZE", (0, 1), (0, 1), 13),
                ("BOTTOMPADDING", (0, 0), (0, 0), 14),
                ("TOPPADDING", (0, 0), (0, 0), 14),
                ("BOTTOMPADDING", (0, 1), (0, 1), 12),
                ("TOPPADDING", (0, 1), (0, 1), 12),
            ]
        )
    )
    story.append(cover)
    story.append(Spacer(1, 0.35 * cm))

    in_code_block = False
    for raw_line in md_text.splitlines():
        line = raw_line.rstrip("\n")

        if line.strip() == "```":
            in_code_block = not in_code_block
            continue

        if in_code_block:
            if line.strip():
                story.append(Paragraph(escape(line), styles["Mono"]))
            else:
                story.append(Spacer(1, 0.15 * cm))
            continue

        if not line.strip():
            story.append(Spacer(1, 0.15 * cm))
            continue

        if line.startswith("# "):
            story.append(Paragraph(escape(line[2:]), styles["TitleCenter"]))
            continue

        if line.startswith("## "):
            story.append(Paragraph(escape(line[3:]), styles["H1"]))
            continue

        if line.startswith("### "):
            story.append(Paragraph(escape(line[4:]), styles["H2"]))
            continue

        if line.startswith("- "):
            story.append(Paragraph(escape(line[2:]), styles["BulletItem"], bulletText="-"))
            continue

        # Plain paragraphs and simple numbered lines.
        story.append(Paragraph(escape(line), styles["Body"]))

    return story


def main():
    if not SOURCE_MD.exists():
        raise FileNotFoundError(f"Markdown source not found: {SOURCE_MD}")

    md_text = SOURCE_MD.read_text(encoding="utf-8")
    story = build_story(md_text)

    doc = SimpleDocTemplate(
        str(OUTPUT_PDF),
        pagesize=A4,
        rightMargin=1.6 * cm,
        leftMargin=1.6 * cm,
        topMargin=1.5 * cm,
        bottomMargin=1.8 * cm,
        title="Ultimate Guide: DSP-Extended 5-Stage RISC",
        author="Minor Project Team",
    )
    doc.build(story, onFirstPage=add_page_number, onLaterPages=add_page_number)
    print(f"Generated: {OUTPUT_PDF}")


if __name__ == "__main__":
    main()
