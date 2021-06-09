from app.parser import Parser
from re import findall


class Tavriav(Parser):

    def __init__(self):
        Parser.__init__(self)
        self._link = 'https://tavriav.ua'
        self._good = None
        self._weight = None
        self._units = None

    @staticmethod
    def get_category() -> dict:
        return {
            "corn": 96,
            "buckwheat": 94,
            "rice": 97,
            "barley": 102,
            "wheat": 100,
        }

    @staticmethod
    def get_goods(soup):
        return soup.find("div", {"class": "catalog-products__container"}).findAll("div", {"class": "products__item"})

    def get_name(self) -> str:
        return self._good.find("p", {"class": "product__title"}).a.string

    def get_img(self):
        img_good = self._good.find("div", {"class": "product__image"}).img["src"]
        return img_good.replace(findall(r'(resize_\d+x\d+)', img_good)[0], 'resize_250x200')

    def get_link(self):
        return self._good.find("p", {"class": "product__title"}).a["href"]

    def get_weight(self):
        w_and_u = self._find_w_and_u(self.get_name())
        weight, units = [w_and_u.group(1), w_and_u.group(2)] if w_and_u else ['1000', 'г']
        kilo = 1000 if units == 'кг' else 1
        weight = self._weight_to_float(weight) * kilo
        self._weight, self._units = weight, units
        return weight

    def get_price(self):
        price = self._good.find("p", {"class": "product__price"})
        if price.b:
            price = price.b.string.strip().replace(',', '.').split(' ')[0]
        else:
            price = price.find('span', {"class": "price__old"}).string.strip().replace(',', '.').split(' ')[0]
        return float(price) / self._weight * 1000

    def insert_good(self, type_good: str):
        self._provider.insert_goods({
            "type": type_good,
            "title": self.get_name(),
            "pictureLink": self.get_img(),
            "weight": self.get_weight(),
            "pricePerKg": self.get_price(),
            "link": self._link + self.get_link(),
            "date": self._get_date(),
            "shopName": "Таврія В"
        })

    def run(self):
        for type_good, part_link in self.get_category().items():
            link = f'{self._link}/subcatalog/{part_link}/'
            soup = self._get_soup(link)
            goods = self.get_goods(soup)
            if not goods:
                break
            for good in goods:
                self._good = good
                self.insert_good(type_good)


if __name__ == '__main__':
    Tavriav().run()
