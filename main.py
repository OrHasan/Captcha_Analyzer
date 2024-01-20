import os
import sys
import cv2
from configparser import ConfigParser
from gradio_client import Client
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
# - - - - - - - - - - - - - - -
sys.path.insert(1, os.path.abspath('Code'))
from Code import captcha_funcs as func
from Code import def_config_file as create_config

config = ConfigParser()
config_file = "Analyzer Configurations.ini"
config.read(config_file)

# General:
for i in range(2):
    try:
        history_dir = config['general']['history_dir']
        current_index = func.get_file_index(history_dir)
        achieved_captcha_file = config['general']['achieved_captcha_file']
        cleared_captcha_file = config['general']['cleared_captcha_file']
        captcha_attempts = int(config['general']['captcha_attempts'])
        break
    except KeyError:
        create_config.update_config_file("general")

# Debug settings:
for i in range(2):
    try:
        show_comparison = config['debug']['show_comparison']
        break
    except KeyError:
        create_config.update_config_file("debug")

# Filters settings:
# 3 options(median, dilate_erode):
# True, True  /  True, False  /  False, True
for i in range(2):
    try:
        use_median = config['filter']['use_median']
        use_dilate_erode = config['filter']['use_dilate_erode']
        median_kernel_size = int(config['filter']['median_kernel_size'])
        dilate_erode_kernel_size = eval(config['filter']['dilate_erode_kernel_size'])
        dilate_erode_iterations = int(config['filter']['dilate_erode_iterations'])
        break
    except KeyError:
        create_config.update_config_file("filter")

# Client:
for i in range(2):
    try:
        client = Client(config['client']['client_url'])
        client_access_attempts = int(config['client']['client_access_attempts'])
        client_access_delay = float(config['client']['client_access_delay'])
        break
    except KeyError:
        create_config.update_config_file("client")

# website:
# Open the url and find the captcha element
driver = webdriver.Chrome()
for i in range(2):
    try:
        text_field_name = config['website']['text_field_name']
        submit_button_xpath = config['website']['submit_button_xpath']
        driver.get(config['website']['website_url'])
        captcha_id = config['website']['captcha_id']
        break
    except KeyError:
        create_config.update_config_file("website")
captcha = driver.find_element(By.ID, captcha_id)


for i in range(captcha_attempts):
    # captcha.screenshot(achieved_captcha_file)

    img = cv2.imread(achieved_captcha_file, 1)
    fig = func.filter_captcha(img, cleared_captcha_file, use_median, use_dilate_erode, median_kernel_size,
                              dilate_erode_kernel_size, dilate_erode_iterations, show_comparison)

    # API
    result = func.run_model(client, cleared_captcha_file, client_access_attempts)
    print(result)
    # cv2.waitKey(0)

    driver.find_element(By.NAME, text_field_name).send_keys(result)
    driver.find_element(By.XPATH, submit_button_xpath).click()

    captcha_file = history_dir + "/Captcha #" + str(current_index) + "- '" + result

    try:
        captcha = driver.find_element(By.ID, captcha_id)
        fig.savefig(captcha_file + "' - Failed.png", bbox_inches='tight')
        sleep(client_access_delay)

    except:
        print("Debug: Code finished as expected")
        fig.savefig(captcha_file + " - Succeeded.png", bbox_inches='tight')
        break

# cv2.destroyAllWindows()
