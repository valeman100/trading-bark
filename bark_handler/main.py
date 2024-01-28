import librosa
import numpy as np
from scipy import signal
from matplotlib import pyplot as plt

# y_fake, sr_within = librosa.load('fake.wav', sr=None)
# y_within, sr_within = librosa.load('sample_bark.wav')
# y_find, _ = librosa.load('single_bark.wav')


def x_correlation(x, y, mode='full', plot=True):
    N = max(len(x), len(y))
    n = min(len(x), len(y))

    if N == len(y):
        lags = np.arange(-N + 1, n)
    else:
        lags = np.arange(-n + 1, N)
    c = signal.correlate(x / np.std(x), y / np.std(y), mode)

    if plot:
        # plt.plot(x)
        # plt.plot(y)
        plt.plot(lags, c / n)
        plt.show()

    return c / n


# corr = x_correlation(y_within, y_find, mode='full', plot=True)
# corr = x_correlation(y_fake, y_find, mode='full', plot=True)

# print('done')
