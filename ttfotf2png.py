import os
import argparse
import numpy as np
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

CAPS = [chr(i) for i in range(65, 65 + 26)]

def pil2num(pil_img):
    num_img = np.asarray(pil_img)
    num_img.flags.writeable = True
    return num_img

def num2pil(num_img):
    pil_img = Image.fromarray(np.uint8(num_img))
    return pil_img

def convert_binary_img(pil_img, threshold=128):
    num_img = pil2num(pil_img)
    for row_i in range(len(num_img)):
        for col_i in range(len(num_img[0])):
            if num_img[row_i][col_i] < threshold:
                num_img[row_i][col_i] = 0
            else:
                num_img[row_i][col_i] = 255
    binary_img = num2pil(num_img)
    return binary_img

def get_offset(pil_img):
    num_img = pil2num(pil_img)
    canvas_size = len(num_img)
    margins = {'top':-1, 'right':-1, 'bottom':-1, 'left':-1}
    # top
    for i in range(canvas_size):
        for j in range(canvas_size):
            if num_img[i][j] != 255:
                margins['top'] = i
                break
        if margins['top'] != -1:
            break
    # bottom
    for i in range(canvas_size):
        for j in range(canvas_size):
            if num_img[canvas_size - i - 1][j] != 255:
                margins['bottom'] = i
                break
        if margins['bottom'] != -1:
            break
    # left
    for j in range(canvas_size):
        for i in range(canvas_size):
            if num_img[i][j] != 255:
                margins['left'] = j
                break
        if margins['left'] != -1:
            break
    # right
    for j in range(canvas_size):
        for i in range(canvas_size):
            if num_img[i][canvas_size - j - 1] != 255:
                margins['right'] = j
                break
        if margins['right'] != -1:
            break
    x_offset = int((margins['right'] - margins['left']) / 2)
    y_offset = int((margins['bottom'] - margins['top']) / 2)
    return x_offset, y_offset

def draw_char(char, font, canvas_size, x_offset=0, y_offset=0):
    img = Image.new('L', (canvas_size, canvas_size), 255)
    draw = ImageDraw.Draw(img)
    draw.text((x_offset, y_offset), char, 0, font=font)
    img = convert_binary_img(img)
    return img

def draw_char_center(char, font, canvas_size):
    no_offset_img = draw_char(char, font, canvas_size)
    x_offset, y_offset = get_offset(no_offset_img)
    center_img = draw_char(char, font, canvas_size, x_offset, y_offset)
    return center_img

def ttfotf2png(src_font, dst_dir, charset, char_size, canvas_size):
    src_font = ImageFont.truetype(src_font, size=char_size)

    for c in CAPS:
        img = draw_char_center(c, src_font, canvas_size)
        img.point(lambda x: x * 0.5)
        if img:
            img.save(os.path.join(dst_dir, c + ".png"))
            print ("proccessed: " + c)

if __name__ == "__main__":
    ttfotf2png("./azukiLP.ttf", "output", CAPS, 100, 100)
