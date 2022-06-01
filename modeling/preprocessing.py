import os
import splitfolders
import shutil
import cv2
import patchify


def folder_structure(target_dir="../data/"):
    """Generates folder structure

    Args:
        target_dir (str, optional): The data directory path relative to the directory you run this function from. Defaults to '../data/'.
    """

    dir_lst = ["data_original", "data_temp"]
    subdir_lst = ["images/", "masks/"]
    parent_dir = os.getcwd()

    # make main directories
    for dir in dir_lst:
        for subdir in subdir_lst:
            os.makedirs(
                os.path.join(parent_dir, target_dir, dir, subdir), exist_ok=True
            )
    return


def create_tiles(
    size=512,
    step=512,
    source_dir="../data/data_original/",
    target_dir="../data/data_temp/",
):
    """Creates smaller patches of `size` from large images in `source_dir` and copies them to `target dir`.

    Args:
        size (int, optional): Size of the patches in pixels. Defaults to 512. Make sure the original image dimension are multiples of this size.
        source_dir (str, optional): Directory where the large images are stored. Defaults to '../data/data_original/'.
        target_dir (str, optional): Directory . Defaults to '../data/data_temp/'.
    """
    image_dir = source_dir + "images/"
    img_target_dir = target_dir + "images/"
    img_counter = 1

    for file in os.listdir(image_dir):
        if file.endswith(".tif"):
            print("chopping up " + file)
            large_image = cv2.imread(image_dir + "/" + file, 0)
            patches = patchify(large_image, (size, size), step=step)
            for i in range(patches.shape[0]):
                for j in range(patches.shape[1]):
                    single_patch_img = patches[i, j]
                    if not cv2.imwrite(
                        img_target_dir
                        + "image_"
                        + str(img_counter)
                        + "_"
                        + str(i)
                        + "_"
                        + str(j)
                        + ".tif",
                        single_patch_img,
                    ):
                        raise Exception("Could not write the image")
            img_counter += 1

    mask_dir = source_dir + "masks/"
    msk_target_dir = target_dir + "masks/"
    msk_counter = 1

    for file in os.listdir(mask_dir):
        if file.endswith(".tif"):
            print("chopping up " + file)
            large_image = cv2.imread(mask_dir + "/" + file, 0)
            patches = patchify(large_image, (size, size), step=step)
            for i in range(patches.shape[0]):
                for j in range(patches.shape[1]):
                    single_patch_img = patches[i, j]
                    if not cv2.imwrite(
                        msk_target_dir
                        + "mask_"
                        + str(msk_counter)
                        + "_"
                        + str(i)
                        + "_"
                        + str(j)
                        + ".tif",
                        single_patch_img,
                    ):
                        raise Exception("Could not write the image")
            msk_counter += 1
    print("Done")
    return


def split_folders(
    input_dir="../data/data_temp/",
    output_dir="../data/data_train/",
    ratio=(0.7, 0.2, 0.1),
    seed=42,
):
    """Splits available data according to a given ratio and copies it to a specified folder.

    Args:
        input_dir (str, optional): Path to directory containing the image tiles. Defaults to '../data/data_temp'.
        output_dir (str, optional): Path to the training directory. Defaults to '..data/data_train'.
        ratio (tuple, optional): Train/validation/test split ratio. Defaults to (0.7,0.2,0.1).
        seed (int, optional): Random seed. Defaults to 42.
    """
    # Create training folder
    cwd_dir = os.getcwd()
    os.makedirs(os.path.join(cwd_dir, output_dir), exist_ok=True)

    # Split the data into train,val,test parts and move them to the training folder
    splitfolders.ratio(
        input_dir,
        output=output_dir,
        seed=seed,
        ratio=ratio,
        group_prefix=None,
        move=True,
    )
    print(f"Done splitting with a train/val/test ratio of {ratio}")

    # This part moves the images to a subfolder because we are doing multiclass segmentation and keras' datagenerator flow_from_directory expects at least one folder
    dir_lst = ["train/", "val/", "test/"]
    dir_lst2 = ["images/", "masks/"]

    for dir in dir_lst:
        for dir2 in dir_lst2:
            os.makedirs(os.path.join(output_dir + dir + dir2 + dir), exist_ok=True)
            for file_name in os.listdir(os.path.join(output_dir + dir + dir2)):
                # file paths
                source = output_dir + dir + dir2 + file_name
                destination = output_dir + dir + dir2 + dir + file_name
                # move bitch!
                if os.path.isfile(source):
                    shutil.move(source, destination)
    return
