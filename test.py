from rtlsdr import RtlSdr
import numpy as np
import matplotlib.pyplot as plt
import timeit


sdr = RtlSdr()

# configure device
sdr.sample_rate = 2.3e5  # Hz
sdr.center_freq = 433e6  # Hz
sdr.freq_correction = 1  # PPM
sdr.gain = 80

N = 2 ** 18
M = 24
y = np.zeros(N * M, dtype=np.complex_)
print(N * M / sdr.sample_rate)


def listen(y):

    for i in range(M):
        idx = np.arange(N) + i * N
        x = np.array(sdr.read_samples(N))
        y[idx] = x
    return y


y = listen(y)
fig, ax = plt.subplots()
ax.plot(np.absolute(y))
fig.savefig('test.png')

np.save("test.npy", np.absolute(y))
