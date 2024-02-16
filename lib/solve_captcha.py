import sys
import cv2
import shutil
from time import sleep
from selenium.common import exceptions
from selenium.webdriver.common.by import By
# - - - - - - - - - - - - - - -
from lib import captcha_funcs


def check_if_verified(driver, config, fig, result, attempt_number, indexes):
    general_config = config.general()
    verified = False
    captcha = None

    try:
        # wait.until(ec.url_changes(captcha_url))
        captcha = driver.find_element(By.ID, config.website()['captcha_id'])

        print("- Incorrect Text -")
        captcha_process_file = general_config['process_history_dir'] + "/Failed/Captcha #" \
                               + str(indexes['process_fail_index'] + attempt_number) + "- '" + result
        cleared_captcha_new_dir = general_config['cleared_history_dir'] + "/Failed/Captcha #" \
                                  + str(indexes['cleared_fail_index'] + attempt_number) + "- '" + result
        fig.savefig(captcha_process_file + "' - Attempt " + str(attempt_number + 1) + " - Failed.png",
                    bbox_inches='tight')
        shutil.move(general_config['cleared_captcha_file'],
                    cleared_captcha_new_dir + "' - Attempt " + str(attempt_number + 1) + " - Failed.png")

    except exceptions.NoSuchElementException:
        print("Captcha detected successfully")

        captcha_process_file = general_config['process_history_dir'] + "/Succeeded/Captcha #" \
                               + str(indexes['process_pass_index']) + "- '" + result
        cleared_captcha_new_dir = general_config['cleared_history_dir'] + "/Succeeded/Captcha #" \
                                  + str(indexes['cleared_pass_index']) + "- '" + result
        fig.savefig(captcha_process_file + "' - Attempt " + str(attempt_number + 1) + " - Succeeded.png",
                    bbox_inches='tight')
        shutil.move(general_config['cleared_captcha_file'],
                    cleared_captcha_new_dir + "' - Attempt " + str(attempt_number + 1) + " - Succeeded.png")

        verified = True

    return verified, captcha


def solve(driver, config, indexes):
    general_config = config.general()
    filter_config = config.filter()
    client_config = config.client()
    website_config = config.website()

    attempts = general_config['captcha_attempts']
    captcha = driver.find_element(By.ID, website_config['captcha_id'])
    for i in range(attempts):
        captcha.screenshot(general_config['achieved_captcha_file'])

        img = cv2.imread(general_config['achieved_captcha_file'], 1)
        fig = captcha_funcs.filter_captcha(img, config, filter_config['use_median'], filter_config['use_dilate_erode'])

        # Send to client to analyze:
        result = captcha_funcs.run_model(config, client_config)
        print(f"Attempt #{i} detected text:", result)
        # cv2.waitKey(0)

        driver.find_element(By.NAME, website_config['text_field_name']).send_keys(result)
        driver.find_element(By.XPATH, website_config['submit_button_xpath']).click()

        verified, captcha = check_if_verified(driver, config, fig, result, i, indexes)
        if verified:
            break

        elif i+1 == attempts:
            print(f"Captcha transcription failed {attempts} times")
            print("\n\033[41m {}\033[00m".format('ERROR'),
                  "\033[91m {}\033[00m".format("FAILED to pass the captcha"))
            sys.exit(1)

        else:
            sleep(client_config['client_access_delay'])

    zhe = driver.get_cookie('ZHE')['value']
    phpsessid = driver.get_cookie('PHPSESSID')['value']
    print("Cookies:\n"
          f"  ZHE: {zhe}\n"
          f"  PHPSESSID: {phpsessid}")

    # cv2.destroyAllWindows()
    return zhe, phpsessid
