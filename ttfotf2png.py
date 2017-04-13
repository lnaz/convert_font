import os
import argparse
import numpy as np
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

CAPS = [chr(i) for i in range(65, 65 + 26)]

def convert_binary_img(pil_img, threshold=128):
    num_img = np.asarray(pil_img)
    num_img.flags.writeable = True
    for row_i in range(len(num_img)):
        for col_i in range(len(num_img[0])):
            if num_img[row_i][col_i] < threshold:
                num_img[row_i][col_i] = 0
            else:
                num_img[row_i][col_i] = 255
    binary_img = Image.fromarray(np.uint8(num_img))
    return binary_img

def draw_char(char, font, canvas_size):
    img = Image.new('L', (canvas_size, canvas_size), 255)
    draw = ImageDraw.Draw(img)
    draw.text((0, 0), char, 0, font=font)
    img = convert_binary_img(img)
    return img

def ttfotf2png(src_font, dst_dir, charset, char_size, canvas_size):
    src_font = ImageFont.truetype(src_font, size=char_size)

    for c in CAPS:
        img = draw_char(c, src_font, canvas_size)
        img.point(lambda x: x * 0.5)
        if img:
            img.save(os.path.join(dst_dir, c + ".png"))
            print ("proccessed: " + c)

if __name__ == "__main__":
    ttfotf2png("./azukiLP.ttf", "output", CAPS, 100, 100)
