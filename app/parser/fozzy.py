from app.parser import Parser
from selenium import webdriver
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
from os import environ


class Fozzy(Parser):

    def __init__(self):
        Parser.__init__(self)
        self._link = 'https://fozzyshop.ua'
        self._options = webdriver.ChromeOptions()

        self._options.binary_location = environ.get("GOOGLE_CHROME_BIN")
        self._options.add_argument('--headless')
        self._options.add_argument('--no-sandbox')
        self._options.add_argument('--disable-dev-shm-usage')
        self._options.add_argument(f'user-agent={UserAgent().random}')

        self.__browser = webdriver.Chrome(executable_path=environ.get("CHROMEDRIVER_PATH"),
                                          chrome_options=self._options)
        self._good = None
        self._weight = None
        self._units = None
        self._price = None

    @staticmethod
    def get_category() -> dict:
        return {
            "corn": '300149-kukuruza',
            "buckwheat": '300143-krupa-grechnevaya',
            "rice": '300152-ris',
            "barley": '300148-krupa-yachnevaya',
            "wheat": '300147-krupa-pshenichnaya',
        }

    @staticmethod
    def get_goods(soup):
        return soup.findAll("div", {"class": "js-product-miniature-wrapper"})

    def get_name(self) -> str:
        return self._good.find("div", {"class": "product-title"}).a['title']

    def get_img(self):
        return self._good.find("div", {"class": "thumbnail-container"}).img["src"]

    def get_link(self):
        return self._good.find("div", {"class": "thumbnail-container"}).a['href']

    def get_weight(self):
        w_and_u = self._find_w_and_u(self.get_name())
        weight, units = [w_and_u.group(1), w_and_u.group(2)] if w_and_u else ['1000', 'г']
        kilo = 1000 if units == 'кг' else 1
        weight = self._weight_to_float(weight) * kilo
        self._weight, self._units = weight, units
        return weight

    def get_price(self):
        div = self._good.find("div", {"class": "retail-price"})
        if div:
            price = div.find("span", {"class": "product-price"})['content']
            return float(price) / self._weight * 1000
        return 0

    def insert_good(self, type_good: str):
        print({
            "type": type_good,
            "title": self.get_name(),
            "pictureLink": self.get_img(),
            "weight": self.get_weight(),
            "pricePerKg": self.get_price(),
            "link": self._link + self.get_link(),
            "date": self._get_date(),
            "shopName": "Fozzy"
        })
        # self._provider.insert_goods({
        #     "type": type_good,
        #     "title": self.get_name(),
        #     "pictureLink": self.get_img(),
        #     "weight": self.get_weight(),
        #     "pricePerKg": self.get_price(),
        #     "link": self._link + self.get_link(),
        #     "date": self._get_date(),
        #     "shopName": "Fozzy"
        # })

    def _get_soup(self, link: str):
        self.__browser.set_page_load_timeout(15)
        try:
            self.__browser.get(link)
        except:
            self.__browser.get(link)
        html = self.__browser.page_source
        self.__browser.quit()
        return BeautifulSoup(html, 'html.parser')

    def run(self):
        for type_good, part_link in self.get_category().items():
            link = f'{self._link}/{part_link}'
            soup = self._get_soup(link)
            goods = self.get_goods(soup)
            if not goods:
                break
            for good in goods:
                self._good = good
                self.insert_good(type_good)


if __name__ == '__main__':
    Fozzy().run()
