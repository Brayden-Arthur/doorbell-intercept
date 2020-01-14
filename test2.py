import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import medfilt

z = np.load("test.npy")
left = 3388000
right = left + 85000
z = medfilt(z[left:right], 5)
fig, ax = plt.subplots(figsize=(15, 4))
ax.plot(z > 0.3, linewidth=1.9)
fig.savefig('test2.png')


np.save("correlate_negative.npy", z)
