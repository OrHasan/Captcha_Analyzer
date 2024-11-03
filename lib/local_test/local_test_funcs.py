import cv2
from matplotlib import pyplot
# - - - - - - - - - - - - - - -
from lib import general_funcs, captcha_funcs, image_filters, process_plot
from lib.local_test import experimental_filters as exp_filters


def analyze_captcha(img, config, client_config, use_median, use_median_mask, use_dilate_erode, captcha, filter_dir):
    fig = captcha_funcs.filter_captcha(img, config, use_median, use_median_mask, use_dilate_erode)
    result = captcha_funcs.run_model(config, client_config)
    quality_string, extra_chars = detection_quality(captcha, result)
    current_index = general_funcs.get_file_index(filter_dir)
    captcha_file = filter_dir + "/Captcha #" + str(current_index) + "- '" + result + "' (" + quality_string
    if extra_chars:
        captcha_file += ", " + extra_chars

    fig.savefig(captcha_file + ").png", bbox_inches='tight')
    pyplot.close()


def detection_quality(real_text, result_text, capitals_only=True):
    if capitals_only:
        result_text = result_text.upper()

    count = 0
    for real_char, result_char in zip(real_text, result_text):
        if real_char == result_char:
            count += 1
    quality = f"{count} of {len(real_text)} chars"

    # matcher = SequenceMatcher(None, real_text, result_text)
    # matching_blocks = matcher.get_matching_blocks()
    # count = sum(block.size for block in matching_blocks if block.a == block.b)
    # quality = str(count) + " of " + str(len(real_text)) + " chars"

    if len(result_text) > len(real_text):
        extra_chars = str(len(result_text) - len(real_text)) + " extra chars"
    else:
        extra_chars = ""

    return quality, extra_chars


def multi_step_filtering(img, config, client_config, captcha, filter_dirs, methods, pbar, bar_max):
    general_config = config.general()

    # Median -> img Mask -> Median -> img Mask -> Enlarge pic -> Dilation:
    pbar.set_postfix_str("Tested Method: " + general_funcs.my_progress(bar_max - 2, bar_max) + f" ({methods[0]})")

    img_median = image_filters.median_filter(img, config)

    masked_img_median, mask = image_filters.remove_additional_pixels(img, img_median)
    # masked_img_median = 255 - masked_img_median

    masked_img_median2 = image_filters.median_filter(masked_img_median, config)
    masked2_img_median2 = 255 - (masked_img_median2 * mask)

    # clear_clear_img_median_big = exp_filters.resize_img(255 - masked2_img_median2, 300)
    masked2_img_median2_big = exp_filters.resize_img(masked2_img_median2, 300)

    _, img_dilation, img_erosion = image_filters.dilate_erode_filter(masked2_img_median2_big, config=config,
                                                                     dilate_kernel_size=(4, 4),
                                                                     erode_kernel_size=(4, 4))
    cv2.imwrite(general_config['cleared_captcha_file'], img_dilation)
    five_steps = [img_median, masked_img_median,
                  masked_img_median2, masked2_img_median2,
                  img_dilation]
    fig = process_plot.comparison_plot(config, img, multi_step=five_steps)

    result = captcha_funcs.run_model(config, client_config)
    quality_string, extra_chars = detection_quality(captcha, result)
    current_index = general_funcs.get_file_index(filter_dirs[0])
    captcha_file = filter_dirs[0] + "/Captcha #" + str(current_index) + " - '" + result + "' (" + quality_string
    if extra_chars:
        captcha_file += ", " + extra_chars
    fig.savefig(captcha_file + ").png", bbox_inches='tight')

    # Median -> img Mask -> Median -> img Mask -> Enlarge pic -> Dilation -> Erosion:
    pbar.set_postfix_str("Tested Method: " + general_funcs.my_progress(bar_max - 1, bar_max) + f" ({methods[1]})")

    cv2.imwrite(general_config['cleared_captcha_file'], img_erosion)
    six_steps = [img_median, masked_img_median,
                 masked_img_median2, masked2_img_median2,
                 img_dilation, img_erosion]
    fig = process_plot.comparison_plot(config, img, multi_step=six_steps)

    result = captcha_funcs.run_model(config, client_config)
    quality_string, extra_chars = detection_quality(captcha, result)
    current_index = general_funcs.get_file_index(filter_dirs[1])
    captcha_file = filter_dirs[1] + "/Captcha #" + str(current_index) + " - '" + result + "' (" + quality_string
    if extra_chars:
        captcha_file += ", " + extra_chars
    fig.savefig(captcha_file + ").png", bbox_inches='tight')

    pbar.set_postfix_str("Method Number: " + general_funcs.my_progress(bar_max, bar_max))
    pyplot.close()
