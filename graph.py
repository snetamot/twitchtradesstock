# Want to make a candlestick graph that tracks
# the current stocks in inventory and the overall value of
# the account

from mplfinance.original_flavor import candlestick_ohlc
import matplotlib.animation as animation
from matplotlib.gridspec import GridSpec
import matplotlib.ticker as mticker
from google import real_time_price
import matplotlib.pyplot as plt
import pandas as pd
import threading
import twitch
import time
import math
import csv
import os


stock = ['NVDA', 'MSFT', 'AAPL', 'GOOGL']

fieldnames = ['x_val', 'price']

start_prices = {}


def store_stock_data(stock_code):
    x = 0
    with open(f'{stock_code}.csv', 'w') as csv_file_head:
        csv_writer = csv.DictWriter(csv_file_head, fieldnames=fieldnames)
        csv_writer.writeheader()
        csv_file_head.close()
        while 1:
            with open(f'{stock_code}.csv', 'a') as csv_file_append:
                #open the csv in append mode
                csv_writer = csv.DictWriter(csv_file_append, fieldnames=fieldnames)
                info = {
                    'x_val': x,
                    'price': real_time_price(stock_code)
                }
                #print(info)
                csv_writer.writerow(info)
                x += 1

def animate_stock(i, stock_code, ax):
    data = pd.read_csv(f'{stock_code}.csv')
    x = data['x_val']
    y = data['price']

    ax.cla()
    price = real_time_price(stock_code)
    if start_prices[stock_code] <= price:
        ax.plot(x, y, color='red')
    else:
        ax.plot(x, y, color='limegreen')

    ax.text(0.05, 0.75, f'{stock_code}: \\${price}', transform=ax.transAxes, fontsize=10)
    ax.get_xaxis().set_ticks([])
    ax.get_yaxis().set_ticks([])


if __name__ == '__main__':
    for elt in stock:
        start_prices[elt] = real_time_price(elt)
    #print(start_prices)
    fig = plt.figure()
    fig.patch.set_facecolor('lavenderblush')
    gs = fig.add_gridspec(4, 6)

    # Plot where the current stocks up and down
    ax1 = fig.add_subplot(gs[0:4, 0:4])
    ax1.get_xaxis().set_ticks([])
    ax1.get_yaxis().set_ticks([])
    ax1.set_facecolor("floralwhite")

    # NVDA
    ax2 = fig.add_subplot(gs[0, 4:6])
    ax2.get_xaxis().set_ticks([])
    ax2.get_yaxis().set_ticks([])
    ax2.set_facecolor("floralwhite")

    # MSFT
    ax3 = fig.add_subplot(gs[1, 4:6])
    ax3.get_xaxis().set_ticks([])
    ax3.get_yaxis().set_ticks([])
    ax3.set_facecolor("floralwhite")

    # AAPL
    ax4 = fig.add_subplot(gs[2, 4:6])
    ax4.get_xaxis().set_ticks([])
    ax4.get_yaxis().set_ticks([])
    ax4.set_facecolor("floralwhite")

    # GOOGL
    ax5 = fig.add_subplot(gs[3, 4:6])
    ax5.get_xaxis().set_ticks([])
    ax5.get_yaxis().set_ticks([])
    ax5.set_facecolor("floralwhite")

    nvda_thread = threading.Thread(target=store_stock_data, args=('NVDA',), daemon=True)
    nvda_thread.start()
    ani_nvda = animation.FuncAnimation(fig, animate_stock, fargs=(f'NVDA', ax2), frames=100
                                       , interval=1000, cache_frame_data=True)

    msft_thread = threading.Thread(target=store_stock_data, args=('MSFT',), daemon=True)
    msft_thread.start()
    ani_msft = animation.FuncAnimation(fig, animate_stock, fargs=(f'MSFT', ax3), frames=100
                                       , interval=1000, cache_frame_data=True)

    aapl_thread = threading.Thread(target=store_stock_data, args=('AAPL',), daemon=True)
    aapl_thread.start()
    ani_aapl = animation.FuncAnimation(fig, animate_stock, fargs=(f'AAPL', ax4), frames=100
                                       , interval=1000, cache_frame_data=True)

    googl_thread = threading.Thread(target=store_stock_data, args=('GOOGL',), daemon=True)
    googl_thread.start()
    ani_googl = animation.FuncAnimation(fig, animate_stock, fargs=(f'GOOGL', ax5), frames=100
                                        , interval=1000, cache_frame_data=True)

    time.sleep(1)
    plt.show()

    nvda_thread.join()
    msft_thread.join()
    aapl_thread.join()
    googl_thread.join()
