from configparser import ConfigParser, ExtendedInterpolation
# from selenium.webdriver.support.wait import WebDriverWait
# - - - - - - - - - - - - - - -
from lib.load_analyzer_config_file import LoadConfig
from lib import def_analyzer_config_file as create_config, detect_arch, general_funcs, solve_captcha


def get_cookie_and_over_captcha():
    global driver

    configurations = ConfigParser(interpolation=ExtendedInterpolation())
    config_file = "analyzer configurations.ini"
    configurations.read(config_file)
    create_config.read_config_file(config_file)

    config = LoadConfig()
    general_config = config.general()
    website_config = config.website()

    if general_config['save_history']:
        indexes = {'captcha_pass_index':
                       general_funcs.get_file_index(general_config['captcha_history_dir'] + "/Succeeded"),
                   'captcha_fail_index':
                       general_funcs.get_file_index(general_config['captcha_history_dir'] + "/Failed"),
                   'process_pass_index':
                       general_funcs.get_file_index(general_config['process_history_dir'] + "/Succeeded"),
                   'process_fail_index':
                       general_funcs.get_file_index(general_config['process_history_dir'] + "/Failed"),
                   'cleared_pass_index':
                       general_funcs.get_file_index(general_config['cleared_history_dir'] + "/Succeeded"),
                   'cleared_fail_index':
                       general_funcs.get_file_index(general_config['cleared_history_dir'] + "/Failed")}
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


if __name__ == "__main__":
    get_cookie_and_over_captcha()
