import datetime
import re

from app.database.provider import insert_goods
from app.parser import get_soup, BASE_URL, get_weight_and_units, price_per_kg

# max_num = 681
CATEGORY = {
        "corn": 96,
        "buckwheat": 94,
        "rice": 97,
        "barley": 102,
        "wheat": 100,
    }


def get_name(good) -> str:
    return good.find("p", {"class": "product__title"}).a.string


def get_link(good) -> str:
    return BASE_URL["tavriav"] + good.find("p", {"class": "product__title"}).a["href"]


def get_img(good) -> str:
    img_good = good.find("div", {"class": "product__image"}).img["src"]
    return img_good.replace(re.findall(r'(resize_\d+x\d+)', img_good)[0], 'resize_250x200')


def get_price(good) -> list:
    price = good.find("p", {"class": "product__price"})
    if price.b:
        price_good = price.b.string.strip().replace(',', '.').split(' ')[0]
        before_discount = None
        return [price_good, before_discount]
    else:
        discount_good = price.find('span', {"class": "price__discount"}).string.strip().replace(',', '.').split(' ')[0]
        before_discount = price.find('span', {"class": "price__old"}).string.strip().replace(',', '.').split(' ')[0]
        return [discount_good, before_discount]


def get_good(good, type_good: str):
    name = get_name(good)
    weight, units = get_weight_and_units(name)
    price, before_discount = get_price(good)
    price = price_per_kg(units, float(price), weight)
    data = {
        "type": type_good,
        "title": name,
        "pictureLink": get_img(good),
        "pricePerKg": float(f"{price:.2f}"),
        "weight": weight,
        "link": get_link(good),
        "date": datetime.datetime.combine(datetime.date.today(), datetime.time.min),
        "shopName": "Таврія В"
    }
    if before_discount:
        before_discount = price_per_kg(units, float(before_discount), weight)
        data['before_discount'] = float(f"{before_discount:.2f}")
    insert_goods(data)


def get_goods(soup) -> list:
    return soup.find("div", {"class": "catalog-products__container"}).findAll("div", {"class": "products__item"})


def get_start(category: dict):
    for type_good, num in category.items():
        link = f'{BASE_URL["tavriav"]}/subcatalog/{num}/'
        soup = get_soup(link)
        goods = get_goods(soup)
        for good in goods:
            get_good(good, type_good)


if __name__ == "__main__":
    get_start(CATEGORY)
