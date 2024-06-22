import pandas as pd
import datetime
import requests
from requests.exceptions import ConnectionError
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed

#market = 'NASDAQ'   # Change if you want to do a different market

def web_content_div(web_content, class_path):
    web_content_divide = web_content.find_all('div', {'class': class_path})
    try:
        spans = web_content_divide[0].find_all('span')
        texts = [span.get_text() for span in spans]
        #print(texts)
    except IndexError:
        texts = []
    return texts


def fetch_price_from_url(url):
    try:
        r = requests.get(url)
        r.raise_for_status()
        web_content = BeautifulSoup(r.text, 'html.parser')
        texts = web_content_div(web_content, 'AHmHk')
        if texts:
            return texts[0]
    except requests.ConnectionError:
        pass
    except requests.HTTPError:
        pass
    return None


def real_time_price_no_threads(stock_code):
    urls = [
        f'https://www.google.com/finance/quote/{stock_code}:NYSE',
        f'https://www.google.com/finance/quote/{stock_code}:NASDAQ'
    ]

    for url in urls:
        price = fetch_price_from_url(url)
        if price:
            return price

    return []
