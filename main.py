from configparser import ConfigParser, ExtendedInterpolation
# from selenium.webdriver.support.wait import WebDriverWait
# - - - - - - - - - - - - - - -
from lib.load_analyzer_config_file import LoadConfig
from lib import def_analyzer_config_file as create_config, detect_arch, general_funcs, solve_captcha


def main():
    configurations = ConfigParser(interpolation=ExtendedInterpolation())
    config_file = "analyzer configurations.ini"
    configurations.read(config_file)
    create_config.read_config_file(config_file)

    config = LoadConfig()
    general_config = config.general()

    indexes = {'process_pass_index': general_funcs.get_file_index(general_config['process_history_dir'] + "/Succeeded"),
               'process_fail_index': general_funcs.get_file_index(general_config['process_history_dir'] + "/Failed"),
               'cleared_pass_index': general_funcs.get_file_index(general_config['cleared_history_dir'] + "/Succeeded"),
               'cleared_fail_index': general_funcs.get_file_index(general_config['cleared_history_dir'] + "/Failed")}

    # Open the url and find the captcha element
    driver = detect_arch.detect_arch_webdriver()
    driver.implicitly_wait(general_config['selenium_minimum_wait'])
    # wait = WebDriverWait(driver, general_config['selenium_condition_wait'])
    driver.get(config.website()['website_url'])

    zhe, phpsessid = solve_captcha.solve(driver, config, indexes)
    driver.quit()
    return zhe, phpsessid


if __name__ == "__main__":
    main()
