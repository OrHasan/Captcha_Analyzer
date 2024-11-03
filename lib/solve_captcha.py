import cv2
from time import sleep
from selenium.webdriver.common.by import By
# - - - - - - - - - - - - - - -
from lib import captcha_funcs, check_status


def solve(driver, config, indexes):
    general_config = config.general()
    filter_config = config.filter()
    client_config = config.client()
    website_config = config.website()

    last_text_field_id = driver.find_elements(By.CSS_SELECTOR,
                                              website_config['text_field_css_selector'])[1].get_attribute("name")
    attempts = general_config['captcha_attempts']
    attempt = 1
    total_attempts = 1
    captcha_number = 1
    zhe = None
    phpsessid = None

    captcha = driver.find_element(By.ID, website_config['captcha_id'])
    while attempt <= attempts:
        captcha.screenshot(general_config['achieved_captcha_file'])

        img = cv2.imread(general_config['achieved_captcha_file'], 1)[1:-1, 1:-1]
        fig = captcha_funcs.filter_captcha(img, config, filter_config['use_median'], filter_config['use_median_mask'],
                                           filter_config['use_dilate_erode'])

        # Send to client to analyze:
        result = captcha_funcs.run_model(config, client_config)[:general_config['capcha_maximum_length']]
        print(f"Attempt #{attempt} detected text:", result)

        if general_config['letters_only'] or general_config['fix_similar_small_letters']:
            result, result_changed = captcha_funcs.remove_numbers_and_fix_small_letters(result, config)
            if result_changed:
                print(f"Text after numbers replacement:", result)
        # cv2.waitKey(0)

        if general_config['capitals_only']:
            result = result.upper()

        driver.find_elements(By.CSS_SELECTOR, website_config['text_field_css_selector'])[1].send_keys(result)
        driver.find_element(By.CSS_SELECTOR, website_config['submit_button_css_selector']).click()

        verified, finished, captcha, last_text_field_id =\
            check_status.check_if_verified(driver, config, last_text_field_id, fig, result,
                                           attempt, total_attempts, indexes, captcha_number)
        if finished:
            zhe = driver.get_cookie('ZHE')['value']
            phpsessid = driver.get_cookie('PHPSESSID')['value']
            print("Cookies:\n"
                  f"  ZHE: {zhe}\n"
                  f"  PHPSESSID: {phpsessid}")
            break

        elif verified:
            attempt = 1
            captcha_number += 1

        elif attempt == attempts:
            print(f"Captcha transcription failed {attempts} times")
            print("\n\033[41m {}\033[00m".format('ERROR'),
                  "\033[91m {}\033[00m".format("FAILED to pass the captcha"))
            # sys.exit(1)
            break

        else:
            attempt += 1
            total_attempts += 1
            sleep(client_config['client_access_delay'])

    # cv2.destroyAllWindows()
    return zhe, phpsessid
