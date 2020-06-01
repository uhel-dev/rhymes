import platform
from selenium import webdriver


def get_browser():
    user_platform = platform.system()
    if user_platform == 'Linux':
        driver = webdriver.Chrome(executable_path='driver/chromedriver')
        return driver
    elif user_platform == 'Windows':
        driver = webdriver.Chrome(executable_path='driver/chromedriver.exe')
        return driver


driver = get_browser()
driver.get('https://www.python.org')