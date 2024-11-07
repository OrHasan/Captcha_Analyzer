import re
from configparser import ConfigParser, ExtendedInterpolation
from os import listdir
from os.path import isfile, join
# from selenium.webdriver.support.wait import WebDriverWait
# - - - - - - - - - - - - - - -
from lib import def_analyzer_config_file as create_config, detect_arch, solve_captcha
from lib.load_analyzer_config_file import LoadConfig


def get_file_index(history_dir):
    history_files = [f for f in listdir(history_dir) if isfile(join(history_dir, f))]
    current_index = 0
    for file_name in history_files:
        current_index = max(current_index, int(re.search(r'#(\d+)', file_name).group(1)))
    current_index += 1

    return current_index


def my_progress(curr, N, width=10, bars=u'▉▊▋▌▍▎▏ '[::-1], full='█', empty=' '):
    p = curr / N
    nfull = int(p * width)
    return "{:>3.0%} |{}{}{}| {:>2}/{}"\
        .format(p, full * nfull,
                bars[int(len(bars) * ((p * width) % 1))],
                empty * (width - nfull - 1),
                curr, N)


def solve_captcha_and_get_cookie():
    # global driver
    configurations = ConfigParser(interpolation=ExtendedInterpolation())
    config_file = "analyzer configurations.ini"
    configurations.read(config_file)
    create_config.read_config_file(config_file)

    config = LoadConfig()
    general_config = config.general()
    website_config = config.website()

    if general_config['save_history']:
        indexes = {'captcha_pass_index':
                       get_file_index(general_config['captcha_history_dir'] + "/Succeeded"),
                   'captcha_fail_index':
                       get_file_index(general_config['captcha_history_dir'] + "/Failed"),
                   'process_pass_index':
                       get_file_index(general_config['process_history_dir'] + "/Succeeded"),
                   'process_fail_index':
                       get_file_index(general_config['process_history_dir'] + "/Failed"),
                   'cleared_pass_index':
                       get_file_index(general_config['cleared_history_dir'] + "/Succeeded"),
                   'cleared_fail_index':
                       get_file_index(general_config['cleared_history_dir'] + "/Failed")}
    else:
        indexes = {}

    # Open the url and find the captcha element
    driver = detect_arch.detect_arch_webdriver()
    driver.implicitly_wait(general_config['selenium_minimum_wait'])
    # wait = WebDriverWait(driver, general_config['selenium_condition_wait'])
    driver.get(website_config['website_url'])

    zhe, phpsessid = solve_captcha.solve(driver, config, indexes)

    if website_config['close_on_finish']:
        driver.quit()
    return zhe, phpsessid
