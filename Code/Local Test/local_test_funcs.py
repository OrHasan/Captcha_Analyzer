import os
import sys
from difflib import SequenceMatcher
# - - - - - - - - - - - - - - -
sys.path.insert(1, os.path.abspath('Code'))
from Code import captcha_funcs as func

def analyze_captcha(img, cleared_captcha_file, use_median, use_dilate_erode,
                    median_kernel_size, dilate_erode_kernel_size, dilate_erode_iterations,
                    show_comparison, client, client_access_attempts, captcha, filter_dir):
    fig = func.filter_captcha(img, cleared_captcha_file, use_median, use_dilate_erode, median_kernel_size,
                              dilate_erode_kernel_size, dilate_erode_iterations, show_comparison)
    result = func.run_model(client, cleared_captcha_file, client_access_attempts)
    quality_string, extra_chars = detection_quality(captcha, result)
    current_index = func.get_file_index(filter_dir)
    captcha_file = filter_dir + "/Captcha #" + str(current_index) + "- '" + result + "' (" + quality_string
    if extra_chars:
        captcha_file += ", " + extra_chars

    fig.savefig(captcha_file + ").png", bbox_inches='tight')


def detection_quality(real_text, result_text):
    matcher = SequenceMatcher(None, real_text, result_text)
    matching_blocks = matcher.get_matching_blocks()
    count = sum(block.size for block in matching_blocks if block.a == block.b)
    quality = str(count) + " of " + str(len(real_text)) + " chars"
    if len(result_text) > len(real_text):
        extra_chars = str(len(result_text) - len(real_text)) + " extra chars"
    else:
        extra_chars = ""

    return quality, extra_chars