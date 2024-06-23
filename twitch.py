# Connect to twitch chat
# IRC bot reads all messages
import socket
import re
from google import real_time_price
from codes import get_current_codes
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

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
run_switch = 1

def total_stock_value():
    #this is the only function that can touch the cash in stocks global variable so no need to lock it for now
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
        time.sleep(15)

def buy(stock_code):
    global liquid_cash
    price = real_time_price(stock_code)
    if price and liquid_cash > price:
        cash_lock.acquire()
        current_stocks_lock.acquire()
        liquid_cash -= price
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
        print("sell finished")
    return

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
    token = 'oauth:p4vhb6kukc2390znfhlv5pshwn5afz'  # CHANGE BEFORE PUBLISH
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
                # check if message is !buy or !sell and add to queue of instructions
                if instr[0] in commands and nyse_and_nasdaq[instr[1]]:
                    instruction_lock.acquire()
                    instr_queue.append(instr)
                    instruction_lock.release()
                    #print(instr_queue)
            except AttributeError:
                print("Initial connection messages")


if __name__ == "__main__":
    with open('NYSE&NASDAQ.txt', 'r') as code_file:
        for code in code_file.read():
            nyse_and_nasdaq[code] = 1
    code_file.close()
    print('All NYSE and NASDAQ stocks updated!')
    while run_switch:
        #print("hello")
        s = input()
        if s == "start":
            # the daemon argument lets these threads automatically exit when we quit from this
            twitch_thread = threading.Thread(target=connect_to_chat, daemon=True)
            instr_thread = threading.Thread(target=fill_instructions, daemon=True)
            stock_value_thread = threading.Thread(target=total_stock_value, daemon=True)
            twitch_thread.start()
            time.sleep(1)
            instr_thread.start()
            time.sleep(1)
            stock_value_thread.start()
        elif s == "quit":
            run_switch = 0
            print("Exiting...")
            break
    quit()
