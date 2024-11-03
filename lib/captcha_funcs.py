import cv2
from gradio_client import handle_file
# - - - - - - - - - - - - - - -
from lib import image_filters, process_plot


def run_model(config, client_config):
    for attempt in range(1, client_config['client_access_attempts'] + 1):
        try:
            result = client_config['client'].predict(handle_file(config.general()['cleared_captcha_file']),
                                                     api_name="/predict")
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


def filter_captcha(img, config, use_median=True, use_median_mask=True, use_dilate_erode=True):
    if not use_median and not use_dilate_erode:
        print("Both filters can't be FALSE, changing the Median filter to true")
        use_median = True

    if use_median:
        img_median = image_filters.median_filter(img, config)
        if use_median_mask:
            img_median, _ = image_filters.remove_additional_pixels(img, img_median)
        clear_img = img_median
    else:
        img_median = None
        clear_img = img

    if use_dilate_erode:
        clear_img, img_dilation, img_erosion =\
            image_filters.dilate_erode_filter(clear_img, "dilation & erosion", config)
    else:
        img_dilation = None
        img_erosion = None

    cv2.imwrite(config.general()['cleared_captcha_file'], clear_img)

    fig = process_plot.comparison_plot(config, img, img_median, img_dilation, img_erosion)
    return fig


def remove_numbers_and_fix_small_letters(result, config):
    general_config = config.general()
    letters_result = ""

    for char in result:
        if general_config['fix_similar_small_letters']:
            match char:
                case "e":   # C / O
                    letters_result += "C"
                    continue
                case "l":
                    letters_result += "I"
                    continue

        if general_config['letters_only']:
            match char:
                case "0":   # O / D / U
                    letters_result += "O"
                case "1":   # I / X / T
                    letters_result += "I"
                case "2":
                    letters_result += "Z"
                case "3":
                    letters_result += "B"
                case "4":   # A / R
                    letters_result += "A"
                case "5":
                    letters_result += "S"
                case "6":   # B / E / O / D (/G)
                    letters_result += "E"
                case "7":   # I / X / T
                    letters_result += "X"
                case "8":   # B / C
                    letters_result += "B"
                case "9":
                    letters_result += "O"
                case _:
                    letters_result += char

    result_changed = result != letters_result
    return letters_result, result_changed
