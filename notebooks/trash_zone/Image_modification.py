from PIL import Image
from itertools import product
import os
import glob
import cv2


def make_tiles(dir_in: str, dir_out: str, d: int):
    """tiles all image files in a given folder
    Args:
        dir_in (str): directory with image files
        dir_out (str): output directory
        d (int): tilesize in pixels
    """
    for filename in glob.glob(dir_in + "/*.tif"):
        img = cv2.imread(filename)
        name, ext = os.path.splitext(filename)
        name = name.split("/")[1]
        w, h = img.size
        grid = product(range(0, h - h % d, d), range(0, w - w % d, d))

        for i, j in grid:
            box = (j, i, j + d, i + d)
            cropped = img.crop(box)
            output = os.path.join(dir_out, f"{name}_{i}_{j}{ext}")
            cv2.imwrite(output, cropped)


def rotation(dir_in: str, dir_out: str, ang: list):
    """rotates images

    Args:
        dir_in (str): directory of images files
        dir_out (str): output directory
        ang (list): list of all angles of rotation
    """
    for filename in glob.glob(
        dir_in + "/*.tif"
    ):  # assumes a .png file, change if not applicable
        img = cv2.imread(filename)
        name, ext = os.path.splitext(filename)
        name = name.split("/")[1]

        h, w = img.shape[:2]
        center = (w / 2, h / 2)

        for i in ang:
            angle = i
            scale = 1

            M = cv2.getRotationMatrix2D(center, angle, scale)
            rotated = cv2.warpAffine(img, M, (w, h))

            output = os.path.join(dir_out, f"{name}_{angle}{ext}")
            cv2.imwrite(output, rotated)


def flip(dir_in: str, dir_out: str, d: int):
    """tiles all image files in a given folder
    Args:
        dir_in (str): directory with image files
        dir_out (str): output directory
        d (int): axis of flip || 0 = vertical axis || 1 = horizontal axis || -1 = both axis
    """
    for filename in glob.glob(
        dir_in + "/*.tif"
    ):  # assumes a .png file, change if not applicable
        img = cv2.imread(filename)
        name, ext = os.path.splitext(filename)
        name = name.split("/")[1]

        img = cv2.flip(img, d)
        output = os.path.join(dir_out, f"{name}_{d}{ext}")
        cv2.imwrite(output, img)
