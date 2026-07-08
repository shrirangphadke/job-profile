#!/usr/bin/env python3

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
import re

from reportlab.lib.colors import HexColor, white
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen import canvas


PAGE_WIDTH, PAGE_HEIGHT = A4


@dataclass
class ResumeData:
    name: str
    contact: str
    links: str
    summary: str
    highlights: list[str]
    core_skills: list[str]
    experience_title: str
    experience_dates: str
    experience_bullets: list[str]
    earlier_experience: list[str]
    education: list[str]


def parse_markdown(path: Path) -> ResumeData:
    lines = path.read_text().splitlines()
    name = lines[0].strip("# ").strip()
    contact = lines[2].replace("  ", "").strip()
    links = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", lines[3]).strip()

    sections: dict[str, list[str]] = {}
    current = None
    for raw_line in lines[5:]:
        line = raw_line.rstrip()
        if line.startswith("## "):
            current = line[3:].strip()
            sections[current] = []
        elif current is not None:
            sections[current].append(line)

    summary = " ".join(line for line in sections["Summary"] if line.strip())
    highlights = [line[2:] for line in sections["Highlights"] if line.startswith("- ")]
    core_skills = [line[2:] for line in sections["Core Skills"] if line.startswith("- ")]

    exp_lines = sections["Experience"]
    experience_title = exp_lines[0].strip("# ").strip()
    experience_dates = exp_lines[2].strip()
    experience_bullets: list[str] = []
    earlier_experience: list[str] = []
    in_earlier = False
    for line in exp_lines[4:]:
        if line.startswith("### "):
            in_earlier = "Earlier Experience" in line
            continue
        if line.startswith("- "):
            if in_earlier:
                earlier_experience.append(line[2:])
            else:
                experience_bullets.append(line[2:])

    education = [line for line in sections["Education"] if line.strip()]
    return ResumeData(
        name=name,
        contact=contact,
        links=links,
        summary=summary,
        highlights=highlights,
        core_skills=core_skills,
        experience_title=experience_title,
        experience_dates=experience_dates,
        experience_bullets=experience_bullets,
        earlier_experience=earlier_experience,
        education=education,
    )


def wrap_text(text: str, font_name: str, font_size: float, width: float) -> list[str]:
    words = text.split()
    lines: list[str] = []
    current = ""
    for word in words:
        candidate = word if not current else f"{current} {word}"
        if stringWidth(candidate, font_name, font_size) <= width:
            current = candidate
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def draw_lines(c: canvas.Canvas, lines: list[str], x: float, y: float, font_name: str, font_size: float, color, leading: float) -> float:
    c.setFillColor(color)
    c.setFont(font_name, font_size)
    for line in lines:
        c.drawString(x, y, line)
        y -= leading
    return y


def bullet_lines(text: str, font_size: float, width: float) -> list[str]:
    wrapped = wrap_text(text, "Helvetica", font_size, width - 10)
    if not wrapped:
        return []
    lines = [f"• {wrapped[0]}"]
    lines.extend(f"  {line}" for line in wrapped[1:])
    return lines


