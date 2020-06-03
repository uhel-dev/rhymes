from crawling.crawler import Crawler
import time


class SongUrlCrawler(Crawler):

    def __init__(self):
        Crawler.__init__(self)

    def get_name_of_songs_from_hiphop(self):
        self.get_page_source('https://www.hip-hop.pl/lista/?lista=1')
        list_of_all_songs = []
        list_of_all_songs.extend(self.browser.find_elements_by_class_name('link1'))
        list_of_all_songs.extend(self.browser.find_elements_by_class_name('link2'))
        return list_of_all_songs

    def convert_text_to_url_query(self):
        list_of_all_songs = self.get_name_of_songs_from_hiphop()
        list_of_songs_text = []
        for song in list_of_all_songs:
            list_of_songs_text.append(song.text.replace(" ", "%20"))
        return list_of_songs_text

    def find_urls(self):
        list_of_songs_text = self.convert_text_to_url_query()
        list_of_urls = []
        for song in list_of_songs_text:
            self.get_page_source('https://genius.com/search?q=' + song)
            time.sleep(3)
            try:
                self.browser.find_element_by_xpath(
                    '/html/body/routable-page/ng-outlet/search-results-page/div/div[2]/div[1]/div[2]/search-result-section/div/a').click()
                time.sleep(3)
                for song in self.browser.find_elements_by_xpath(
                        '/html/body/div[6]/div[1]/ng-transclude/search-result-paginated-section/scrollable-data/div/transclude-injecting-local-scope/search-result-item/div/mini-song-card/a'):
                    if 'transleted' not in song.text:
                        list_of_urls.append(song.get_attribute('href'))
            except:
                print(song.replace('%20', ' ') + ' No such song')
        return list_of_urls

