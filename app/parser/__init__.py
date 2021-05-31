from bs4 import BeautifulSoup
from requests import get
import re


BASE_URL = {
    'tavriav': 'https://tavriav.ua',
    'auchan': 'https://auchan.zakaz.ua',
    'metro': 'https://metro.zakaz.ua',
    'fozzy': 'https://fozzyshop.ua/',
    'atb': 'https://zakaz.atbmarket.com/',
}


def get_soup(url: str):
    return BeautifulSoup(get(url).text, 'html.parser')


def get_weight(good) -> str:
    return good.find("div", {"class": "ProductTile__weight"}).string


def get_weight_and_units(name_good) -> list:
    weight = re.search(r'(\d*х*x*\d*,*\.*\d+)\s*(к*г)', name_good)
    weight, units = [weight.group(1), weight.group(2)] if weight else ['1', 'кг']
    return [weight_to_float(weight), units]


def weight_to_float(weight: str):
    weight = weight.replace(',', '.')
    try:
        weight = float(weight)
    except:
        x, y = weight.split('х') if weight.split('х') else weight.split('x')
        weight = float(x) * float(y)
    return weight


def price_per_kg(units: str, price: float, weight: float) -> float:
    kilo = 1000 if units == 'г' else 1
    cost = price / weight * kilo
    return cost


from ..parser.tavriav import get_start
