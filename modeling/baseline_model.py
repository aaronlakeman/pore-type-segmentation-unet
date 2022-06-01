import glob
import cv2
import numpy as np


def baseline_model(corr_masks, uncorrected_masks):
    list = []
    for correct in glob.glob(corr_masks + "*.tif"):
        for uncorrect in glob.glob(uncorrected_masks + "*.tif"):
            img_1 = cv2.imread(correct, 1)
            img_2 = cv2.imread(uncorrect, 1)

            res = cv2.absdiff(img_1, img_2)
            res = res.astype(np.uint8)
            percentage = np.round(100 - ((np.count_nonzero(res) * 100) / res.size), 2)
            list.append(percentage)
            print(f"The mean accuracy is equal to {np.mean(list)}")
            print(f"These are the accuracies of the individual images{list}")
