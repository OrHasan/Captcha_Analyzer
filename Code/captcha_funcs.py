import re
import numpy as np
import cv2
from os import listdir
from os.path import isfile, join
from matplotlib import pyplot as plt


def get_file_index(history_dir):
    history_files = [f for f in listdir(history_dir) if isfile(join(history_dir, f))]
    current_index = 0
    for file_name in history_files:
        current_index = max(current_index, int(re.search(r'#(\d+)', file_name).group(1)))
    current_index += 1

    return current_index


def run_model(client, cleared_captcha_file, client_access_attempts=3):
    for attempt in range(1, client_access_attempts + 1):
        try:
            result = client.predict(cleared_captcha_file, api_name="/predict").upper()
            # break
        except TimeoutError:
            if attempt != client_access_attempts:
                print("API Timeout, try number: " + str(attempt + 1))
            else:
                print("API Timeout, retry limit reached")
                result = ""

        return result


def filter_captcha(img, cleared_captcha_file, use_median=True, use_dilate_erode=True,
                   median_kernel_size=5, dilate_erode_kernel_size=(3, 3), dilate_erode_iterations=1,
                   show_comparison=False):
    if not use_median and not use_dilate_erode:
        print("Both filters can't be FALSE, changing the Median filter to true")
        use_median = True

    if use_median:
        img_median = cv2.medianBlur(img, median_kernel_size)
        clear_img = img_median
    else:
        img_median = None
        clear_img = img

    if use_dilate_erode:
        kernel = np.ones(dilate_erode_kernel_size, np.uint8)
        img_dilation = cv2.dilate(clear_img, kernel, iterations=dilate_erode_iterations)
        img_erosion = cv2.erode(img_dilation, kernel, iterations=dilate_erode_iterations)
        clear_img = img_erosion
    else:
        img_dilation = None
        img_erosion = None

    cv2.imwrite(cleared_captcha_file, clear_img)

    fig = comparison_plot(img, img_median, img_dilation, img_erosion, show_comparison)
    return fig


def comparison_plot(img, img_median, img_dilation, img_erosion, show_comparison=False):
    if img_median is None:
        fig, axs = plt.subplots(nrows=2, ncols=3)

        axs[0, 0].remove()
        axs[0, 2].remove()
        axs[1, 1].remove()

        axs[0, 1].imshow(img)
        axs[0, 1].axis('off')
        axs[0, 1].set_title('Captcha')

        axs[1, 0].imshow(img_dilation)
        axs[1, 0].axis('off')
        axs[1, 0].set_title('Step 1:\nDilation Filter')

        axs[1, 2].imshow(img_erosion)
        axs[1, 2].axis('off')
        axs[1, 2].set_title('Step 2:\nErosion Filter')

    elif img_dilation is None:
        fig, axs = plt.subplots(nrows=2, ncols=1)

        axs[0].imshow(img)
        axs[0].axis('off')
        axs[0].set_title('Captcha')

        axs[1].imshow(img_median)
        axs[1].axis('off')
        axs[1].set_title('Step 1:\nMedian Filter')

    else:
        fig, axs = plt.subplots(nrows=2, ncols=3)

        axs[0, 0].remove()
        axs[0, 2].remove()

        axs[0, 1].imshow(img)
        axs[0, 1].axis('off')
        axs[0, 1].set_title('Captcha')

        axs[1, 0].imshow(img_median)
        axs[1, 0].axis('off')
        axs[1, 0].set_title('Step 1:\nMedian Filter')

        axs[1, 1].imshow(img_dilation)
        axs[1, 1].axis('off')
        axs[1, 1].set_title('Step 2:\nDilation Filter')

        axs[1, 2].imshow(img_erosion)
        axs[1, 2].axis('off')
        axs[1, 2].set_title('Step 3:\nErosion Filter')

    if show_comparison:
        plt.show()

    return fig
