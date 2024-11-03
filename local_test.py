import cv2
from os import makedirs, listdir
from os.path import isfile, join
from configparser import ConfigParser, ExtendedInterpolation
from tqdm import tqdm   # , trange
from time import sleep
# - - - - - - - - - - - - - - -
from lib.load_analyzer_config_file import LoadConfig
from lib.local_test import local_test_funcs as test_func
from lib import general_funcs, def_analyzer_config_file as create_config, captcha_funcs


configurations = ConfigParser(interpolation=ExtendedInterpolation())
config_file = "analyzer configurations.ini"
configurations.read(config_file)
create_config.read_config_file(config_file)

config = LoadConfig()
filter_config = config.filter()
client_config = config.client()
test_config = config.local_test()

# Create the filters folders if not exist
makedirs(test_config['filter_1_dir'], exist_ok=True)
makedirs(test_config['filter_1_masked_dir'], exist_ok=True)
makedirs(test_config['filters_1_2_3_dir'], exist_ok=True)
makedirs(test_config['filters_1_2_3_masked_dir'], exist_ok=True)
makedirs(test_config['filters_2_3_dir'], exist_ok=True)
makedirs(test_config['5_steps_filtering_dir'], exist_ok=True)
makedirs(test_config['6_steps_filtering_dir'], exist_ok=True)

captcha_pics = [f for f in listdir(test_config['test_db_dir']) if isfile(join(test_config['test_db_dir'], f))]
model_test_repeats = test_config['model_test_repeats']
model_test_results = [0] * model_test_repeats

pbar = tqdm(captcha_pics, bar_format='{l_bar}{bar:10}{r_bar}{bar:-10b}', desc="Capchas Done")
for captcha in pbar:
    img = cv2.imread(test_config['test_db_dir'] + '/' + captcha, 1)[1:-1, 1:-1]
    captcha = captcha[:-4].upper()

    if test_config['test_type'] == "Model Test":
        captcha_funcs.filter_captcha(img, config, filter_config['use_median'], filter_config['use_median_mask'],
                                     filter_config['use_dilate_erode'])

        for i in range(model_test_repeats):
            pbar.set_postfix_str("Runs Done: " + general_funcs.my_progress(i, model_test_repeats))
            model_test_results[i] = captcha_funcs.run_model(config, client_config)

        pbar.set_postfix_str("Runs Done: " + general_funcs.my_progress(model_test_repeats, model_test_repeats))
        constant_result = all(test_result == model_test_results[0] for test_result in model_test_results[1:])
        print("\n", model_test_results)
        if constant_result:
            print("The results are", "\033[92m {}\033[00m" .format("Constant"))
        else:
            print("The results are", "\033[91m {}\033[00m".format("NOT Constant"))

    elif test_config['test_type'] == "Filter Test":
        methods = ["Median", "Median&Mask", "Median + Dilation&Erosion",
                   "Median&Mask + Dilation&Erosion", "Dilation&Erosion",
                   "5 Steps Filtering", "6 Steps Filtering"]
        tested_filters_amount = len(methods)
        use_median = [True, True, True, True, False]
        use_median_mask = [False, True, False, True, False]
        use_dilate_erode = [False, False, True, True, True]
        filter_dirs = [test_config['filter_1_dir'], test_config['filter_1_masked_dir'],
                       test_config['filters_1_2_3_dir'], test_config['filters_1_2_3_masked_dir'],
                       test_config['filters_2_3_dir'],
                       test_config['5_steps_filtering_dir'], test_config['6_steps_filtering_dir']]

        for i in range(tested_filters_amount-2):
            pbar.set_postfix_str("Tested Method: " + general_funcs.my_progress(i, tested_filters_amount) + f" ({methods[i]})")
            test_func.analyze_captcha(img, config, client_config, use_median[i], use_median_mask[i],
                                      use_dilate_erode[i], captcha, filter_dirs[i])
            if i != 2:
                pbar.set_postfix_str("Tested Method: " + general_funcs.my_progress(i + 1, tested_filters_amount) + f" ({methods[i]})")

        test_func.multi_step_filtering(img, config, client_config, captcha, filter_dirs[-2:], methods[-2:],
                                       pbar, tested_filters_amount)

        if captcha != captcha_pics[-1][:-4].upper():
            sleep(test_config['test_client_access_delay'])
