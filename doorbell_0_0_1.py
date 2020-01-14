import shutil
import subprocess

import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
import time
import glob
from rtlsdr import RtlSdr
from scipy.signal import medfilt

flist = glob.glob('./ring/*.wav')
print(flist)
sdr = RtlSdr()

# configure device
sdr.sample_rate = 2.3e5  # Hz
sdr.center_freq = 433e6  # Hz
sdr.freq_correction = 1  # PPM
sdr.gain = 80

z = np.load("template.npy")
N = 2 ** 16
M = 2
y = np.zeros(N * M, dtype=np.complex_)


def listen(y, N, M):
    for i in range(M):
        idx = np.arange(N) + i * N
        x = np.array(sdr.read_samples(N))
        y[idx] = x
    y = np.absolute(y)
    y = medfilt(y, 5)
    y = (y > 0.3) + 1e-3
    return y


def find_signals(c_array, sig, every_n_corr=150, threshold=0.6, file_name='doorbell.wav'):
    for i in np.arange(0, sig.shape[0], every_n_corr):
        st = i
        fn = min(i + z.shape[0], sig.shape[0])
        c_array[0:(fn - st), 1] = sig[st:fn]
        corr_array = np.corrcoef(c_array[::50, :], rowvar=False)[0, 1]
        if corr_array > threshold:
            subprocess.run(['aplay', f'./{file_name}'])
            break


# t = np.load("correlate_negative.npy")

while True:
    sig = listen(y, N, M)
    c_array = np.zeros((z.shape[0], 2))
    c_array[:, 0] = z
    f = np.random.choice(flist)
    find_signals(c_array, sig, threshold=0.6, file_name=f)
