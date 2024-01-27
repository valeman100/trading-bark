import bs4 as bs
import requests
import yfinance as yf
from random import randrange


def get_tickers_from_SP500():
    # Scrape the Wikipedia page related to the S&P500
    resp = requests.get('http://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    soup = bs.BeautifulSoup(resp.text, 'lxml')
    table = soup.find('table', {'class': 'wikitable sortable'})
    tickers = []

    # Import stock tickers
    for row in table.findAll('tr')[1:]:
        ticker = row.findAll('td')[0].text
        tickers.append(ticker)

    # Store stock tickers into a list
    tickers = [s.replace('\n', '') for s in tickers]

    return tickers

