# Want to make a candlestick graph that tracks
# the current stocks in inventory and the overall value of
# the account

import matplotlib.animation as animation
from google import real_time_price
import matplotlib.pyplot as plt
import threading
import twitch
import time


stock = ['NVDA', 'MSFT', 'AAPL', 'GOOGL']
start_prices = {}

#Dictionary of dictionaries
stock_data = {code: {'x_val': [], 'price': []} for code in stock}

cash_data = {"liquid": {"x_val": [], 'amount': []}, "stock": {"x_val": [], "amount": []}}

def store_stock_cash_data():
    x = 0
    while True:
        cash_data["stock"]["x_val"].append(x)
        cash_data["stock"]["amount"].append(twitch.cash_in_stocks)
        x += 1
        time.sleep(1)

def store_liquid_cash_data():
    x = 0
    while True:
        cash_data["liquid"]["x_val"].append(x)
        cash_data["liquid"]["amount"].append(twitch.liquid_cash)
        x += 1
        time.sleep(1)

def animate_cash(i, ax):
    x1 = cash_data["liquid"]["x_val"]
    y1 = cash_data["liquid"]["amount"]

    x2 = cash_data["stock"]["x_val"]
    y2 = cash_data["stock"]["amount"]
    ax.cla()
    ax.plot(x1, y1, color='cyan')
    ax.plot(x2, y2, color='purple')
    ax.text(.05, .45, f'Cash in liquid: ${twitch.liquid_cash}\nCash in stocks: ${twitch.cash_in_stocks}'
            , transform=ax.transAxes, fontsize=10)
    ax.get_xaxis().set_ticks([])
    ax.get_yaxis().set_ticks([])


def store_stock_data(stock_code):
    x = 0
    while True:
        price = real_time_price(stock_code)
        stock_data[stock_code]['x_val'].append(x)
        stock_data[stock_code]['price'].append(price)
        x += 1
        time.sleep(1)

def animate_stock(i, stock_code, ax):
    x = stock_data[stock_code]['x_val']
    y = stock_data[stock_code]['price']
    #clear
    ax.cla()
    price = y[-1]
    if start_prices[stock_code] <= price:
        ax.plot(x, y, color='red')
    else:
        ax.plot(x, y, color='limegreen')

    ax.text(0.05, 0.75, f'{stock_code}: ${price}', transform=ax.transAxes, fontsize=10)
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

    liquid_cash_thread = threading.Thread(target=store_liquid_cash_data, daemon=True)
    liquid_cash_thread.start()

    stock_cash_thread = threading.Thread(target=store_stock_cash_data, daemon=True)
    stock_cash_thread.start()

    ani_total_cash = animation.FuncAnimation(fig, animate_cash, fargs=(ax1,), frames=100
                                             , interval=1000, cache_frame_data=True)

    time.sleep(1)
    plt.show()

    nvda_thread.join()
    msft_thread.join()
    aapl_thread.join()
    googl_thread.join()
    liquid_cash_thread.join()
    stock_cash_thread.join()
