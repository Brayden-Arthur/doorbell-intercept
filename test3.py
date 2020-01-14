import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
import time

z = np.load("template.npy")
t = np.load("correlate_negative.npy")

t1 = time.time()
l=[]
for i in np.arange(0, t.shape[0], 150):
    c_array = np.zeros((z.shape[0], 2))
    c_array[:, 0] = z
    st = i
    fn = min(i + z.shape[0], t.shape[0])
    c_array[0:(fn - st), 1] = t[st:fn]
    corr_array = np.corrcoef(c_array[::50,:], rowvar=False)
    l.append(corr_array[0,1])
l=np.array(l)
t2 = time.time()
print(t2-t1)
fig, ax = plt.subplots(figsize=(15, 4))
ax.plot(l, linewidth=1.9)
fig.savefig('corr_coefs.png')
