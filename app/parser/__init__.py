# from bs4 import BeautifulSoup
# from requests import get

# BASE_URL = {
#     'tavriav': 'https://tavriav.ua/',
# }
#
#
# def get_soup(url: str):
#     return BeautifulSoup(get(url).text, 'html.parser')
#

from ..parser.tavriav import get_start
