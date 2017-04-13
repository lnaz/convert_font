import os
import argparse
import numpy as np
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

CAPS = [chr(i) for i in range(65, 65 + 26)]

def draw_char(char, font, canvas_size):
    img = Image.new("RGB", (canvas_size, canvas_size), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    draw.text((0, 0), char, (0, 0, 0), font=font)
    return img

def ttfotf2png(src_font, dst_dir, charset, char_size, canvas_size):
    src_font = ImageFont.truetype(src_font, size=char_size)

    for c in CAPS:
        img = draw_char(c, src_font, canvas_size)
        if img:
            img.save(os.path.join(dst_dir, c + ".png"))
            print ("proccessed: " + c)

if __name__ == "__main__":
    ttfotf2png("./azukiLP.ttf", "output", CAPS, 30, 100)
