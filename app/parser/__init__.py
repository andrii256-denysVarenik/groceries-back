from selenium import webdriver
from fake_useragent import UserAgent
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from app.database.provider import DbProvider
from datetime import datetime, date, time
from re import search


class Parser(object):

    def __init__(self):
        self._options = webdriver.ChromeOptions()

        self._options.add_argument('headless')
        self._options.add_argument(f'user-agent={UserAgent().random}')

        self.__browser = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=self._options)
        self._provider = DbProvider()

    def _get_soup(self, link: str):
        self.__browser.get(link)
        html = self.__browser.page_source
        self.__browser.quit()
        return BeautifulSoup(html, 'html.parser')

    @staticmethod
    def _get_date():
        return datetime.combine(date.today(), time.min)

    @staticmethod
    def _find_w_and_u(name_good: str):
        return search(r'(\d*х*\**x*\d*,*\.*\d+)\s*(к*г)', name_good)

    @staticmethod
    def _weight_to_float(weight: str):
        weight = weight.replace(',', '.')
        try:
            weight = float(weight)
        except:
            if weight.find('х') != -1:
                x, y = weight.split('х')
            elif weight.find('x') != -1:
                x, y = weight.split('x')
            elif weight.find('*') != -1:
                x, y = weight.split('*')
            else:
                return
            weight = float(x) * float(y)
        return weight

    def run(self):
        pass


from app.parser.auchan import Auchan
from app.parser.fozzy import Fozzy
from app.parser.metro import Metro
from app.parser.tavriav import Tavriav
