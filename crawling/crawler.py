import platform

from selenium import webdriver

list_of_all_vowels = ['a', 'ą', 'e', 'ę', 'i', 'o', 'u', 'y', 'ó']
#
# class DatabaseConnector:
#
#     def __init__(self):
#         self.db = MySQLdb.connect(
#             host='rhymes.coptohj5zzcm.us-east-1.rds.amazonaws.com',
#             port='3306',
#             user='admin',
#             password='zapalniczka123',
#         )

class DatabaseEntry:

    def __init__(self, word, vowels, nofVowels, nofChars):
        self.word = word
        self.vowels = vowels
        self.nofVowels = nofVowels
        self.nofChars = nofChars

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

        print(db_entries)



class GeniusCrawler(Crawler):

    def __init__(self):
        Crawler.__init__(self)


    def extract_lyrics_from_url(self, url):
        self.get_page_source(url)
        lyrics = self.browser.find_element_by_class_name('lyrics')
        lyrics = lyrics.find_element_by_css_selector('section').find_element_by_css_selector('p').text
        return lyrics

    def get_database_entries(self, url):
        lyrics = self.extract_lyrics_from_url(url)
        words = self.parse_lyrics(lyrics)
        db_entries = []
        for word in words:
            db_entries.append(self.get_database_entry(word))

        print(db_entries)



# c = TekstowoCrawler()
# c = GeniusCrawler()
# c.get_database_entries('https://www.tekstowo.pl/piosenka,sarius,sam.html')
# lyrics = c.extract_lyrics_from_url('https://genius.com/Sarius-sam-lyrics')
# c.parse_lyrics(lyrics)
# lyrics = c.extract_lyrics_from_url('https://www.tekstowo.pl/piosenka,sarius,sam.html')
# c.parse_lyrics(lyrics)


# ioe
# c.get_vowels('ziomek')