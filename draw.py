from pathlib import Path

from PIL import Image, ImageDraw, ImageFont
import matplotlib


WIDTH = 1024
HEIGHT = 1024
BACKGROUND = "#f7f3ea"
NAVY = "#14213d"
RED = "#b3001b"
INK = "#202633"
MUTED = "#586070"
BORDER = "#d8d1c5"

stories = [
    (
        "DIPLOMACY - SHENZHEN",
        "Trump, Xi and Putin issue joint peace declaration",
        "First three-way summit of the US, Chinese and Russian leaders, held in Shenzhen, China.",
        "#9d3c2b",
    ),
    (
        "WAR - UKRAINE",
        "Russia fires 400 drones and 110 missiles at Ukraine",
        "Kyiv bridges and power grid hit; two missiles fall inside Poland.",
        "#a52a35",
    ),
    (
        "JUSTICE - THE HAGUE",
        "World Court: Myanmar committed genocide against Rohingya",
        "Landmark ICJ ruling on Myanmar's treatment of the Rohingya people.",
        "#76528b",
    ),
    (
        "BUSINESS - AI",
        "Anthropic's $81 billion IPO is the largest ever",
        "Shares open 33 percent above the offer price in a record listing.",
        "#39705b",
    ),
    (
        "MIDDLE EAST - HORMUZ",
        "US blockade of Iranian shipping holds at Hormuz",
        "Tehran threatens Gulf oil facilities and tanker convoys.",
        "#a76b22",
    ),
    (
        "CLIMATE - ANTALYA",
        "COP31 talks stall over fossil fuels on final day",
        "Negotiators deadlocked as the UN climate summit reaches its close.",
        "#397385",
    ),
]


def draw_headline(draw, text, x, y, max_width):
    font_dir = Path(matplotlib.get_data_path()) / "fonts" / "ttf"
    words = text.split()
    for size in range(31, 23, -1):
        font = ImageFont.truetype(str(font_dir / "DejaVuSans-Bold.ttf"), size)
        if draw.textbbox((0, 0), text, font=font)[2] <= max_width:
            draw.text((x, y), text, font=font, fill=NAVY)
            return y + 39
        splits = []
        for split in range(1, len(words)):
            first = " ".join(words[:split])
            second = " ".join(words[split:])
            first_width = draw.textbbox((0, 0), first, font=font)[2]
            second_width = draw.textbbox((0, 0), second, font=font)[2]
            if first_width <= max_width and second_width <= max_width:
                splits.append((abs(first_width - second_width), first, second))
        if splits:
            _, first, second = min(splits)
            draw.text((x, y), first, font=font, fill=NAVY)
            draw.text((x, y + 39), second, font=font, fill=NAVY)
            return y + 78
    raise ValueError(f"Headline does not fit in two lines: {text}")


def draw_subline(draw, text, x, y, max_width):
    font_dir = Path(matplotlib.get_data_path()) / "fonts" / "ttf"
    words = text.split()
    for size in range(21, 17, -1):
        font = ImageFont.truetype(str(font_dir / "DejaVuSans.ttf"), size)
        if draw.textbbox((0, 0), text, font=font)[2] <= max_width:
            draw.text((x, y), text, font=font, fill=INK)
            return y + 28
        splits = []
        for split in range(1, len(words)):
            first = " ".join(words[:split])
            second = " ".join(words[split:])
            first_width = draw.textbbox((0, 0), first, font=font)[2]
            second_width = draw.textbbox((0, 0), second, font=font)[2]
            if first_width <= max_width and second_width <= max_width:
                splits.append((abs(first_width - second_width), first, second))
        if splits:
            _, first, second = min(splits)
            draw.text((x, y), first, font=font, fill=INK)
            draw.text((x, y + 28), second, font=font, fill=INK)
            return y + 56
    raise ValueError(f"Sub-line does not fit in two lines: {text}")


def main():
    font_dir = Path(matplotlib.get_data_path()) / "fonts" / "ttf"
    masthead_font = ImageFont.truetype(str(font_dir / "DejaVuSans-Bold.ttf"), 58)
    date_font = ImageFont.truetype(str(font_dir / "DejaVuSans-Bold.ttf"), 29)
    kicker_font = ImageFont.truetype(str(font_dir / "DejaVuSans-Bold.ttf"), 19)
    footer_font = ImageFont.truetype(str(font_dir / "DejaVuSans.ttf"), 15)

    image = Image.new("RGB", (WIDTH, HEIGHT), BACKGROUND)
    draw = ImageDraw.Draw(image)

    masthead = "THE WORLD IN ONE DAY"
    masthead_bounds = draw.textbbox((0, 0), masthead, font=masthead_font)
    draw.text(((WIDTH - (masthead_bounds[2] - masthead_bounds[0])) / 2, 27),
              masthead, font=masthead_font, fill=NAVY)

    band_top, band_bottom = 108, 169
    draw.rectangle((0, band_top, WIDTH, band_bottom), fill=RED)
    date = "FRIDAY 20 NOVEMBER 2026"
    date_bounds = draw.textbbox((0, 0), date, font=date_font)
    draw.text(((WIDTH - (date_bounds[2] - date_bounds[0])) / 2, 122),
              date, font=date_font, fill="white")

    margin_x = 24
    gap_x = 12
    gap_y = 14
    card_width = (WIDTH - 2 * margin_x - gap_x) // 2
    card_height = 239
    first_y = 187

    for index, (kicker, headline, subline, accent) in enumerate(stories):
        column = index % 2
        row = index // 2
        x = margin_x + column * (card_width + gap_x)
        y = first_y + row * (card_height + gap_y)
        draw.rectangle((x, y, x + card_width, y + card_height),
                       outline=BORDER, width=2)
        text_x = x + 10
        text_width = card_width - 20
        text_y = y + 15
        draw.text((text_x, text_y), kicker, font=kicker_font, fill=accent)
        text_y += 35
        text_y = draw_headline(draw, headline, text_x, text_y, text_width)
        text_y += 9
        draw_subline(draw, subline, text_x, text_y, text_width)

    footer = "Six stories that defined the day - compiled from 20 November 2026 reporting"
    footer_bounds = draw.textbbox((0, 0), footer, font=footer_font)
    draw.text(((WIDTH - (footer_bounds[2] - footer_bounds[0])) / 2, 976),
              footer, font=footer_font, fill=MUTED)

    image.save(Path(__file__).with_name("image.png"), format="PNG")


if __name__ == "__main__":
    main()
