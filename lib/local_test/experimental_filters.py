import cv2
import numpy as np


def sharp_img(img):
    sharp_kernel = np.array([[0, -1, 0],
                             [-1, 5, -1],
                             [0, -1, 0]])
    sharp_img = cv2.filter2D(img, -1, sharp_kernel)

    return sharp_img


def detect_edges(img, method="square"):
    match method:
        case "square":
            edges_kernel = np.array([[-1, -1, -1],
                                     [-1, 8, -1],
                                     [-1, -1, -1]])
        case "plus":
            edges_kernel = np.array([[0, -1, 0],
                                     [-1, 4, -1],
                                     [0, -1, 0]])
        case _:
            print("\n\033[43m {}\033[00m".format('WARNING'),
                  "\033[33m {}\033[00m".format("UN-EXISTING METHOD was inserted into the Edge Detection function !"))
            return img

    img_with_edges = cv2.filter2D(img, -1, edges_kernel)
    return img_with_edges


def resize_img(img, scale_percent=None, dimensions=None):
    if scale_percent:
        width = int(img.shape[1] * scale_percent / 100)
        height = int(img.shape[0] * scale_percent / 100)

    elif dimensions:
        width = dimensions[0]
        height = dimensions[1]

    else:
        print("\n\033[43m {}\033[00m".format('WARNING'),
              "\033[33m {}\033[00m".format("Please provide either Scale-Percent or image Dimensions"
                                           "into the Image Resizing function !"))
        return img

    dim = (width, height)
    resized_img = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)

    return resized_img


def remove_noise_colors(img, img_temp):
    lower = np.array([0, 0, 0])
    upper = np.array([70, 100, 95])
    mask = cv2.inRange(img, lower, upper)
    img_temp[mask > 0] = [255, 255, 255]

    lower = np.array([0, 0, 100])
    upper = np.array([30, 15, 125])
    mask = cv2.inRange(img, lower, upper)
    img_temp[mask > 0] = [255, 255, 255]

    lower = np.array([70, 100, 100])
    upper = np.array([70, 100, 130])
    mask = cv2.inRange(img, lower, upper)
    img_temp[mask > 0] = [255, 255, 255]

    lower = np.array([40, 0, 130])
    upper = np.array([110, 50, 170])
    mask = cv2.inRange(img, lower, upper)
    img_temp[mask > 0] = [255, 255, 255]

    lower = np.array([0, 130, 0])
    upper = np.array([40, 160, 50])
    mask = cv2.inRange(img, lower, upper)
    img_temp[mask > 0] = [255, 255, 255]

    lower = np.array([40, 100, 120])
    upper = np.array([110, 140, 150])
    mask = cv2.inRange(img, lower, upper)
    img_temp[mask > 0] = [255, 255, 255]

    lower = np.array([100, 120, 30])
    upper = np.array([160, 170, 80])
    mask = cv2.inRange(img, lower, upper)
    img_temp[mask > 0] = [255, 255, 255]

    lower = np.array([120, 30, 60])
    upper = np.array([150, 60, 100])
    mask = cv2.inRange(img, lower, upper)
    img_temp[mask > 0] = [255, 255, 255]

    lower = np.array([80, 20, 30])
    upper = np.array([100, 40, 50])
    mask = cv2.inRange(img, lower, upper)
    img_temp[mask > 0] = [255, 255, 255]

    lower = np.array([100, 80, 30])
    upper = np.array([150, 120, 60])
    mask = cv2.inRange(img, lower, upper)
    img_temp[mask > 0] = [255, 255, 255]

    lower = np.array([0, 100, 0])
    upper = np.array([20, 130, 40])
    mask = cv2.inRange(img, lower, upper)
    img_temp[mask > 0] = [255, 255, 255]

    lower = np.array([80, 50, 0])
    upper = np.array([120, 80, 20])
    mask = cv2.inRange(img, lower, upper)
    img_temp[mask > 0] = [255, 255, 255]

    lower = np.array([60, 60, 10])
    upper = np.array([100, 100, 60])
    mask = cv2.inRange(img, lower, upper)
    img_temp[mask > 0] = [255, 255, 255]

    lower = np.array([80, 0, 20])
    upper = np.array([115, 30, 60])
    mask = cv2.inRange(img, lower, upper)
    img_temp[mask > 0] = [255, 255, 255]

    lower = np.array([140, 60, 0])
    upper = np.array([170, 100, 30])
    mask = cv2.inRange(img, lower, upper)
    img_temp[mask > 0] = [255, 255, 255]

    lower = np.array([90, 0, 50])
    upper = np.array([120, 15, 80])
    mask = cv2.inRange(img, lower, upper)
    img_temp[mask > 0] = [255, 255, 255]

    lower = np.array([145, 0, 10])
    upper = np.array([170, 15, 50])
    mask = cv2.inRange(img, lower, upper)
    img_temp[mask > 0] = [255, 255, 255]

    lower = np.array([50, 100, 0])
    upper = np.array([80, 130, 40])
    mask = cv2.inRange(img, lower, upper)
    img_temp[mask > 0] = [255, 255, 255]

    lower = np.array([90, 20, 30])
    upper = np.array([120, 60, 60])
    mask = cv2.inRange(img, lower, upper)
    img_temp[mask > 0] = [255, 255, 255]

    lower = np.array([105, 100, 110])
    upper = np.array([140, 130, 140])
    mask = cv2.inRange(img, lower, upper)
    img_temp[mask > 0] = [255, 255, 255]

    lower = np.array([25, 90, 50])
    upper = np.array([60, 120, 80])
    mask = cv2.inRange(img, lower, upper)
    img_temp[mask > 0] = [255, 255, 255]

    return img_temp


def show_letters_color_only(img):
    lower = np.array([100, 170, 240])
    upper = np.array([115, 185, 255])
    mask = cv2.inRange(img, lower, upper)
    res1 = cv2.bitwise_and(img, img, mask=mask)

    lower = np.array([110, 235, 140])
    upper = np.array([125, 250, 155])
    mask = cv2.inRange(img, lower, upper)
    res2 = cv2.bitwise_and(img, img, mask=mask)

    lower = np.array([90, 80, 105])
    upper = np.array([110, 95, 120])
    mask = cv2.inRange(img, lower, upper)
    res3 = cv2.bitwise_and(img, img, mask=mask)

    lower = np.array([190, 215, 125])
    upper = np.array([205, 230, 140])
    mask = cv2.inRange(img, lower, upper)
    res4 = cv2.bitwise_and(img, img, mask=mask)

    temp_res = cv2.bitwise_or(res1, res2)
    temp_res = cv2.bitwise_or(temp_res, res3)
    final_res = cv2.bitwise_or(temp_res, res4)

    return final_res
