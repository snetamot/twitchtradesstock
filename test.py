from google import real_time_price
from googlenothreads import real_time_price_no_threads
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
import matplotlib.pyplot as plt

# This test is for testing the runtime when trying to find the value of a stock price when using multiple possible urls
def test_time_save():
    start = time.time()
    print(f'Google: {real_time_price("GOOGL")}')
    print(f'Apple: {real_time_price("AAPL")}')
    print(f'Nvidia: {real_time_price("NVDA")}')
    print(f'Amazon: {real_time_price("AMZN")}')
    print(f'GameStop: {real_time_price("GME")}')
    end = time.time()
    print(f'Multithreading took:{end - start}')

    start = time.time()
    print(f'Google: {real_time_price_no_threads("GOOGL")}')
    print(f'Apple: {real_time_price_no_threads("AAPL")}')
    print(f'Nvidia: {real_time_price_no_threads("NVDA")}')
    print(f'Amazon: {real_time_price_no_threads("AMZN")}')
    print(f'GameStop: {real_time_price_no_threads("GME")}')
    end = time.time()
    print(f'No multithreading took:{end - start}')


def test_threading():
    current_stocks = {"GOOGL": 2, "AAPL": 4, "NVDA": 6, "AMZN": 8, "GME": 10}
    start = time.time()
    with ThreadPoolExecutor() as executor:
        future_to_total = {executor.submit(real_time_price, keys): keys for keys in current_stocks.keys()}
        for future in as_completed(future_to_total):
            print(future_to_total[future])
            print(current_stocks[future_to_total[future]]*future.result())
    end = time.time()
    print(end-start)

if __name__ == "__main__":
    #test_time_save()
    #test_threading()
    #s = input()
    #print(s)
    print("hello!")