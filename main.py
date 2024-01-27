# select a random row from the db whenever the bark detector detects a bark

import time
import warnings
from db_handler import get_tickers_from_SP500

from functions import extract_random_stock, random_picker

warnings.filterwarnings('ignore')

stocks_list = get_tickers_from_SP500()


def bark_detector():
    return True


while bark_detector():  # not

    # stock_value, stock = extract_random_stock(stocks_list, print_info=True)
    ticker = random_picker(stocks_list)
    time.sleep(2)

stock_value, stock = extract_random_stock(stocks_list, print_info=True)
print(f'\nLast "{stock.info["shortName"]}" closure value: $ {stock_value:.2f}')
time.sleep(10)

print('done')
