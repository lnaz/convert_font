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

def get_offset(pil_img, normal_canvas_size):
    num_img = pil2num(pil_img)
    canvas_size = len(num_img)
    canvas_offset = canvas_size - normal_canvas_size
    margins = {}
    # top
    for i in range(canvas_size):
        for j in range(canvas_size):
            if num_img[i][j] != 255:
                margins['top'] = i
                break
        if 'top' in margins:
            break
    # bottom
    for i in range(canvas_size):
        for j in range(canvas_size):
            if num_img[canvas_size - i - 1][j] != 255:
                margins['bottom'] = i - canvas_offset
                break
        if 'bottom' in margins:
            break
    # left
    for j in range(canvas_size):
        for i in range(canvas_size):
            if num_img[i][j] != 255:
                margins['left'] = j
                break
        if 'left' in margins:
            break
    # right
    for j in range(canvas_size):
        for i in range(canvas_size):
            if num_img[i][canvas_size - j - 1] != 255:
                margins['right'] = j - canvas_offset
                break
        if 'right' in margins:
            break
    x_offset = int((margins['right'] - margins['left']) / 2)
    y_offset = int((margins['bottom'] - margins['top']) / 2)
    offsets = (x_offset, y_offset)
    # print (margins)

    is_tb_maximum = margins['top'] + margins['bottom'] <= 0
    is_lr_maximum = margins['right'] + margins['left'] <= 0
    is_maximum = is_tb_maximum or is_lr_maximum
    return offsets, is_maximum

def draw_char(char, font_path, canvas_size, char_size, offsets=(0, 0)):
    font = ImageFont.truetype(font_path, size=char_size)
    img = Image.new('L', (canvas_size, canvas_size), 255)
    draw = ImageDraw.Draw(img)
    draw.text(offsets, char, 0, font=font)
    img = convert_binary_img(img)
    return img

def draw_char_center(char, font_path, canvas_size, char_size):
    no_offset_img = draw_char(char, font_path, canvas_size + 20, char_size)
    offsets, is_maximum = get_offset(no_offset_img, canvas_size)
    center_img = draw_char(char, font_path, canvas_size, char_size, offsets)
    return center_img, is_maximum

def draw_char_maximum(char, font_path, canvas_size):
    char_size = canvas_size
    while True:
        img, is_maximum = draw_char_center(char, font_path, canvas_size, char_size)
        if is_maximum:
            break
        char_size += 1
    return img

def ttfotf2png(src_font_path, dst_dir_path, charset, canvas_size):
    for c in CAPS:
        img = draw_char_maximum(c, src_font_path, canvas_size)
        if img:
            img.save(os.path.join(dst_dir_path, c + ".png"))
            print ("proccessed: " + c)

if __name__ == "__main__":
    ttfotf2png("./azukiLP.ttf", "output", CAPS, 100)
