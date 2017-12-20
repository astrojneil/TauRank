import matplotlib.pyplot as plt
import numpy as np
x = np.logspace(-5, 1, 50)
y = np.exp(-x)
plt.plot(x, y, marker = '.')
plt.xscale('log')
fig = plt.gcf()
fig.savefig('testExp.png')

