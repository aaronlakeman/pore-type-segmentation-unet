from PIL import Image
from itertools import product
import os
import glob

def make_tiles(dir_in:str, dir_out:str, d:int):
    """tiles all image files in a given folder
    Args:
        dir_in (str): directory with image files
        dir_out (str): output directory
        d (int): tilesize in pixels
    """
    for filename in glob.glob(dir_in + '/*.png'): #assumes a .png file, change if not applicable
        img = Image.open(filename)
        name, ext = os.path.splitext(filename)
        name = name.split('/')[1]
        w, h = img.size
        
        grid = product(range(0, h-h%d, d), range(0, w-w%d, d))
        for i, j in grid:
            box = (j, i, j+d, i+d)
            out = os.path.join(dir_out, f'{name}_{i}_{j}{ext}')
            img.crop(box).save(out)