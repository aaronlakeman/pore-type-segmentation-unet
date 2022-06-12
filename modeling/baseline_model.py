import cv2
import numpy as np


def baseline_model(corr_masks, uncorrected_masks, img_list, msk_list):
    """Calculates the accuracy based on the pixel-vice difference between images

    Args:
        corr_masks (_type_): _description_
        uncorrected_masks (_type_): _description_
        img_list (_type_): _description_
        msk_list (_type_): _description_
    """
    list = []
    for i in range(len(img_list)):
        img_1 = cv2.imread(corr_masks + img_list[i], 1)
        img_2 = cv2.imread(uncorrected_masks + msk_list[i], 1)

        res = cv2.absdiff(img_1, img_2)
        res = res.astype(np.uint8)
        percentage = np.round(100 - ((np.count_nonzero(res) * 100) / res.size), 2)
        list.append(percentage)
    print(f"The mean accuracy is equal to {round(np.mean(list), 2)}")
    print(f"These are the accuracies of the individual images{list}")
