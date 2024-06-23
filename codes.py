import os
import requests
import json

# Based off of Robert's script: https://github.com/rreichel3/US-Stock-Symbols turned into python
# runs before you start, updates the

def fetch_and_save_tickers(url, txt_file):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:85.0) Gecko/20100101 Firefox/85.0'
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()

        tickers = [row['symbol'] for row in data['data']['rows']]

        with open(txt_file, 'w') as tf:
            for ticker in tickers:
                tf.write(f"{ticker}\n")

        replace_caret_with_dash(txt_file)
    else:
        print(f"Failed to fetch data from {url}")


def replace_caret_with_dash(file_path):
    with open(file_path, 'r') as file:
        content = file.read()

    content = content.replace('^', '-')

    with open(file_path, 'w') as file:
        file.write(content)


def combine_files(output_file, *input_files):
    with open(output_file, 'w') as outfile:
        for file_name in input_files:
            with open(file_name, 'r') as infile:
                outfile.write(infile.read())


def get_current_codes():
    nasdaq_url = "https://api.nasdaq.com/api/screener/stocks?tableonly=true&limit=25&offset=" \
                 "0&exchange=nasdaq&download=true"
    nyse_url = "https://api.nasdaq.com/api/screener/stocks?tableonly=true&limit=25&offset=0&exchange=nyse&download=true"

    nasdaq_txt_file = 'nasdaq_code.txt'
    nyse_txt_file = 'nyse_code.txt'
    combined_txt_file = 'NYSE&NASDAQ.txt'

    fetch_and_save_tickers(nasdaq_url, nasdaq_txt_file)
    fetch_and_save_tickers(nyse_url, nyse_txt_file)

    combine_files(combined_txt_file, nasdaq_txt_file, nyse_txt_file)
    os.remove('nasdaq_code.txt')
    os.remove('nyse_code.txt')
