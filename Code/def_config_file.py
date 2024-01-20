import os
import configparser


def create_general_section():
    # General:
    config['general'] = {'history_dir': "Data/History",
                         'achieved_captcha_file': "Data/New Captcha.png",
                         'cleared_captcha_file': "Data/Cleared Captcha.png",
                         'captcha_attempts': "20"}

def create_website_section():
    # Website:
    config['website'] = {'website_url': "https://www.zone-h.org/archive?hz=1",
                         'captcha_id': "cryptogram",
                         'text_field_name': "captcha",
                         'submit_button_xpath': "//*[@id='propdeface']/form/input[2]"}

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
    config['debug'] = {'show_comparison': "True"}

def create_local_test_section():
    # Tests:
    # test_type: "Model Test" - Test the analysis model constancy / "Filter Test" - Test different filtering steps
    config['local_test'] = {'test_type': "Filter Test",
                            'test_database_dir': "Data/Test Database",
                            'test_client_access_delay': "0.5",
                            # Model Test variables:
                            'model_test_repeats': "10",
                            # Filter Test variables:
                            'filter_1_dir': "Data\Methods Test\Filter 1",
                            'filters_1_2_3_dir': "Data\Methods Test\Filters 1,2,3",
                            'filters_2_3_dir': "Data\Methods Test\Filters 2,3"}


def create_config_file():
    create_general_section()
    create_website_section()
    create_filters_section()
    create_client_section()
    create_debug_section()
    create_local_test_section()

    with open('Analyzer Configurations.ini', 'w') as configfile:
        config.write(configfile)


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

    with open('Analyzer Configurations.ini', 'w') as configfile:
        config.write(configfile)


config = configparser.ConfigParser()
config_file = "Analyzer Configurations.ini"
if not os.path.isfile(config_file):
    print("\n\033[43m {}\033[00m".format('WARNING'), 'The Configurations file',
          "\033[33m {}\033[00m".format('IS MISSING !'))
    print('Creating default configurations file.')
    create_config_file()
config.read(config_file)
