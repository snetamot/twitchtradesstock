# Connect to twitch chat
# IRC bot reads all messages

from concurrent.futures import ThreadPoolExecutor, as_completed
from codes import get_current_codes
from google import real_time_price
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import threading
import socket
import time
import re

instr_queue = []
current_stocks = {}
nyse_and_nasdaq = {}
liquid_cash = 10000.00
cash_in_stocks = 0.00
commands = ["!buy", "!sell"]
regex = r'^:([^!]+)!.*:(.*)$'
# locks for the global variables and data structures
cash_lock = threading.Lock()
instruction_lock = threading.Lock()
current_stocks_lock = threading.Lock()
#Global run switch allows for concurrency
run_switch = 1

cash_data = {"liquid": {"x_val": [], 'amount': []}, "stock": {"x_val": [], "amount": []}}

stop_event = threading.Event()

def store_stock_cash_data():
    global cash_in_stocks
    x = 0
    while not stop_event.is_set():
        cash_data["stock"]["x_val"].append(x)
        cash_data["stock"]["amount"].append(cash_in_stocks)
        x += 1
        time.sleep(1)
        if len(cash_data["stock"]["x_val"]) > 150:
            cash_data["stock"]["x_val"] = cash_data["stock"]["x_val"][50:]
            cash_data["stock"]["amount"] = cash_data["stock"]["amount"][50:]

def store_liquid_cash_data():
    global liquid_cash
    x = 0
    while not stop_event.is_set():
        cash_data["liquid"]["x_val"].append(x)
        cash_data["liquid"]["amount"].append(liquid_cash)
        x += 1
        time.sleep(1)

def animate_cash(i, ax):
    global liquid_cash, cash_in_stocks
    #x1 = cash_data["liquid"]["x_val"]
    #y1 = cash_data["liquid"]["amount"]
    x2 = cash_data["stock"]["x_val"]
    y2 = cash_data["stock"]["amount"]
    ax.cla()
    #ax.plot(x1, y1, color='cyan')
    ax.plot(x2, y2, color='purple')
    ax.text(.05, .45, f'Cash in liquid: ${liquid_cash}\nCash in stocks: ${cash_in_stocks}',
            transform=ax.transAxes, fontsize=10)
    ax.get_xaxis().set_ticks([])
    ax.get_yaxis().set_ticks([0, 2500, 5000, 7500, 10000])

def total_stock_value():
    #this is the only function that edit the cash in stocks global variable so no need to lock it for now
    global cash_in_stocks, run_switch
    while run_switch:
        total = 0.00
        current_stocks_lock.acquire()
        with ThreadPoolExecutor() as executor:
            future_to_total = {executor.submit(real_time_price, keys): keys for keys in current_stocks.keys()}
            for future in as_completed(future_to_total):
                total += current_stocks[future_to_total[future]]*future.result()
        current_stocks_lock.release()
        print(f'Current total in account: {total}\n')
        cash_in_stocks = total
        time.sleep(2.5)

def buy(stock_code):
    global liquid_cash
    price = real_time_price(stock_code)
    if price and liquid_cash > price:
        cash_lock.acquire()
        current_stocks_lock.acquire()
        liquid_cash -= price
        #print(liquid_cash)
        if stock_code in current_stocks:
            current_stocks[stock_code] += 1
        else:
            current_stocks[stock_code] = 1
        current_stocks_lock.release()
        cash_lock.release()
    print(f'bought {stock_code}')
    return


def sell(stock_code):
    global liquid_cash
    if stock_code in current_stocks and current_stocks[stock_code] >= 1:
        print(f'selling {stock_code}')
        cash_lock.acquire()
        current_stocks_lock.acquire()
        price = real_time_price(stock_code)
        current_stocks[stock_code] -= 1
        print(f'sold {stock_code}')
        if not current_stocks[stock_code]:
            current_stocks.pop(stock_code)  #removes key if value is 0
        liquid_cash += price
        current_stocks_lock.release()
        cash_lock.release()
    return

