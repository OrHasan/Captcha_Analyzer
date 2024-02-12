import numpy as np
import cv2
# - - - - - - - - - - - - - - -
from lib import general_funcs


def run_model(config, client_config):
    for attempt in range(1, client_config['client_access_attempts'] + 1):
        try:
            result = client_config['client'].predict(config.general()['cleared_captcha_file'],
                                                     api_name="/predict").upper()
            # break
        except TimeoutError:
            if attempt != client_config['client_access_attempts']:
                continue
                # (terminal prints will collide with the progress bar)
                # print("API Timeout, try number: " + str(attempt + 1))
            else:
                print("API Timeout, retry limit reached")
                result = ""

        return result


def filter_captcha(img, config, use_median=True, use_dilate_erode=True):
    filter_config = config.filter()

    if not use_median and not use_dilate_erode:
        print("Both filters can't be FALSE, changing the Median filter to true")
        use_median = True

    if use_median:
        img_median = cv2.medianBlur(img, filter_config['median_kernel_size'])
        clear_img = img_median
    else:
        img_median = None
        clear_img = img

    if use_dilate_erode:
        kernel = np.ones(filter_config['dilate_erode_kernel_size'], np.uint8)
        img_dilation = cv2.dilate(clear_img, kernel, iterations=filter_config['dilate_erode_iterations'])
        img_erosion = cv2.erode(img_dilation, kernel, iterations=filter_config['dilate_erode_iterations'])
        clear_img = img_erosion
    else:
        img_dilation = None
        img_erosion = None

    cv2.imwrite(config.general()['cleared_captcha_file'], clear_img)

    fig = general_funcs.comparison_plot(config, img, img_median, img_dilation, img_erosion)
    return fig
