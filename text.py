from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import textwrap
import subprocess
import sys
import os
import math


def draw_text(text, font_path, font_size=20, line_spacing=5, text_width=50):
    font = ImageFont.truetype(font_path, font_size)
    total_height = 0
    image_width = 0
    res = []
    zlines = text.split('\n')

    for zline in zlines:
        lines = textwrap.wrap(zline, text_width)

        # Calculate est size of the image
        for line in lines:
            line_width = font.getbbox(line)[2]
            line_height = font.getbbox(line)[3]
            if line_width > image_width:
                image_width = line_width
            total_height += line_height + line_spacing
            res.append(line)

    total_height -= line_spacing - 4

    # create picture
    image = Image.new('1', (image_width, total_height), "white")
    draw = ImageDraw.Draw(image)

    # draw text line by line
    y = 0
    for line in res:
        draw.text((0, y), line, fill="black", font=font)
        y += font.getbbox(line)[3] + line_spacing

    scalar = 384 / image_width
    new_image = image.resize([384, math.floor(total_height * scalar)])
    return new_image


if __name__ == "__main__":
    abspath = os.path.dirname(os.path.abspath(__file__))
    font = os.getenv("cat_font", abspath + "/MatrixSans-Regular.ttf")
    font_size = int(os.getenv("cat_font_size", 20))
    font_spacing = int(os.getenv("cat_font_spacing", -2))
    length = int(os.getenv("cat_length", 60))
    max_versuche = int(os.getenv("cat_max-retries", 5))
    searchtime = int(os.getenv("cat_search", 6))

    input_text = sys.stdin.read()
    image = draw_text(input_text, font, font_size, font_spacing, length)
    img_bytes = BytesIO()
    image.save(img_bytes, format='PPM')
    img_bytes.seek(0)
    data = img_bytes.read()

    tries = 0
    success = False

    print(f"{input_text}\nInitialize printer")
    while tries < max_versuche and not success:
        result = subprocess.run([sys.executable, abspath + "/printer.py", "-s", str(searchtime), "-"], input=data,
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=abspath)
        if result.returncode == 0:
            print(result.stdout.decode())
            success = True
        else:
            print(f"Error on try #{tries + 1} of {max_versuche}: {result.stderr.decode()}")
            tries += 1

    if not success:
        print(f"Print aborted after {tries} retries")
