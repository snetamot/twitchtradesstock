import pandas as pd
import datetime
import requests
from requests.exceptions import ConnectionError
from bs4 import BeautifulSoup

# good: more robust when it comes to which market you want to trade in
# bad: it seems the data is around a week old?? (potentially to deter scrapers?)
def web_content_div(web_content, class_path):
    web_content_divide = web_content.find_all('div', {'class': class_path})
    try:
        spans = web_content_divide[0].find_all('span')
        texts = [span.get_text() for span in spans]
    except IndexError:
        texts = []
    return texts

def real_time_price(stock_code):
    url = 'https://finance.yahoo.com/quote/' + stock_code + '/'
    try:
        r = requests.get(url)
        web_content = BeautifulSoup(r.text, 'html.parser')
        texts = web_content_div(web_content, 'container svelte-aay0dk')
        print(texts)
        if texts:
            price, change = texts[0], texts[1]
        else:
            price, change = [], []
    except ConnectionError:
        price, change = [], []
    return price, change


print(real_time_price('NVDA'))
