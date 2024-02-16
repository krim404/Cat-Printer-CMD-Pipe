from PIL import Image, ImageDraw, ImageFont
import textwrap
import subprocess
import sys
import os
import math

def draw_text(text, font_path, font_size=20, line_spacing=5, text_width=50):
    font = ImageFont.truetype(font_path, font_size)
    total_height = 0
    image_width = 0
    ergebnis = []
    zeilen = text.split('\n')

    for zeile in zeilen:
        lines = textwrap.wrap(zeile, text_width)

        # Calculate est size of the image
        for line in lines:
            line_width = font.getbbox(line)[2]
            line_height = font.getbbox(line)[3]
            if line_width > image_width:
                image_width = line_width
            total_height += line_height + line_spacing
            ergebnis.append(line)

    total_height -= line_spacing - 4

    # create picture
    image = Image.new('1', (image_width, total_height), "white")
    draw = ImageDraw.Draw(image)

    # draw text line by line
    y = 0
    for line in ergebnis:
        draw.text((0, y), line, fill="black", font=font)
        y += font.getbbox(line)[3] + line_spacing

    scalar = 384 / image_width
    new_image = image.resize([384, math.floor(total_height * scalar)])
    return new_image

if __name__ == "__main__":
    absoluter_pfad = os.path.dirname(os.path.abspath(__file__))
    font = os.getenv("cat_font", absoluter_pfad + "/MatrixSans-Regular.ttf")
    font_size = os.getenv("cat_font_size", 20)
    font_spacing = os.getenv("cat_font_spacing", -2)
    length = os.getenv("cat_length", 60)
    searchtime = os.getenv("cat_search", 6)
    tempfile = os.getenv("cat_tempfile", absoluter_pfad + "/temp.pbm")

    input_text = sys.stdin.read()
    image = draw_text(input_text, font, font_size, font_spacing, length)
    image.save(tempfile)
    result = subprocess.run([sys.executable, absoluter_pfad + "/printer.py", "-s", searchtime, tempfile], capture_output=True, text=True, cwd=absoluter_pfad)
    print(result.stdout)
    print(result.stderr)
    if os.path.exists(tempfile):
        os.remove(tempfile)