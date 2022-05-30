import os
import splitfolders


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
