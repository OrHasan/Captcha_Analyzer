from difflib import SequenceMatcher
# - - - - - - - - - - - - - - -
from lib import general_funcs, captcha_funcs


def analyze_captcha(img, config, client_config, use_median, use_dilate_erode, captcha, filter_dir):
    fig = captcha_funcs.filter_captcha(img, config, use_median, use_dilate_erode)
    result = captcha_funcs.run_model(config, client_config)
    quality_string, extra_chars = detection_quality(captcha, result)
    current_index = general_funcs.get_file_index(filter_dir)
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