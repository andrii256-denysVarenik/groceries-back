from app.parser import Parser


class Auchan(Parser):

    def __init__(self):
        Parser.__init__(self)
        self._link = 'https://auchan.zakaz.ua'
        self._good = None
        self._weight = None
        self._units = None

    @staticmethod
    def get_category() -> dict:
        return {
            "corn": "corn-groats",
            "buckwheat": "buckwheat",
            "rice": "rice",
            "barley": "barley-groats",
            "wheat": "wheat-groats",
        }

    @staticmethod
    def get_goods(soup):
        return soup.find("div", {"class": "ProductsBox__list"}).findAll("div", {"class": "ProductsBox__listItem"})

    def get_name(self) -> str:
        return self._good.a["title"]

    def get_img(self):
        return self._good.find("div", {"class": "ProductTile__imageContainer"}).img['src'].replace('150', '350')

    def get_link(self):
        return self._good.a["href"]

    def get_weight(self):
        w_and_u = self._find_w_and_u(self._good.find("div", {"class": "ProductTile__weight"}).string)
        weight, units = [w_and_u.group(1), w_and_u.group(2)] if w_and_u else ['1000', 'г']
        kilo = 1000 if units == 'кг' else 1
        weight = self._weight_to_float(weight) * kilo
        self._weight, self._units = weight, units
        return weight

    def get_price(self):
        price = self._good.find("span", {"class": "Price__value_caption"}).string
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
            "shopName": "Ашан"
        })

    def run(self):
        for type_good, part_link in self.get_category().items():
            link = f'{self._link}/uk/categories/{part_link}-auchan/'
            soup = self._get_soup(link)
            goods = self.get_goods(soup)
            if not goods:
                break
            for good in goods:
                self._good = good
                self.insert_good(type_good)


if __name__ == '__main__':
    Auchan().run()