def render_pdf(data: ResumeData, output_path: Path) -> None:
    palette = {
        "ink": HexColor("#132238"),
        "muted": HexColor("#566579"),
        "accent": HexColor("#C86B2A"),
        "panel": HexColor("#F4F7FA"),
        "rule": HexColor("#D5DEE7"),
    }

    scales = [1.0, 0.97, 0.94, 0.91, 0.88]
    for scale in scales:
        c = canvas.Canvas(str(output_path), pagesize=A4)
        margin_x = 34
        top = PAGE_HEIGHT - 34
        bottom = 28
        header_h = 86
        gutter = 18
        sidebar_w = 152
        main_x = margin_x + sidebar_w + gutter
        main_w = PAGE_WIDTH - margin_x - main_x

        c.setTitle(f"{data.name} - Resume")
        c.setStrokeColor(palette["rule"])
        c.setFillColor(palette["ink"])

        c.roundRect(margin_x, top - header_h, PAGE_WIDTH - 2 * margin_x, header_h, 12, stroke=0, fill=1)
        c.setFillColor(white)
        c.setFont("Helvetica-Bold", 21 * scale)
        c.drawString(margin_x + 18, top - 30, data.name)
        c.setFont("Helvetica", 9.2 * scale)
        c.drawString(margin_x + 18, top - 49, data.contact)
        c.drawString(margin_x + 18, top - 64, data.links)

        content_top = top - header_h - 18

        c.setFillColor(palette["panel"])
        c.roundRect(margin_x, bottom, sidebar_w, content_top - bottom, 12, stroke=0, fill=1)

        def section_header(x: float, y: float, title: str, width: float) -> float:
            c.setFillColor(palette["accent"])
            c.setFont("Helvetica-Bold", 10.2 * scale)
            c.drawString(x, y, title.upper())
            c.setStrokeColor(palette["accent"])
            c.setLineWidth(1)
            c.line(x, y - 4, x + width, y - 4)
            return y - 13

        sidebar_y = content_top - 18
        sidebar_x = margin_x + 14
        sidebar_y = section_header(sidebar_x, sidebar_y, "Core Skills", sidebar_w - 28)
        for item in data.core_skills:
            lines = bullet_lines(item, 8.2 * scale, sidebar_w - 28)
            sidebar_y = draw_lines(c, lines, sidebar_x, sidebar_y, "Helvetica", 8.2 * scale, palette["ink"], 10.0 * scale) - 2

        sidebar_y -= 6
        sidebar_y = section_header(sidebar_x, sidebar_y, "Education", sidebar_w - 28)
        for line in data.education:
            wrapped = wrap_text(line, "Helvetica", 8.0 * scale, sidebar_w - 28)
            sidebar_y = draw_lines(c, wrapped, sidebar_x, sidebar_y, "Helvetica", 8.0 * scale, palette["ink"], 9.6 * scale) - 4

        main_y = content_top
        main_y = section_header(main_x, main_y, "Summary", main_w)
        summary_lines = wrap_text(data.summary, "Helvetica", 8.9 * scale, main_w)
        main_y = draw_lines(c, summary_lines, main_x, main_y, "Helvetica", 8.9 * scale, palette["muted"], 11 * scale) - 6

        main_y = section_header(main_x, main_y, "Highlights", main_w)
        for item in data.highlights:
            lines = bullet_lines(item, 8.6 * scale, main_w)
            main_y = draw_lines(c, lines, main_x, main_y, "Helvetica", 8.6 * scale, palette["ink"], 10.6 * scale) - 2

        main_y -= 3
        main_y = section_header(main_x, main_y, "Experience", main_w)
        c.setFillColor(palette["ink"])
        c.setFont("Helvetica-Bold", 10.0 * scale)
        c.drawString(main_x, main_y, data.experience_title)
        c.setFont("Helvetica", 8.3 * scale)
        c.setFillColor(palette["muted"])
        c.drawRightString(main_x + main_w, main_y, data.experience_dates)
        main_y -= 13

        for item in data.experience_bullets:
            lines = bullet_lines(item, 8.35 * scale, main_w)
            main_y = draw_lines(c, lines, main_x, main_y, "Helvetica", 8.35 * scale, palette["ink"], 10.1 * scale) - 1.5

        main_y -= 4
        c.setFont("Helvetica-Bold", 9.2 * scale)
        c.setFillColor(palette["accent"])
        c.drawString(main_x, main_y, "Earlier Experience")
        main_y -= 11
        for item in data.earlier_experience:
            lines = bullet_lines(item.replace("**", ""), 8.0 * scale, main_w)
            main_y = draw_lines(c, lines, main_x, main_y, "Helvetica", 8.0 * scale, palette["ink"], 9.5 * scale) - 1

        if min(main_y, sidebar_y) > bottom + 6:
            c.save()
            return

    raise RuntimeError("Content did not fit on one page with current layout.")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()

    args.output.parent.mkdir(parents=True, exist_ok=True)
    data = parse_markdown(args.input)
    render_pdf(data, args.output)
    print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()