# Threads end when the function returns
def fill_instructions():
    global run_switch
    while run_switch:
        #check if there's any instr in queue
        if instr_queue:
            instruction_lock.acquire()
            curr_instr = instr_queue.pop()
            instruction_lock.release()
            if curr_instr[0] == '!buy':
                #print(curr_instr[1])
                #print(type(curr_instr[1]))
                threading.Thread(target=buy, args=(curr_instr[1],)).start()
                #buy(curr_instr[1])
            elif curr_instr[0] == '!sell':
                #print(curr_instr)
                #print(curr_instr[1])
                threading.Thread(target=sell, args=(curr_instr[1],)).start()
                #sell(curr_instr[1])


def connect_to_chat():
    global run_switch
    print("Connecting to chat...")
    server = 'irc.chat.twitch.tv'
    port = 6667
    nickname = 'snebot'  # CHANGE BEFORE PUBLISH
    # Oauth token from here -> https://twitchapps.com/tmi/
    token = 'oauth:oe4mrpiibm2w8kbiz6tp4qi6rcdntd'  # CHANGE BEFORE PUBLISH
    channel = '#chattradesstock'  # CHANGE BEFORE PUBLISH

    twitch_sock = socket.socket()
    twitch_sock.connect((server, port))

    twitch_sock.send(f"PASS {token}\n".encode('utf-8'))
    twitch_sock.send(f"NICK {nickname}\n".encode('utf-8'))
    twitch_sock.send(f"JOIN {channel}\n".encode('utf-8'))

    while run_switch:
        # twitch sometimes sends a PING message
        # ensures that the bot is still there and awake
        # need to respond with a PONG message

        msg = twitch_sock.recv(512).decode('utf-8')
        if msg.startswith('PING'):
            twitch_sock.send("PONG\n".encode('utf-8'))

        else:
            # print(msg)
            # want to only take care of !buy and !sell right now
            # restrict message to be of format !buy/sell stock_code (amount?)
            match = re.search(regex, msg)
            try:
                #chatter_username = match.group(1)
                chatter_message = match.group(2)
                # print(f"{chatter_username}: {chatter_message}")
                instr = chatter_message.split()
                instr = instr[0:2]
                print(instr)
                # check if message is !buy or !sell and add to queue of instructions
                try:
                    if instr[0] in commands and nyse_and_nasdaq[instr[1]]:
                        instruction_lock.acquire()
                        instr_queue.append(instr)
                        instruction_lock.release()
                        #print(instr_queue)
                except KeyError:
                    pass
            except AttributeError:
                print("Initial connection messages")


if __name__ == '__main__':
    get_current_codes()
    with open('NYSE&NASDAQ.txt', 'r') as code_file:
        for code in code_file.readlines():
            code = code.strip()
            nyse_and_nasdaq[code] = 1
    code_file.close()
    #print(nyse_and_nasdaq)
    print('All NYSE and NASDAQ stocks updated!')

    twitch_thread = threading.Thread(target=connect_to_chat, daemon=True)
    instr_thread = threading.Thread(target=fill_instructions, daemon=True)
    stock_value_thread = threading.Thread(target=total_stock_value, daemon=True)
    twitch_thread.start()
    instr_thread.start()
    stock_value_thread.start()

    fig = plt.figure()
    fig.patch.set_facecolor('lavenderblush')
    gs = fig.add_gridspec(4, 4)

    # Plot where the current stocks up and down
    ax1 = fig.add_subplot(gs[0:4, 0:4])
    ax1.get_xaxis().set_ticks([])
    ax1.get_yaxis().set_ticks([])
    ax1.set_facecolor("floralwhite")

    liquid_cash_thread = threading.Thread(target=store_liquid_cash_data, daemon=True)
    stock_cash_thread = threading.Thread(target=store_stock_cash_data, daemon=True)

    liquid_cash_thread.start()
    stock_cash_thread.start()

    ani_total_cash = animation.FuncAnimation(fig, animate_cash, fargs=(ax1,), interval=1000, cache_frame_data=False)

    plt.show()
    quit()
