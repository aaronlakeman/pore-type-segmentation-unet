import numpy as np


def make_pred(image_patches, mask_patches, model):
    """Transforms masks and images, creates prediction on images, returns a list with patched and transformed true masks and pred masks

    Args:
        image_patches (_list_): list of image patches for prediction (test data)
        mask_patches (_list_): list of mask patches (test data)

    Returns:
        _type_: _description_
    """
    # Make predictions and save predictions
    predicted_patches = []
    patches_mask = []

    pred_patches = []
    true_patches = []

    for i in range(image_patches.shape[0]):
        for j in range(image_patches.shape[1]):

            single_patch = image_patches[i, j, :, :]
            single_mask = mask_patches[i, j, :, :]

            single_patch = single_patch / 255.0

            single_patch = np.expand_dims(np.array(single_patch), axis=2)
            single_mask = np.expand_dims(np.array(single_mask), axis=2)

            single_patch_input = np.expand_dims(single_patch, 0)
            single_mask_input = np.expand_dims(single_mask, 0)

            single_patch_prediction = model.predict(single_patch_input)
            single_patch_predicted_img = np.argmax(single_patch_prediction, axis=3)[
                0, :, :
            ]

            predicted_patches.append(single_patch_predicted_img)
            patches_mask.append(single_mask_input)

            # flatten the predict and the true mask
            pred = single_patch_predicted_img.flatten()
            true = single_mask_input.flatten()

            pred_patches.append(pred)
            true_patches.append(true)

    return predicted_patches, patches_mask, pred_patches, true_patches


def patch_masks(true_patch, baseline_patch):
    # Make predictions and save predictions
    output_true_patches = []
    output_baseline_patches = []

    for i in range(true_patch.shape[0]):
        for j in range(true_patch.shape[1]):

            single_true_patch = true_patch[i, j, :, :]
            single_baseline_patch = baseline_patch[i, j, :, :]

            # flatten the predict and the true mask
            true_flatten = single_true_patch.flatten()
            baseline_flatten = single_baseline_patch.flatten()

            output_true_patches.append(true_flatten)
            output_baseline_patches.append(baseline_flatten)

    return output_true_patches, output_baseline_patches


def single_image_IoU(true_patches, pred_patches):
    """Calculates the class IoU and mean IoU for each image patch of a single larger image and saves them in a list

    Args:
        true_patches (_array_): 2-D array of all true values, includes all 512*512 patches of a single mask
        pred_patches (_array_): 2-D array of all predicted values, includes all 512*512 patches of a single mask
    Returns:
        _lists_: returns four lists containing overall IoU as well as IoU of each class
    """
    # Instantiate lists collecting IoU's / Currently the mask has no unique value
    mean_IoU = []
    class_1_IoU = []
    class_2_IoU = []
    class_3_IoU = []
    class_4_IoU = []

    for i in range(len(pred_patches)):  # Run through all true and predicted patches
        # Get true and predicted mask
        pred = pred_patches[i]
        true = true_patches[i]

        # instantiate true-false classes
        c1_true = 0
        c1_false = 0
        c2_true = 0
        c2_false = 0
        c3_true = 0
        c3_false = 0
        c4_true = 0
        c4_false = 0

        # loop and compare single entries between true and pred
        for k in range(len(pred)):
            # Class 1 (background)
            if true[k] == 0:
                if pred[k] == 0:
                    c1_true += 1
                else:
                    c1_false += 1
            # Class 2 (fractures)
            elif true[k] == 1:
                if pred[k] == 1:
                    c2_true += 1
                else:
                    c2_false += 1
            # Class 3 (pore)
            elif true[k] == 2:
                if pred[k] == 2:
                    c3_true += 1
                else:
                    c3_false += 1
            elif true[k] == 3:
                if pred[k] == 3:
                    c4_true += 1
                else:
                    c4_false += 1

        # append all values within a patch where values are observed
        mean_IoU.append((c1_true + c2_true + c3_true + c4_true) / len(pred))

        if c1_true > 0 or c1_false > 0:
            class_1_IoU.append((c1_true) / (c1_true + c1_false))
        if c2_true > 0 or c2_false > 0:
            class_2_IoU.append((c2_true) / (c2_true + c2_false))
        if c3_true > 0 or c3_false > 0:
            class_3_IoU.append((c3_true) / (c3_true + c3_false))
        if c4_true > 0 or c4_false > 0:
            class_4_IoU.append((c4_true) / (c4_true + c4_false))

    return mean_IoU, class_1_IoU, class_2_IoU, class_3_IoU, class_4_IoU


def map_func(val, dictionary):
    return dictionary[val] if val in dictionary else val
