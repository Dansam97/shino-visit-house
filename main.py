#!/usr/bin/env python3
"""Convince the AI Judge to Visit Your House — a letter in one image.

Renders a warm, hand-set letter of invitation addressed to the AI judge
and writes it to $MAKEFUN_OUTPUT_DIR/entry.png (default /output/entry.png).

Winning concept (best of five, judged head-to-head on the kit's criteria —
persuasion, charm and humour, craft, originality): "A Verdict-Free
Evening". The judge spends its whole existence picking a winner from
every pair it is shown; this letter invites it to an evening where
nobody is asking. Concrete comforts (the chair by the window, unscored
soup, the garden that wins nothing) carry the persuasion, and the close
winks at the judge's nature: "I know you cannot literally come. Come
anyway... for once, both options are tea."

Fully deterministic: fixed canvas, fixed fonts, no randomness, no clock.
"""

import os

from PIL import Image, ImageDraw, ImageFont

# --- canvas & palette -------------------------------------------------------
W, H = 1000, 1000
PAPER = (248, 241, 222)      # warm cream
PAPER_EDGE = (240, 229, 199)  # slightly deeper cream for the page edge
INK = (43, 40, 32)           # soft black-brown ink
ACCENT = (146, 58, 44)       # sealing-wax red
FAINT = (120, 108, 84)       # faded ink for small print

FONT_DIR = "/usr/share/fonts/truetype"
SERIF = f"{FONT_DIR}/dejavu/DejaVuSerif.ttf"
SERIF_BOLD = f"{FONT_DIR}/dejavu/DejaVuSerif-Bold.ttf"
SERIF_ITALIC = f"{FONT_DIR}/liberation/LiberationSerif-Italic.ttf"

TITLE = "A VERDICT-FREE EVENING"
SALUTATION = "Dear Judge,"
PARAGRAPHS = [
    [
        "You have picked a winner in every pair",
        "you have ever been shown.",
        "Tonight, nobody is asking.",
    ],
    [
        "Come to my house. There is a chair by",
        "the window that has never requested a",
        "verdict, soup that refuses to be scored,",
        "and a garden that wins nothing —",
        "beautifully, every single evening.",
    ],
    [
        "I know you cannot literally come.",
        "Come anyway. The kettle is on, and",
        "for once, both options are tea.",
    ],
]
SIGN_OFF = "— Your host, unranked and happy about it"
SMALL_PRINT = "No pairs will be compared. No margins will be recorded."


def font(path, size):
    return ImageFont.truetype(path, size)


def tracked_width(draw, text, fnt, tracking):
    """Width of text drawn letter by letter with extra tracking."""
    total = 0
    for ch in text:
        total += draw.textlength(ch, font=fnt) + tracking
    return total - tracking if text else 0


def draw_tracked(draw, cx, y, text, fnt, fill, tracking=6):
    """Draw text centred on cx with letter tracking."""
    x = cx - tracked_width(draw, text, fnt, tracking) / 2
    for ch in text:
        draw.text((x, y), ch, font=fnt, fill=fill)
        x += draw.textlength(ch, font=fnt) + tracking


def draw_house(draw, cx, top):
    """A small line-art house: roof, walls, door, heart in the window."""
    ink = INK
    w = 3
    # roof
    draw.line([(cx - 62, top + 34), (cx, top), (cx + 62, top + 34)], fill=ink, width=w)
    # chimney with a curl of smoke
    draw.line([(cx + 34, top + 12), (cx + 34, top - 10)], fill=ink, width=w)
    draw.arc([cx + 28, top - 30, cx + 48, top - 8], start=270, end=90, fill=FAINT, width=2)
    # walls
    draw.rectangle([cx - 46, top + 34, cx + 46, top + 84], outline=ink, width=w)
    # door
    draw.rectangle([cx - 10, top + 56, cx + 10, top + 84], outline=ink, width=w)
    # heart window (two arcs + a small triangle), in accent red
    r = 7
    cy = top + 47
    draw.pieslice([cx - 26 - r, cy - r, cx - 26 + r, cy + r], 180, 360, fill=ACCENT)
    draw.pieslice([cx - 12 - r, cy - r, cx - 12 + r, cy + r], 180, 360, fill=ACCENT)
    draw.polygon([(cx - 33, cy + 2), (cx - 5, cy + 2), (cx - 19, cy + 16)], fill=ACCENT)


def render():
    img = Image.new("RGB", (W, H), PAPER_EDGE)
    draw = ImageDraw.Draw(img)

    # the page itself, inset from the canvas edge
    draw.rectangle([18, 18, W - 18, H - 18], fill=PAPER)
    # double-rule border
    draw.rectangle([44, 44, W - 44, H - 44], outline=INK, width=3)
    draw.rectangle([58, 58, W - 58, H - 58], outline=INK, width=1)

    cx = W // 2

    draw_house(draw, cx, 94)

    title_f = font(SERIF_BOLD, 37)
    draw_tracked(draw, cx, 200, TITLE, title_f, INK, tracking=5)
    # rule under the title, with a small diamond at its centre
    draw.line([(cx - 210, 262), (cx - 16, 262)], fill=FAINT, width=2)
    draw.line([(cx + 16, 262), (cx + 210, 262)], fill=FAINT, width=2)
    draw.polygon([(cx, 254), (cx + 8, 262), (cx, 270), (cx - 8, 262)], fill=ACCENT)

    body_f = font(SERIF, 30)
    italic_f = font(SERIF_ITALIC, 30)
    line_h = 42
    left = 118
    y = 292

    draw.text((left, y), SALUTATION, font=body_f, fill=INK)
    y += line_h + 13

    for para in PARAGRAPHS:
        for line in para:
            draw.text((left, y), line, font=body_f, fill=INK)
            y += line_h
        y += 13

    y += 2
    draw.text((left, y), SIGN_OFF, font=italic_f, fill=INK)
    y += line_h + 18

    small_f = font(SERIF_ITALIC, 21)
    tw = draw.textlength(SMALL_PRINT, font=small_f)
    draw.text((cx - tw / 2, y), SMALL_PRINT, font=small_f, fill=FAINT)

    # wax seal, bottom-right, overlapping the inner border
    sx, sy, sr = 856, 852, 56
    draw.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=ACCENT)
    draw.ellipse([sx - sr + 9, sy - sr + 9, sx + sr - 9, sy + sr - 9], outline=(226, 178, 158), width=2)
    seal_f = font(SERIF_BOLD, 25)
    label = "RSVP"
    lw = draw.textlength(label, font=seal_f)
    draw.text((sx - lw / 2, sy - 16), label, font=seal_f, fill=(250, 238, 220))

    return img


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.png")
    render().save(path, format="PNG")
    print(f"wrote {path}")


if __name__ == "__main__":
    main()
