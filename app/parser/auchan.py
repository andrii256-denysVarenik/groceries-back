from app.parser import get_soup, BASE_URL, get_weight_and_units, get_weight, price_per_kg, get_date
from app.parser import db

CATEGORY = {
    "corn": "corn-groats",
    "buckwheat": "buckwheat",
    "rice": "rice",
    "barley": "barley-groats",
    "wheat": "wheat-groats",
}


def get_start(category):
    for type_good, num in category.items():
        link = f'{BASE_URL["auchan"]}/uk/categories/{num}-auchan/'
        soup = get_soup(link)
        goods = get_goods(soup)
        for good in goods:
            get_good(good, type_good)


def get_goods(soup) -> list:
    return soup.find("div", {"class": "ProductsBox__list"}).findAll("div", {"class": "ProductsBox__listItem"})


def get_good(good, type_good: str):
    name = get_name(good)
    weight, units = get_weight_and_units(get_weight(good))
    price = get_price(good)
    price = price_per_kg(units, float(price), weight)
    data = {
        "type": type_good,
        "title": name,
        "pictureLink": get_img(good),
        "pricePerKg": float(f"{price:.2f}"),
        "weight": weight,
        "link": BASE_URL['auchan'] + get_link(good),
        "date": get_date(),
        "shopName": "Ашан"
    }
    db.insert_goods(data)


def get_name(good) -> str:
    return good.a["title"]


def get_img(good):
    return good.find("div", {"class": "ProductTile__imageContainer"}).img['src'].replace('150', '350')


def get_image(good):
    return good.find("div", {"class": "ProductTile__imageContainer"}).img['src'].replace('150', '350')


def get_price(good):
    return good.find("span", {"class": "Price__value_caption"}).string


def get_link(good):
    return good.a["href"]


if __name__ == "__main__":
    get_start(CATEGORY)
