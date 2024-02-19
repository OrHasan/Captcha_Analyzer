import os
from configparser import ConfigParser, ExtendedInterpolation


def create_general_section():
    # General:
    config['general'] = {'data_folder': "data",
                         'history_dir': "${data_folder}/history",
                         'process_history_dir': "${history_dir}/filtering process",
                         'cleared_history_dir': "${history_dir}/cleared captchas",
                         'achieved_captcha_file': "${data_folder}/new captcha.png",
                         'cleared_captcha_file': "${data_folder}/cleared captcha.png",
                         'captcha_attempts': "50",
                         'capcha_maximum_length': "5",
                         'letters_only': "True",
                         'selenium_minimum_wait': '1',
                         'selenium_condition_wait': '3'}


def create_website_section():
    # Website:
    config['website'] = {'website_url': "https://www.zone-h.org/archive?hz=1",
                         'captcha_id': "cryptogram",
                         'text_field_name': "captcha",
                         'submit_button_xpath': "//*[@id='propdeface']/form/input[2]",
                         'close_on_finish': "False"}


def create_filters_section():
    # Filters settings:
    # 3 options(median, dilate_erode):
    # True, True  /  True, False  /  False, True
    config['filter'] = {'use_median': "True",
                        'use_dilate_erode': "False",
                        'median_kernel_size': "5",
                        'dilate_erode_kernel_size': "(3, 3)",
                        'dilate_erode_iterations': "1"}


def create_client_section():
    # Client:
    config['client'] = {'client_url': "https://docparser-text-captcha-breaker.hf.space/",
                        'client_access_attempts': "3",
                        'client_access_delay': "0.25"}


def create_debug_section():
    # Debug settings:
    config['debug'] = {'show_comparison': "False"}


def create_local_test_section():
    # Tests:
    # test_type: "Model Test" - Test the analysis model constancy / "Filter Test" - Test different filtering steps
    config['local_test'] = {'test_type': "Filter Test",
                            'test_database_dir': "${general:data_folder}/test database",
                            'test_client_access_delay': "0.5",
                            # Model Test variables:
                            'model_test_repeats': "10",
                            # Filter Test variables:
                            'methods_test_dir': "${general:data_folder}/methods test",
                            'filter_1_dir': "${methods_test_dir}/filter 1",
                            'filters_1_2_3_dir': "${methods_test_dir}/filters 1,2,3",
                            'filters_2_3_dir': "${methods_test_dir}/filters 2,3"}


def read_config_file(config_file_name="analyzer configurations.ini"):
    global config_file, config

    config_file = config_file_name
    config = ConfigParser(interpolation=ExtendedInterpolation())
    if not os.path.isfile(config_file):
        print("\n\033[43m {}\033[00m".format('WARNING'), 'The Configurations file',
              "\033[33m {}\033[00m".format('IS MISSING !'))
        print('Creating default configurations file.')
        create_config_file()
    config.read(config_file)


def create_config_file():
    create_general_section()
    create_website_section()
    create_filters_section()
    create_client_section()
    create_debug_section()
    create_local_test_section()

    with open(config_file, 'w') as configfile:
        config.write(configfile)
    config.read(config_file)


def update_config_file(section):
    print("\n\033[43m {}\033[00m".format('WARNING'), "\033[33m {}\033[00m".format('MISSING DATA'),
          'in the "' + section + '" section ')
    print('Recreating the section with default data.')

    if section == "general":
        create_general_section()

    elif section == "website":
        create_website_section()

    elif section == "filter":
        create_filters_section()

    elif section == "client":
        create_client_section()

    elif section == "debug":
        create_debug_section()

    elif section == "local_test":
        create_local_test_section()

    else:
        print("\n\033[41m {}\033[00m".format('ERROR'),
              "\033[91m {}\033[00m".format('\'' + section + '\' section isn\'t exist !'))
        print('Please recheck the section name inside the code')
        return "Unavailable Section"

    with open(config_file, 'w') as configfile:
        config.write(configfile)
    config.read(config_file)


global config_file, config
