import os
import sys
import cv2
from os import listdir
from os.path import isfile, join
from configparser import ConfigParser
from gradio_client import Client
from tqdm import tqdm
from time import sleep
# - - - - - - - - - - - - - - -
sys.path.insert(1, os.path.abspath('Code'))
sys.path.insert(1, os.path.abspath('Code/Local Test'))
import local_test_funcs as test_func
from Code import captcha_funcs as func
from Code import def_config_file as create_config


config = ConfigParser()
config_file = "Analyzer Configurations.ini"
config.read(config_file)

# General:
for i in range(2):
    try:
        cleared_captcha_file = config['general']['cleared_captcha_file']
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
# 3 options(median, dilate_erode):      - relevant to "Model Test"
# True, True  /  True, False  /  False, True
for i in range(2):
    try:
        use_median = eval(config['filter']['use_median'])
        use_dilate_erode = eval(config['filter']['use_dilate_erode'])
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
        break
    except KeyError:
        create_config.update_config_file("client")

# Tests:
# "Model Test" - Test the analysis model constancy
# "Filter Test" - Test different filtering steps
for i in range(2):
    try:
        test_type = config['local_test']['test_type']
        test_db_dir = config['local_test']['test_database_dir']
        test_client_access_delay = float(config['local_test']['test_client_access_delay'])

        # Model Test variables:
        model_test_repeats = int(config['local_test']['model_test_repeats'])
        model_test_results = [0] * model_test_repeats

        # Filter Test variables:
        filter_1_dir = config['local_test']['filter_1_dir']
        filters_1_2_3_dir = config['local_test']['filters_1_2_3_dir']
        filters_2_3_dir = config['local_test']['filters_2_3_dir']
        break
    except KeyError:
        create_config.update_config_file("local_test")

# Create the filters folders if not exist
os.makedirs(filter_1_dir, exist_ok=True)
os.makedirs(filters_1_2_3_dir, exist_ok=True)
os.makedirs(filters_2_3_dir, exist_ok=True)

captcha_pics = [f for f in listdir(test_db_dir) if isfile(join(test_db_dir, f))]


for captcha in captcha_pics:
    img = cv2.imread(test_db_dir + '/' + captcha, 1)
    captcha = captcha[:-4].upper()

    if test_type == "Model Test":
        func.filter_captcha(img, cleared_captcha_file, use_median, use_dilate_erode, median_kernel_size,
                            dilate_erode_kernel_size, dilate_erode_iterations, show_comparison)

        for i in tqdm(range(model_test_repeats)):
            model_test_results[i] = func.run_model(client, cleared_captcha_file, client_access_attempts)

        constant_result = all(test_result == model_test_results[0] for test_result in model_test_results[1:])
        print(model_test_results)
        if constant_result:
            print("The results are", "\033[92m {}\033[00m" .format("Constant"))
        else:
            print("The results are", "\033[91m {}\033[00m".format("NOT Constant"))

    elif test_type == "Filter Test":
        use_median = True
        use_dilate_erode = False
        test_func.analyze_captcha(img, cleared_captcha_file, use_median, use_dilate_erode,
                                  median_kernel_size, dilate_erode_kernel_size, dilate_erode_iterations,
                                  show_comparison, client, client_access_attempts, captcha, filter_1_dir)
        sleep(test_client_access_delay)

        use_median = True
        use_dilate_erode = True
        test_func.analyze_captcha(img, cleared_captcha_file, use_median, use_dilate_erode,
                                  median_kernel_size, dilate_erode_kernel_size, dilate_erode_iterations,
                                  show_comparison, client, client_access_attempts, captcha, filters_1_2_3_dir)
        sleep(test_client_access_delay)

        use_median = False
        use_dilate_erode = True
        test_func.analyze_captcha(img, cleared_captcha_file, use_median, use_dilate_erode,
                                  median_kernel_size, dilate_erode_kernel_size, dilate_erode_iterations,
                                  show_comparison, client, client_access_attempts, captcha, filters_2_3_dir)
        if captcha != captcha_pics[-1][:-4].upper():
            sleep(test_client_access_delay)
