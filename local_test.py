import cv2
from os import makedirs, listdir
from os.path import isfile, join
from configparser import ConfigParser, ExtendedInterpolation
from tqdm import tqdm
from time import sleep
# - - - - - - - - - - - - - - -
from lib.load_analyzer_config_file import LoadConfig
from lib.local_test import local_test_funcs as test_func
from lib import def_analyzer_config_file as create_config, captcha_funcs


configurations = ConfigParser(interpolation=ExtendedInterpolation())
config_file = "analyzer configurations.ini"
configurations.read(config_file)
create_config.read_config_file(config_file)

config = LoadConfig()
general_config = config.general()
filter_config = config.filter()
client_config = config.client()
test_config = config.local_test()

# Create the filters folders if not exist
makedirs(test_config['filter_1_dir'], exist_ok=True)
makedirs(test_config['filters_1_2_3_dir'], exist_ok=True)
makedirs(test_config['filters_2_3_dir'], exist_ok=True)

captcha_pics = [f for f in listdir(test_config['test_db_dir']) if isfile(join(test_config['test_db_dir'], f))]

for captcha in captcha_pics:
    img = cv2.imread(test_config['test_db_dir'] + '/' + captcha, 1)
    captcha = captcha[:-4].upper()

    if test_config['test_type'] == "Model Test":
        captcha_funcs.filter_captcha(img, config, filter_config['use_median'], filter_config['use_dilate_erode'])
        model_test_results = [captcha_funcs.run_model(config, client_config) for i
                              in tqdm(range(test_config['model_test_repeats']), desc="Captcha Transcribes")]
        constant_result = all(test_result == model_test_results[0] for test_result in model_test_results[1:])
        print(model_test_results)
        if constant_result:
            print("The results are", "\033[92m {}\033[00m" .format("Constant"))
        else:
            print("The results are", "\033[91m {}\033[00m".format("NOT Constant"))

    elif test_config['test_type'] == "Filter Test":
        use_median = True
        use_dilate_erode = False
        test_func.analyze_captcha(img, config, client_config, use_median, use_dilate_erode,
                                  captcha, test_config['filter_1_dir'])
        sleep(test_config['test_client_access_delay'])

        use_median = True
        use_dilate_erode = True
        test_func.analyze_captcha(img, config, client_config, use_median, use_dilate_erode,
                                  captcha, test_config['filters_1_2_3_dir'])
        sleep(test_config['test_client_access_delay'])

        use_median = False
        use_dilate_erode = True
        test_func.analyze_captcha(img, config, client_config, use_median, use_dilate_erode,
                                  captcha, test_config['filters_2_3_dir'])
        if captcha != captcha_pics[-1][:-4].upper():
            sleep(test_config['test_client_access_delay'])
