import argparse
import glob
import os
import pathlib

import numpy as np
from PIL import Image, ImageDraw, ImageFont

CLASS_NAMES = np.array([["i", "I"],
               ["ii", "II"],
               ["iii", "III"],
               ["iv", "IV"],
               ["v", "V"],
               ["vi", "VI"],
               ["vii", "VII"],
               ["viii", "VIII"],
               ["ix", "IX"],
               ["x", "X"]])


def glob_files(path, extension='*'):
    search_string = os.path.join(path, extension)
    files = glob.glob(search_string)

    paths = []
    for f in files:
      if os.path.isdir(f):
        sub_paths = glob_files(f + '/')
        paths += sub_paths
      else:
        paths.append(f)

    # We sort the images in alphabetical order to match them
    #  to the annotation files
    paths.sort()

    return paths


def create_text_image(text, out_filename, font_file,
                      start_x=100, start_y=30, font_size=200, w=300, h=300):
    image = Image.new('RGB', (w, h), color=(255, 255, 255))
    font = ImageFont.truetype(font_file, font_size)
    d = ImageDraw.Draw(image)
    d.text((start_x, start_y), text, font=font, fill=(0, 0, 0))
    image.save(out_filename)
    # print(text, out_filename, font_file)


def create_text_images(font_folder, out_folder):
    font_files = glob_files(font_folder, "*.ttc")
    for font_file in font_files:
        for num1, num2 in CLASS_NAMES:
            out_sub_folder = os.path.join(out_folder, num1)
            pathlib.Path(out_sub_folder).mkdir(parents=True, exist_ok=True)

            out_filename = os.path.join(out_sub_folder, num1 + "_1-" + os.path.basename(font_file))
            # print(out_filename)
            create_text_image(num1, out_filename + ".jpg", font_file)

            out_filename = os.path.join(out_sub_folder, num2 + "_2-" + os.path.basename(font_file))
            # print(out_filename)
            create_text_image(num2, out_filename + ".jpg", font_file)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-font_folder", action="store", dest="font_folder", type=str)
    parser.add_argument("-out_folder", action="store", dest="out_folder", type=str)

    args = parser.parse_args()
    create_text_images(args.font_folder, args.out_folder)
