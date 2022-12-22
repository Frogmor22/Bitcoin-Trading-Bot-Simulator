from time import sleep
from binance import Client #good

# Starting values
btc_wallet = 0
usd_wallet = 500

api_key = 'API_KEY'
api_secret = 'API_SECRET'
client = Client(api_key, api_secret)


def btc_price(file): #Fetches BTC Price using binance api and writes it to a file
    btc_price = client.get_symbol_ticker(symbol="BTCUSDT")
    btc_price = str(btc_price)
    price = []
    for x in btc_price:
        if x == '.':
            break
        if x.isnumeric():
            price.append(x)
    price = ''.join(price)
    price = str(price)
    with open(file, 'r+') as th:
        th.read().split('\n')
        th.write(price + '\n')
    return (price)


def wma(file): # Reads BTC Price history from file (price_history) and calculates the weighted moving average
    with open(file, 'r') as ma:
        file_contents = ma.read().split('\n')
    if len(file_contents) > 43:
        five = int(file_contents[len(file_contents) - 42])
        four = int(file_contents[len(file_contents) - 32])
        three = int(file_contents[len(file_contents) - 22])
        two = int(file_contents[len(file_contents) - 12])
        one = int(file_contents[len(file_contents) - 2])
        wma = (five * 1 / 15) + (four * 2 / 15) + (three * 3 / 15) + (two * 4 / 15) + (one * 5 / 15)
        return (wma)
    else:
        return 0


def changefive(file): # Reads BTC Price history from file (price_history) and calculates the 5-minute change.
    with open(file, 'r') as cf:
        file_contents = cf.read().split('\n')
    if len(file_contents) > 11:
        change_five = (float(price) - float(file_contents[len(file_contents) - 11])) / float(
            file_contents[len(file_contents) - 11]) * 100
        return change_five
    else:
        return 0


def buy(): # Converts value from usd_wallet into btc_wallet using btc price as exchange rate, includes 0.1% trading fee.
    global usd_wallet
    global btc_wallet
    btc_buy = (float(usd_wallet) - (float(usd_wallet) * 0.001)) / float(price)
    if float(change_five) > 0.05 and (float(price) <= (weighted_moving_average + weighted_moving_average * 0.02)):
        btc_wallet = btc_buy
        usd_wallet = 0
        with open('buy_history.txt', 'r+') as bh: # Writes purchase price to file (buy_history)
            bh.read().split('\n')
            bh.write(str(int(price))+'\n')
        print('BOUGHT BTC AT: $', price)


def sell(): # Converts value from btc_wallet to usd_wallet using btc price as exchange rate, includes 0.1% trading fee.
    global usd_wallet
    global btc_wallet
    btc_sell = (float(btc_wallet) - (float(btc_wallet) * 0.001)) * float(price)
    if float(profit) >= 0.5:  # Sell at Profit
        usd_wallet = btc_sell
        btc_wallet = 0
        print('SOLD AT PROFIT')
    if float(profit) <= -0.5:  # Sell at Loss
        usd_wallet = btc_sell
        btc_wallet = 0
        print('SOLD AT LOSS')


def gainloss(file): # Reads from file (buy_history) and calculates profit since last purchase.
    with open(file, 'r') as p:
        file_contents = p.read().split('\n')
    if file_contents[len(file_contents) - 2] == '':
        profit = 0
        return profit
    else:
        profit = (float(price) - float(file_contents[len(file_contents) - 2])) / float(
            file_contents[len(file_contents) - 2]) * 100
        return profit


while True:

    price = btc_price('price_history.txt') # fetch price
    price = float(price)
    weighted_moving_average = wma('price_history.txt') # calculates weighted moving average
    change_five = changefive('price_history.txt') # calculates 5 minute change

    if btc_wallet > 0:
        profit = gainloss('buy_history.txt') # sell bitcoin based on parameters
        sell()
    else:
        buy() # buy bitcoin based on parameters

    # Output
    print('___')
    print('BTC Wallet:', btc_wallet, 'USD: $', (btc_wallet * price))
    print('USD Wallet: $', usd_wallet)
    print('')
    if btc_wallet > 0:
        print('Profit:', gainloss('buy_history.txt'), '%')
    print('BTC Price: $', price)
    print('Weighted Moving Average', weighted_moving_average, '%')
    print('Five Minute Change:', change_five, '%')

    sleep(30)
