import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed


def web_content_div(web_content, class_path):
    web_content_divide = web_content.find_all('div', {'class': class_path})
    try:
        #find the first span from the above div
        spans = web_content_divide[0].find_all('span')
        texts = [span.get_text() for span in spans]
    except IndexError:
        texts = []
    return texts

def fetch_from_url(url):
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

#multithreaded! it's ~30% faster on average! yippee!
def real_time_price(stock_code):

    #Add or remove markets here!
    urls = [f'https://www.google.com/finance/quote/{stock_code}:NASDAQ',
            f'https://www.google.com/finance/quote/{stock_code}:NYSE']

    with ThreadPoolExecutor() as executor:
        future_to_url = [executor.submit(fetch_from_url, url) for url in urls]

        for future in as_completed(future_to_url):
            price = future.result()
            if price:
                return float(price[1:])
    # if not found return empty list
    return []
