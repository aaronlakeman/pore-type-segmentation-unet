import os
import splitfolders
import cv2
import patchify


def folder_structure(target_dir="../data/"):
    """Generates folder structure

    Args:
        target_dir (str, optional): The data directory path relative to the directory you run this function from. Defaults to '../data/'.
    """

    dir_lst = ["data_original", "data_temp", "data_train"]
    subdir_lst = ["_images/", "_masks/"]
    parent_dir = os.getcwd()

    # make main directories
    for dir in dir_lst:
        os.makedirs(os.path.join(parent_dir, target_dir, dir), exist_ok=True)

    # make subdirectories
    for i in ["train", "val", "test"]:
        for subdir in subdir_lst:
            os.makedirs(
                os.path.join(parent_dir, target_dir + dir_lst[2], i + subdir + i),
                exist_ok=True,
            )
    return


def split_folders(
    input_dir="../data/data_temp",
    output_dir="..data/data_train",
    ratio=(0.8, 0.2),
    seed=42,
):
    """Splits available data according to a given ratio and copies it to a specified folder.

    Args:
        input_dir (str, optional): Path to directory containing the image tiles. Defaults to '../data/data_temp'.
        output_dir (str, optional): Path to the training directory. Defaults to '..data/data_train'.
        ratio (tuple, optional): Train/validation/test split ratio. Defaults to (0.8,0.2).
        seed (int, optional): Random seed. Defaults to 42.
    """

    splitfolders.ratio(
        input_dir, output=output_dir, seed=seed, ratio=ratio, group_prefix=None
    )
    return


def create_tiles(
    size=512,
    step=512,
    source_dir="../data/data_original/",
    target_dir="../data/data_temp/",
):
    """_summary_

    Args:
        size (int, optional): Size of the patches in pixels. Defaults to 512. Make sure the original image dimension are multiples of this size.
        source_dir (str, optional): Directory where the large images are stored. Defaults to '../data/data_original/'.
        target_dir (str, optional): Directory . Defaults to '../data/data_temp/'.
    """
    # Create image tiles
    working_dir = os.getcwd()
    print(working_dir)
    counter = 1

    for root, dirs, files in os.walk(source_dir):
        for filename in files:
            if filename.endswith(".tif"):
                print(root)
                print(filename)
                large_image = cv2.imread(root + "/" + filename, 0)
                patches = patchify(large_image, (size, size), step=step)
                for i in range(patches.shape[0]):
                    for j in range(patches.shape[1]):
                        single_patch_img = patches[i, j]
                        if not cv2.imwrite(
                            target_dir
                            + "image_"
                            + str(counter)
                            + "_"
                            + str(i)
                            + "_"
                            + str(j)
                            + ".tif",
                            single_patch_img,
                        ):
                            raise Exception("Could not write the image")
                counter += 1
    return


def split_folders(
    input_dir="../data/data_temp",
    output_dir="..data/data_train",
    ratio=(0.8, 0.2),
    seed=42,
):
    """Splits available data according to a given ratio and copies it to a specified folder.

    Args:
        input_dir (str, optional): Path to directory containing the image tiles. Defaults to '../data/data_temp'.
        output_dir (str, optional): Path to the training directory. Defaults to '..data/data_train'.
        ratio (tuple, optional): Train/validation/test split ratio. Defaults to (0.8,0.2).
        seed (int, optional): Random seed. Defaults to 42.
    """
    splitfolders.ratio(
        input_dir, output=output_dir, seed=seed, ratio=ratio, group_prefix=None
    )
    return
