from app.parser import get_soup, BASE_URL, get_weight_and_units, price_per_kg, get_date
from app.parser import db


def get_start():
    CATEGORY = {
        "corn": '300149-kukuruza',
        "buckwheat": '300143-krupa-grechnevaya',
        "rice": '300152-ris',
        "barley": '300148-krupa-yachnevaya',
        "wheat": '300147-krupa-pshenichnaya',
    }
    for type_good, num in CATEGORY.items():
        for i in range(1, 11):
            link = f'{BASE_URL["fozzy"]}/{num}?page={i}'
            soup = get_soup(link)
            goods = get_goods(soup)
            if not goods:
                break
            for good in goods:
                get_good(good, type_good)


def get_goods(soup):
    return soup.findAll("div", {"class": "js-product-miniature-wrapper"})


def get_good(good, type_good: str):
    name = get_name(good)
    weight, units = get_weight_and_units(name)
    price = get_price(good)
    if price:
        price = price_per_kg(units, float(price), weight)
        data = {
            "type": type_good,
            "title": name,
            "pictureLink": get_img(good),
            "pricePerKg": float(f"{price:.2f}"),
            "weight": weight,
            "link": get_link(good),
            "date": get_date(),
            "shopName": "Fozzy"
        }
        db.insert_goods(data)


def get_name(good):
    return good.find("div", {"class": "product-title"}).a['title']


def get_img(good):
    return good.find("div", {"class": "thumbnail-container"}).img["src"]


def get_link(good):
    return good.find("div", {"class": "thumbnail-container"}).a['href']


def get_price(good):
    div = good.find("div", {"class": "retail-price"})
    if div:
        return div.find("span", {"class": "product-price"})['content']
    return


if __name__ == "__main__":
    get_start()
