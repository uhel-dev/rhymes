import platform
from typing import List, Any
from selenium import webdriver
import time


def get_browser():
    user_platform = platform.system()
    if user_platform == 'Linux':
        driver = webdriver.Chrome(executable_path='driver/chromedriver')
        return driver
    elif user_platform == 'Windows':
        driver = webdriver.Chrome(executable_path='driver/chromedriver.exe')
        return driver


def get_name_of_songs():
    driver = get_browser()
    driver.get('https://www.hip-hop.pl/lista/?lista=1')
    list_of_all_songs: List[Any] = []
    list_of_all_songs.extend(driver.find_elements_by_class_name('link1'))
    list_of_all_songs.extend(driver.find_elements_by_class_name('link2'))
    return list_of_all_songs


def convert_text_to_url_query():
    list_of_all_songs = get_name_of_songs()
    list_of_songs_text = []
    for song in list_of_all_songs:
        list_of_songs_text.append(song.text.replace(" ", "%20"))
    print(list_of_songs_text)

