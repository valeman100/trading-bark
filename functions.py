from datetime import datetime
from random import randrange
import yfinance as yf
from matplotlib import pyplot as plt


def plot_history(data, ticker):
    data['Close'].plot(figsize=(10, 7))

    plt.title("Close Price of %s" % ticker, fontsize=16)
    plt.ylabel('Price', fontsize=14)
    plt.xlabel('Year', fontsize=14)
    plt.grid(which="major", color='k', linestyle='-.', linewidth=0.5)
    plt.savefig(f'{ticker}_history.png')

    plt.show()


def print_stock_info(stock):
    try:
        print(stock.earnings_dates.dropna(subset=['EPS Estimate']))
    except Exception:
        print("No earnings dates found")

    news = stock.news if stock.news else None
    if news:
        print("\nLatest news:")
        for new in news:
            print(new['title'])


def random_picker(stocks_list):
    if isinstance(stocks_list, dict):
        i = randrange(len(stocks_list["ACT Symbol"]))
    else:
        i = randrange(len(stocks_list))

    return i


def extract_random_stock(stocks_list, print_info=False):
    start_date = '2000-01-01'
    end_date = datetime.now().strftime("%Y-%m-%d")

    last_stock_value = []
    stock_name = None
    while not last_stock_value:
        i = random_picker(stocks_list)
        if isinstance(stocks_list, dict):
            ticker = stocks_list["ACT Symbol"][i]
            stock_name = stocks_list["Company Name"][i]
        else:
            ticker = stocks_list[i]

        stock = yf.Ticker(ticker)
        data = stock.history(start=start_date, end=end_date, auto_adjust=True)
        last_stock_value = data.get('Close').tolist()

    print(f'\nYour dog is barking! Hurry up to buy "{stock_name}"!\n')

    if print_info:
        print_stock_info(stock)
        # plot_history(data, ticker)

    return last_stock_value[-1], ticker, stock


def send_message(corr):
    msg = {'text': 'woof woof: {:.4f}'.format(corr)}
    print(msg)
