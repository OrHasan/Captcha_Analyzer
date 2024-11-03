import os
import shutil
from selenium.common import exceptions
from selenium.webdriver.common.by import By


def check_if_verified(driver, config, old_text_field_id, fig, result,
                      attempt_number, total_attempts, indexes, captcha_number):
    general_config = config.general()
    website_config = config.website()
    more_captcha_exception = "Different Captcha"
    verified = False
    finished = False
    captcha = None

    try:
        # wait.until(ec.url_changes(captcha_url))
        captcha = driver.find_element(By.ID, website_config['captcha_id'])
        text_field_id = driver.find_elements(By.CSS_SELECTOR,
                                             website_config['text_field_css_selector'])[1].get_attribute("name")

        if text_field_id != old_text_field_id:
            raise Exception(more_captcha_exception)

        print("- Incorrect Text -\n")

        if general_config['save_history']:
            captcha_process_file = general_config['process_history_dir'] + "/Failed/Captcha #" \
                                   + str(indexes['process_fail_index'] + total_attempts - 1) + " - '" + result
            captcha_file_new_dir = general_config['captcha_history_dir'] + "/Failed/Captcha #" \
                                   + str(indexes['captcha_fail_index'] + total_attempts - 1) + " - '" + result
            cleared_captcha_new_dir = general_config['cleared_history_dir'] + "/Failed/Captcha #" \
                                      + str(indexes['cleared_fail_index'] + total_attempts - 1) + " - '" + result

            fig.savefig(captcha_process_file + "' - Attempt " + str(attempt_number) + " - Failed.png",
                        bbox_inches='tight')
            shutil.move(general_config['achieved_captcha_file'],
                        captcha_file_new_dir + "' - Attempt " + str(attempt_number) + " - Failed.png")
            shutil.move(general_config['cleared_captcha_file'],
                        cleared_captcha_new_dir + "' - Attempt " + str(attempt_number) + " - Failed.png")

    except (exceptions.NoSuchElementException, Exception) as e:
        if general_config['save_history']:
            captcha_process_file = general_config['process_history_dir'] + "/Succeeded/Captcha #" \
                                   + str(indexes['process_pass_index'] + captcha_number - 1) + " - '" + result
            captcha_file_new_dir = general_config['captcha_history_dir'] + "/Succeeded/Captcha #" \
                                   + str(indexes['captcha_pass_index'] + captcha_number - 1) + " - '" + result
            cleared_captcha_new_dir = general_config['cleared_history_dir'] + "/Succeeded/Captcha #" \
                                      + str(indexes['cleared_pass_index'] + captcha_number - 1) + " - '" + result

            fig.savefig(captcha_process_file + "' - Attempt " + str(attempt_number) + " - Succeeded.png",
                        bbox_inches='tight')
            shutil.move(general_config['achieved_captcha_file'],
                        captcha_file_new_dir + "' - Attempt " + str(attempt_number) + " - Succeeded.png")
            shutil.move(general_config['cleared_captcha_file'],
                        cleared_captcha_new_dir + "' - Attempt " + str(attempt_number) + " - Succeeded.png")

        verified = True
        if str(e) == more_captcha_exception:
            print("Captcha detected successfully, Proceeding to the next one\n")
        else:
            print("Captcha detected successfully\n")
            text_field_id = None
            finished = True

    if not general_config['save_history']:
        os.remove(general_config['achieved_captcha_file'])
        os.remove(general_config['cleared_captcha_file'])

    return verified, finished, captcha, text_field_id
