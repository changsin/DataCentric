import argparse
import glob
import os
import pathlib

import albumentations as A
import cv2
import numpy as np
from PIL import Image

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


# Declare an augmentation pipeline
transformer = A.Compose([
    A.Affine(shear=20, scale=0.5, fit_output=True, mode=cv2.BORDER_REFLECT_101),
    # A.Perspective(scale=0.5, fit_output=True, pad_mode=cv2.BORDER_REFLECT_101),
    # A.RandomCrop(width=100, height=100),
    A.HorizontalFlip(p=0.5),
    # A.RandomBrightnessContrast(p=0.2),
])


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


def augment_image(transformer, in_filename, out_filename):
    # Read an image with OpenCV and convert it to the RGB colorspace
    image = cv2.imread(in_filename)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Augment an image
    transformed = transformer(image=image)
    transformed_image = transformed["image"]
    transformed_image = Image.fromarray(transformed_image, 'RGB')
    transformed_image.save(out_filename)
    # print(text, out_filename, font_file)


def augment_images(in_folder, out_folder):
    for num1, num2 in CLASS_NAMES:
        in_sub_folder = os.path.join(in_folder, num1)
        out_sub_folder = os.path.join(out_folder, num1)
        pathlib.Path(out_sub_folder).mkdir(parents=True, exist_ok=True)
        print(in_sub_folder)

        in_files = glob_files(in_sub_folder, "*")
        for in_file in in_files:
            out_filename = os.path.join(out_sub_folder, os.path.basename(in_file))
            augment_image(transformer, in_file, out_filename)
            print(out_filename)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-in_folder", action="store", dest="in_folder", type=str)
    parser.add_argument("-out_folder", action="store", dest="out_folder", type=str)

    args = parser.parse_args()
    augment_images(args.in_folder, args.out_folder)
