import librosa
from flask import Flask
from bark_handler.main import x_correlation
from sirbarksalot.lib.scheduler import Scheduler
from sirbarksalot.listener.listen import Listener
from sirbarksalot.listener.specgram import save_specgram_to_file
import time


def make_filename(ext, ms):
    return "./clips/sample_{0}.{1}".format(ms, ext)


import logging

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
    score = max(x_correlation(data, y_find, mode='full', plot=True))

    # write it out
    if score > 0.18:
        _ms = "{0}".format(time.time()).split(".")[0]
        logger.info("{0}".format(_ms))
        _LISTEN.write_to_file(data, make_filename("wav", _ms))
        save_specgram_to_file(data, make_filename("png", _ms))

        send_message(score)

    return 0


app = Flask(__name__)

if __name__ == "__main__":
    scheduler = Scheduler(6, listen)
    scheduler.start()
    app.run(debug=True, port=5555)
    scheduler.stop()
    _LISTEN.stop_stream()
    _LISTEN.shutdown()
