import cv2
import shutil
from configparser import ConfigParser, ExtendedInterpolation
from time import sleep
from selenium.webdriver.common.by import By
# - - - - - - - - - - - - - - -
from lib.load_analyzer_config_file import LoadConfig
from lib import def_analyzer_config_file as create_config, detect_arch, general_funcs, captcha_funcs


configurations = ConfigParser(interpolation=ExtendedInterpolation())
config_file = "analyzer configurations.ini"
configurations.read(config_file)
create_config.read_config_file(config_file)

config = LoadConfig()
general_config = config.general()
filter_config = config.filter()
client_config = config.client()
website_config = config.website()

process_pass_index = general_funcs.get_file_index(general_config['process_history_dir'] + "/Succeeded")
process_fail_index = general_funcs.get_file_index(general_config['process_history_dir'] + "/Failed")
cleared_pass_index = general_funcs.get_file_index(general_config['cleared_history_dir'] + "/Succeeded")
cleared_fail_index = general_funcs.get_file_index(general_config['cleared_history_dir'] + "/Failed")

# Open the url and find the captcha element
driver = detect_arch.detect_arch_webdriver()
driver.get(website_config['website_url'])
captcha = driver.find_element(By.ID, website_config['captcha_id'])

for i in range(general_config['captcha_attempts']):
    captcha.screenshot(general_config['achieved_captcha_file'])

    img = cv2.imread(general_config['achieved_captcha_file'], 1)
    fig = captcha_funcs.filter_captcha(img, config, filter_config['use_median'], filter_config['use_dilate_erode'])

    # Send to client to analyze:
    result = captcha_funcs.run_model(config, client_config)
    print(result)
    # cv2.waitKey(0)

    driver.find_element(By.NAME, website_config['text_field_name']).send_keys(result)
    driver.find_element(By.XPATH, website_config['submit_button_xpath']).click()

    try:
        captcha = driver.find_element(By.ID, website_config['captcha_id'])

        captcha_process_file = general_config['process_history_dir'] + "/Failed/Captcha #"\
                               + str(process_fail_index+i) + "- '" + result
        cleared_captcha_new_dir = general_config['cleared_history_dir'] + "/Failed/Captcha #"\
                                  + str(cleared_fail_index+i) + "- '" + result
        fig.savefig(captcha_process_file + "' - Attempt " + str(i+1) + " - Failed.png", bbox_inches='tight')
        shutil.move(general_config['cleared_captcha_file'], cleared_captcha_new_dir + "' - Attempt " + str(i+1) + " - Failed.png")
        sleep(config.client()['client_access_delay'])

    except:
        print("Debug: Code finished as expected")

        captcha_process_file = general_config['process_history_dir'] + "/Succeeded/Captcha #"\
                               + str(process_pass_index) + "- '" + result
        cleared_captcha_new_dir = general_config['cleared_history_dir'] + "/Succeeded/Captcha #"\
                                  + str(cleared_pass_index) + "- '" + result
        fig.savefig(captcha_process_file + "' - Attempt " + str(i+1) + " - Succeeded.png", bbox_inches='tight')
        shutil.move(general_config['cleared_captcha_file'],
                    cleared_captcha_new_dir + "' - Attempt " + str(i+1) + " - Succeeded.png")
        break

# cv2.destroyAllWindows()
driver.quit()
