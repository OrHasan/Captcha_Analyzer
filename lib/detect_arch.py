import platform
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options


def identify_system():
    os_name = platform.system()
    architecture = platform.machine()

    if os_name == 'Darwin':
        if architecture == 'x86_64':
            return 'MacOS amd64'
        elif architecture == 'arm64':
            return 'MacOS arm64'
        else:
            return 'MacOS (Unknown Architecture)'

    elif os_name == 'Windows':
        if architecture == 'AMD64':
            return 'Windows amd64'
        else:
            return 'Windows (Unknown Architecture)'

    elif os_name == 'Linux':
        if architecture == 'x86_64':
            return 'Linux amd64'
        else:
            return 'Linux (Unknown Architecture)'

    else:
        return 'Unknown OS and Architecture'


def detect_arch_webdriver():
    # system_info = identify_system()

    options = Options()
    # options.add_argument("--headless")
    options.add_argument("--no-sandbox")    # Linux
    options.add_argument("--disable-gpu")   # Windows / Docker
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")

    return webdriver.Chrome(service=Service(), options=options)

    # if system_info == 'MacOS arm64':
    #     return webdriver.Chrome(service=Service('./selenium/chromedriver-mac-arm64/chromedriver'), options=options)
    # elif system_info == 'MacOS amd64':
    #     return webdriver.Chrome(service=Service('./selenium/chromedriver-mac-x64/chromedriver'), options=options)
    # elif system_info == 'Windows amd64':
    #     return webdriver.Chrome(service=Service('./selenium/chromedriver-win64/chromedriver.exe'), options=options)
    # elif system_info == 'Linux amd64':
    #     return webdriver.Chrome(service=Service('./selenium/chromedriver-linux64/chromedriver'), options=options)
    #
    # raise RuntimeError("Could not detect OS")
