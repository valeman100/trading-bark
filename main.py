import warnings

from matplotlib import pyplot as plt

from bark_handler.sirbarksalot.lib.scheduler import Scheduler
from bark_handler.sirbarksalot.listener.listen import Listener
from db_handler import get_tickers_from_SP500, get_tickers_from_xlsx
from functions import extract_random_stock, random_picker, send_message
import librosa
from flask import Flask
from bark_handler.main import x_correlation
import logging

warnings.filterwarnings('ignore')
import sys


class DevNull:
    def write(self, msg):
        pass


sys.stderr = DevNull()
# stocks_list = get_tickers_from_SP500()
stocks_list = get_tickers_from_xlsx()

logging.basicConfig()
logger = logging.getLogger("sirbarksalot")
logger.setLevel('INFO')

y_find, _ = librosa.load('real_data/single_bark.wav')

_LISTEN = Listener()
_LISTEN.start_stream()


def listen():
    # get some data
    data = _LISTEN.record()
    # data, _ = librosa.load('real_data/bark2.wav')
    # plt.plot(data)
    # plt.show()

    # make a spectrogram
    score = max(x_correlation(data, y_find, mode='full', plot=False))

    # write it out
    if score > 0.28:
        send_message(score)
        stock_value, ticker, stock = extract_random_stock(stocks_list, print_info=True)
        print(f'\nLast "{ticker}" closure value: $ {stock_value:.2f}\n')
    else:
        i = random_picker(stocks_list)
        if isinstance(stocks_list, dict):
            ticker = stocks_list["ACT Symbol"][i]
        else:
            ticker = stocks_list[i]
        print(f'\nRandomly selected stock: {ticker}, correlation score: {score:.4f}')

    del data

    return 0


app = Flask(__name__)

if __name__ == "__main__":
    scheduler = Scheduler(1, listen)
    scheduler.start()
    app.run(debug=True, port=5555, use_reloader=False)
    scheduler.stop()
    _LISTEN.stop_stream()
    _LISTEN.shutdown()

print('done')
