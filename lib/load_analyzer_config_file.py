import os
import sys
from configparser import ConfigParser, ExtendedInterpolation
from gradio_client import Client
# - - - - - - - - - - - - - - -
import lib.def_analyzer_config_file as create_config


class LoadConfig:
    def __init__(self, config_file="analyzer configurations.ini"):
        if os.path.basename(os.getcwd()) == "lib":
            config_file_path = os.path.dirname(os.getcwd()) + "/" + config_file
        else:
            config_file_path = config_file

        self.config_file = config_file_path
        create_config.read_config_file(self.config_file)
        self.config = ConfigParser(interpolation=ExtendedInterpolation())
        self.config.read(self.config_file)

    def error_handling(self, fail_count, section):
        if not fail_count:
            create_config.update_config_file(section)
            self.config.read(self.config_file)

        else:
            print("\n\033[41m {}\033[00m".format('ERROR'),
                  "\033[91m {}\033[00m".format("The program CANNOT CONTINUE!"),
                  "The required KEY name ISN'T EXIST in the default data")
            sys.exit(1)

    def general(self):
        for i in range(2):
            try:
                return {
                    'save_history': eval(self.config['general']['save_history']),
                    'captcha_history_dir': self.config['general']['captcha_history_dir'],
                    'process_history_dir': self.config['general']['process_history_dir'],
                    'cleared_history_dir': self.config['general']['cleared_history_dir'],
                    'achieved_captcha_file': self.config['general']['achieved_captcha_file'],
                    'cleared_captcha_file': self.config['general']['cleared_captcha_file'],
                    'captcha_attempts': int(self.config['general']['captcha_attempts']),
                    'capcha_maximum_length': int(self.config['general']['capcha_maximum_length']),
                    'letters_only': eval(self.config['general']['letters_only']),
                    'capitals_only': eval(self.config['general']['capitals_only']),
                    'fix_similar_small_letters': eval(self.config['general']['fix_similar_small_letters']),
                    'selenium_minimum_wait': float(self.config['general']['selenium_minimum_wait']),
                    'selenium_condition_wait': float(self.config['general']['selenium_condition_wait']),
                }

            except KeyError:
                LoadConfig.error_handling(self, i, "general")

    def debug(self):
        for i in range(2):
            try:
                return {
                    'show_comparison': eval(self.config['debug']['show_comparison'])
                }

            except KeyError:
                LoadConfig.error_handling(self, i, "debug")

    def website(self):
        for i in range(2):
            try:
                return {
                    'website_url': self.config['website']['website_url'],
                    'captcha_id': self.config['website']['captcha_id'],
                    'text_field_css_selector': self.config['website']['text_field_css_selector'],
                    'submit_button_css_selector': self.config['website']['submit_button_css_selector'],
                    'close_on_finish': eval(self.config['website']['close_on_finish']),
                    'sql_file_name': self.config['website']['sql_file_name'],
                    'pages_to_scan': int(self.config['website']['pages_to_scan'])
                }

            except KeyError:
                LoadConfig.error_handling(self, i, "website")

    def filter(self):
        # 3 options(median, dilate_erode):
        # True, True  /  True, False  /  False, True
        for i in range(2):
            try:
                return {
                    'use_median': eval(self.config['filter']['use_median']),
                    'use_median_mask': eval(self.config['filter']['use_median_mask']),
                    'use_dilate_erode': eval(self.config['filter']['use_dilate_erode']),
                    'median_kernel_size': int(self.config['filter']['median_kernel_size']),
                    'dilate_kernel_size': eval(self.config['filter']['dilate_kernel_size']),
                    'erode_kernel_size': eval(self.config['filter']['erode_kernel_size']),
                    'dilate_iterations': int(self.config['filter']['dilate_iterations']),
                    'erode_iterations': int(self.config['filter']['erode_iterations'])
                }

            except KeyError:
                LoadConfig.error_handling(self, i, "filter")

    def client(self):
        for i in range(2):
            try:
                return {
                    'client': Client(self.config['client']['client_url']),
                    'client_access_attempts': int(self.config['client']['client_access_attempts']),
                    'client_access_delay': float(self.config['client']['client_access_delay'])
                }

            except KeyError:
                LoadConfig.error_handling(self, i, "client")

    def local_test(self):
        # "Model Test" - Test the analysis model constancy
        # "Filter Test" - Test different filtering steps
        for i in range(2):
            try:
                return {
                    'test_type': self.config['local_test']['test_type'],
                    'test_db_dir': self.config['local_test']['test_database_dir'],
                    'test_client_access_delay': float(self.config['local_test']['test_client_access_delay']),

                    # Model Test variables:
                    'model_test_repeats': int(self.config['local_test']['model_test_repeats']),

                    # Filter Test variables:
                    'filter_1_dir': self.config['local_test']['filter_1_dir'],
                    'filter_1_masked_dir': self.config['local_test']['filter_1_masked_dir'],
                    'filters_1_2_3_dir': self.config['local_test']['filters_1_2_3_dir'],
                    'filters_1_2_3_masked_dir': self.config['local_test']['filters_1_2_3_masked_dir'],
                    'filters_2_3_dir': self.config['local_test']['filters_2_3_dir'],
                    '5_steps_filtering_dir': self.config['local_test']['5_steps_filtering_dir'],
                    '6_steps_filtering_dir': self.config['local_test']['6_steps_filtering_dir']
                }

            except KeyError:
                LoadConfig.error_handling(self, i, "local_test")
