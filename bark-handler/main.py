# read in the wav file and get the sampling rate
import numpy as np
from scipy import signal
from scipy.io import wavfile
from matplotlib import pyplot as plt

sampling_freq, audio = wavfile.read('single_bark.wav')
ref_sampling_freq, ref_audio = wavfile.read('sample_bark.wav')

# save ndarray as png
plt.plot(audio[:, 0])
plt.plot(ref_audio[:, 0])
plt.show()
# plt.savefig('audio.png')

# read in the reference image file
# reference = plt.imread('reference_audio.png')

# cross correlate the image and the audio signal
corr = signal.correlate(audio[:, 0], ref_audio[:, 0], method='fft', mode='full')/len(audio[:, 0])

clock = np.arange(64, len(corr), 1280)
# plot the cross correlation signal
plt.plot(clock, corr[clock], 'bo')
plt.show()



print('done')
