import time
import warnings
from bark_handler.sirbarksalot.lib.scheduler import Scheduler
from bark_handler.sirbarksalot.listener.listen import Listener
from db_handler import get_tickers_from_SP500
from functions import extract_random_stock, random_picker
import librosa
from flask import Flask
from bark_handler.main import x_correlation
import logging

warnings.filterwarnings('ignore')
stocks_list = get_tickers_from_SP500()

logging.basicConfig()
logger = logging.getLogger("sirbarksalot")
logger.setLevel('INFO')

y_find, _ = librosa.load('bark_handler/single_bark.wav')

_LISTEN = Listener()
_LISTEN.start_stream()


def send_message(corr):
    msg = {'text': 'woof woof: {:.4f}'.format(corr)}
    print(msg)


def listen():
    # get some data
    data = _LISTEN.record()

    # make a spectrogram
    score = max(x_correlation(data, y_find, mode='full', plot=False))

    # write it out
    if score > 0.18:
        send_message(score)
        print(f'\nYour dog is barking! Hurry up to buy this stock!\n')
        stock_value, stock = extract_random_stock(stocks_list, print_info=True)
        print(f'\nLast "{stock.info["shortName"]}" closure value: $ {stock_value:.2f}\n')
    else:
        ticker = random_picker(stocks_list)
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
