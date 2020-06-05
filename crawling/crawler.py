import platform
import time

from mysql.connector import IntegrityError
from selenium import webdriver
import mysql.connector

list_of_all_vowels = ['a', 'ą', 'e', 'ę', 'i', 'o', 'u', 'y', 'ó']


class DatabaseConnector:

    def __init__(self):
        self.db = mysql.connector.connect(
            host='rhymes.coptohj5zzcm.us-east-1.rds.amazonaws.com',
            port='3306',
            user='admin',
            password='zapalniczka123',
            database='rhymes'
        )

        self.cursor = self.db.cursor()

    def add_song_entry_to_db(self, db_entry):
        try:
            sql = "INSERT INTO words (word, vowels, vowels_count, chars_count) VALUES (%s, %s, %s, %s)"
            val = (db_entry.word, db_entry.vowels, db_entry.vowels_count, db_entry.chars_count)
            self.cursor.execute(sql, val)
            self.db.commit()
        except IntegrityError:
            print('{0} already exists in database'.format(db_entry.word))
        except:
            print('Unable to add: {0}'.format(db_entry.word))

    def add_link_entry_to_db(self, urlin):
        try:
            sql = "INSERT INTO links (url) VALUES (%s)"
            val = (urlin,)
            self.cursor.execute(sql, val)
            self.db.commit()
            print('Entry: {0} added to the DB'.format(val))
        except IntegrityError:
            print('Song {0} already exists in database'.format(urlin))
        except:
            print('Unable to add: {0}'.format(urlin))


class DatabaseEntry:

    def __init__(self, word, vowels, nofVowels, nofChars):
        self.word = word
        self.vowels = vowels
        self.vowels_count = nofVowels
        self.chars_count = nofChars


class Crawler:

    def __init__(self):
        self.browser = self.get_browser()

    def get_browser(self):
        user_platform = platform.system()
        if user_platform == 'Linux':
            driver = webdriver.Chrome(executable_path='/home/sofo/Desktop/rhymes/rhymes/driver/chromedriver_linux')
            return driver
        elif user_platform == 'Windows':
            driver = webdriver.Chrome(executable_path='driver/chromedriver.exe')
            return driver

    def get_page_source(self, url):
        self.browser.get(url)

    def get_vowels(self, word):
        vowels = ''
        for char in word:
            if char in list_of_all_vowels:
                vowels += char
        return vowels

    def get_vowels_count(self, vowels):
        return len(vowels)

    def get_word_char_count(self, word):
        return len(word)

    def get_database_entry(self, word):
        vowels = self.get_vowels(word)
        vowels_count = self.get_vowels_count(vowels)
        chars_count = self.get_word_char_count(word)
        return DatabaseEntry(word, vowels, vowels_count, chars_count)

    def parse_lyrics(self, lyrics):
        words = set()
        lyrics_arr = lyrics.split('\n')
        for sentence in lyrics_arr:
            if sentence != "":
                words_from_sentence = sentence.split(' ')
                for word in words_from_sentence:
                    if word != '':
                        if '\u200a' in word:
                            word = word.split('\u200a')[0]
                            words.add(word.lower())
                        else:
                            words.add(word.lower())
        return words

    def import_from_file(self):
        dictionary = open('/home/sofo/Desktop/rhymes/rhymes/A.txt', 'r')
        db = DatabaseConnector()
        for line in dictionary:
            word = line.strip()
            db_entry = self.get_database_entry(word)
            db.add_song_entry_to_db(db_entry)
        print('Finished')
        dictionary.close()



class TekstowoCrawler(Crawler):

    def __init__(self):
        Crawler.__init__(self)

    def extract_lyrics_from_url(self, url):
        self.get_page_source(url)
        lyrics = self.browser.find_element_by_class_name('song-text').text
        return lyrics

    def get_database_entries(self, url):
        lyrics = self.extract_lyrics_from_url(url)
        words = self.parse_lyrics(lyrics)
        db_entries = []
        for word in words:
            db_entries.append(self.get_database_entry(word))

        return db_entries


class GeniusCrawler(Crawler):

    def __init__(self):
        Crawler.__init__(self)

    def extract_lyrics_from_url(self, url):
        self.get_page_source(url)
        time.sleep(2)
        lyrics = self.browser.find_element_by_class_name('lyrics')
        lyrics = lyrics.find_element_by_css_selector('section').find_element_by_css_selector('p').text
        return lyrics

    def get_database_entries(self, url):
        lyrics = self.extract_lyrics_from_url(url)
        words = self.parse_lyrics(lyrics)
        db_entries = []
        for word in words:
            db_entries.append(self.get_database_entry(word))

        return db_entries

# c = TekstowoCrawler()
# c = GeniusCrawler()
# c.get_database_entries('https://www.tekstowo.pl/piosenka,sarius,sam.html')

# lyrics = c.extract_lyrics_from_url('https://genius.com/Sarius-sam-lyrics')
# c.parse_lyrics(lyrics)
# lyrics = c.extract_lyrics_from_url('https://www.tekstowo.pl/piosenka,sarius,sam.html')
# c.parse_lyrics(lyrics)


# for i in enumerate(dbEntries):
#     print('Adding {0}'.format(dbEntries[i]))
#     db.add_song_entry_to_db(dbEntries[i])

# ioe
# c.get_vowels('ziomek')
dic_import = Crawler()
dic_import.import_from_file()
