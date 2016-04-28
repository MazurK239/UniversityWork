import math
import numpy as np
import random
import matplotlib.pyplot as plt

N = 460
d_t = 1
nu1 = 0.2
nu2 = 0.15
A1 = 1
A2 = 1
fi1 = 0
fi2 = 0
x = []

for k in range(N/2):
	x.extend([A1 * math.cos(2 * math.pi * nu1 * d_t * k - fi1) + A2 * math.cos(2 * math.pi * nu2 * d_t * k - fi2)] * 2)

p = math.ceil(math.log(N,2))
N2 = int(2**(p+1))

X = np.fft.fft(x, N2) 
D = [((X[j].real)**2 + (X[j].imag)**2) / N**2 for j in range(N2/2 + 1)] 

plt.subplot(211)
plt.plot([d_t * k for k in range(N)], x)

plt.subplot(212)
plt.plot([j / float((N2 * d_t)) for j in range(N2/2 + 1)], D, 'k')
plt.show()
