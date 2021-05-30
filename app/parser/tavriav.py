import datetime
import re

from bs4 import BeautifulSoup
from requests import get

from app.database.provider import insert_goods


def get_soup(url: str):
    return BeautifulSoup(get(url).text, 'html.parser')


BASE_URL = {
    'tavriav': 'https://tavriav.ua',
    'atb': 'https://zakaz.atbmarket.com/',
    'silpo': 'https://shop.silpo.ua/',
}

# max_num = 681


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


def get_weight_and_units(name_good) -> list:
    weight = re.search(r'(\d*х*x*\d*,*\.*\d+)\s*(к*г)', name_good)
    weight, units = [weight.group(1), weight.group(2)] if weight else ['1', 'кг']
    return [weight_to_float(weight), units]


def price_per_kg(units: str, price: float, weight: float) -> float:
    kilo = 1000 if units == 'г' else 1
    cost = price / weight * kilo
    return cost


def weight_to_float(weight: str):
    weight = weight.replace(',', '.')
    try:
        weight = float(weight)
    except:
        x, y = weight.split('х') if weight.split('х') else weight.split('x')
        weight = float(x) * float(y)
    return weight


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


def get_start():
    CATEGORY = {
        "corn": 96,
        "buckwheat": 94,
        "rice": 97,
        "barley": 102,
        "wheat": 100,
    }
    for type_good, num in CATEGORY.items():
        link = f'{BASE_URL["tavriav"]}/subcatalog/{num}/'
        soup = get_soup(link)
        goods = get_goods(soup)
        for good in goods:
            get_good(good, type_good)


if __name__ == "__main__":
    get_start()
