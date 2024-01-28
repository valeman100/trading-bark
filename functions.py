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

    # plt.show()


def print_stock_info(stock):
    print(stock.earnings_dates.dropna(subset=['EPS Estimate']))

    print("\nLatest news:")
    for news in stock.news:
        print(news['title'])


def random_picker(stocks_list):
    i = randrange(len(stocks_list))
    random_stock = stocks_list[i]

    return random_stock


def extract_random_stock(stocks_list, print_info=False):
    ticker = random_picker(stocks_list)

    start_date = '2000-01-01'
    end_date = datetime.now().strftime("%Y-%m-%d")

    stock = yf.Ticker(ticker)
    data = stock.history(start=start_date, end=end_date, auto_adjust=True)

    last_stock_value = data['Close'][-1]

    if print_info:
        print_stock_info(stock)
        plot_history(data, ticker)

    return last_stock_value, stock

