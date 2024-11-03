import cv2
import numpy as np


def median_filter(img, config=None, kernel_size=None):
    if config:
        kernel_size = config.filter()['median_kernel_size']
    elif not config and not kernel_size:
        print("\n\033[43m {}\033[00m".format('WARNING'),
              "\033[33m {}\033[00m".format('The Median filter is MISSING INPUT DATA.'),
              "\nPlease make sure to send the config variable or the Kernel Size manually")
        return img

    img_median = cv2.medianBlur(img, kernel_size)
    return img_median


def dilate_erode_filter(img, method="dilation & erosion", config=None, dilate_kernel_size=None, erode_kernel_size=None,
                        dilate_iterations=0, erode_iterations=0):
    if config:
        filter_config = config.filter()

        if not dilate_kernel_size:
            dilate_kernel_size = filter_config['dilate_kernel_size']
        if not erode_kernel_size:
            erode_kernel_size = filter_config['erode_kernel_size']
        if not dilate_iterations:
            dilate_iterations = filter_config['dilate_iterations']
        if not erode_iterations:
            erode_iterations = filter_config['erode_iterations']

    elif not dilate_kernel_size or not erode_kernel_size or not dilate_iterations or not erode_iterations:
        print("\n\033[43m {}\033[00m".format('WARNING'),
              "\033[33m {}\033[00m".format('The Dilate & Erode filter is MISSING INPUT DATA.'),
              "\nPlease make sure to send the config variable or/and all the other variables manually")
        return img

    dilate_kernel = np.ones(dilate_kernel_size, np.uint8)
    erode_kernel = np.ones(erode_kernel_size, np.uint8)
    match method:
        case "dilation & erosion":
            img_dilation = cv2.dilate(img, dilate_kernel, iterations=dilate_iterations)
            img_erosion = cv2.erode(img_dilation, erode_kernel, iterations=erode_iterations)
            filtered_img = img_erosion

        case "erosion & dilation":
            img_erosion = cv2.erode(img, erode_kernel, iterations=erode_iterations)
            img_dilation = cv2.dilate(img_erosion, dilate_kernel, iterations=dilate_iterations)
            filtered_img = img_dilation

        case "erosion":
            img_erosion = cv2.erode(img, erode_kernel, iterations=erode_iterations)
            img_dilation = None
            filtered_img = img_erosion

        case "dilation":
            img_dilation = cv2.dilate(img, dilate_kernel, iterations=dilate_iterations)
            img_erosion = None
            filtered_img = img_dilation

        case _:
            print("\n\033[43m {}\033[00m".format('WARNING'),
                  "\033[33m {}\033[00m".format("UN-EXISTING METHOD was inserted into the Dilate & Erode function !"))
            return img

    return filtered_img, img_dilation, img_erosion


def remove_additional_pixels(img, filtered_img):
    gray_levels_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    bw_img_2d = cv2.threshold(gray_levels_img, 254, 255, cv2.THRESH_BINARY)[1]
    bw_img_3d = np.expand_dims(bw_img_2d, axis=2)
    mask = (255 - bw_img_3d)
    clear_img = 255 - (filtered_img * mask)

    return clear_img, mask
