#! usr/local/bin/python
# coding: utf-8

import matplotlib.pyplot as plt
import numpy as np
import math
import random

d_t = 1
N = 230
A1 = 1
fi_1 = 0
gamma = 0.50
alpha = 0.1
beta = 0.05
nu_1 = 0.1
X1 = 9.0
a = 0.25

sigma = math.sqrt(A1**2 / (2 * gamma))

x = [alpha + beta * d_t * k + A1 * math.cos(2*math.pi * nu_1 * d_t * k - fi_1) + sigma * random.gauss(0, 1) for k in range(N)]  # Ряд

xx = [x[k] - d_t * k / 20.0 for k in range(N)]  # Исключили линейный тренд

m = sum(xx) / N  # Мат. ожидание

x0 = map(lambda x_k: x_k - m, xx)  # Центрированный ряд

p = math.ceil(math.log(N,2))
N2 = int(2**(p+1))

X = np.fft.fft(x0, N2) 
D = [((X[j].real)**2 + (X[j].imag)**2) / N**2 for j in range(N2/2 + 1)]  # Периодограмма

sigma0 = math.sqrt(sum([item**2 for item in x0]) / (N - 1))

c_m = np.fft.irfft(np.abs(X)**2, N2)
c = map(lambda item: item.real / N, c_m[:N])

def smooth_period(N_star):
    W = [(1 - 2*a) + 2 * a * math.cos(math.pi * m / N_star) for m in range(N_star)]
    c_voln = [W[m] * c[m] for m in range(N_star)]

    D_voln_j = np.fft.fft(c_voln, N2)
    D_voln = map(lambda item: (2 * item.real - c_voln[0]) / N_star, D_voln_j[:N2/2 + 1])
    return D_voln

plt.figure(1)
plt.subplot(611)
plt.plot([d_t * k for k in range(N)], x)

plt.subplot(612)
plt.plot([d_t * k for k in range(N)], x0, 'r')

plt.subplot(613)
plt.plot([j / float((N2 * d_t)) for j in range(N2/2 + 1)], D, 'k', [j / float((N2 * d_t)) for j in range(N2/2 + 1)], [2 * sigma0**2 * X1 / N for dummy_idx in range(N2/2 + 1)], 'r--')

plt.subplot(614)
plt.plot([d_t * k for k in range(N)], c, 'r')

plt.subplot(615)
plt.plot([j / float((N2 * d_t)) for j in range(N2/2 + 1)], smooth_period(int(0.5 * N)), 'k')

plt.subplot(616)
plt.plot([j / float((N2 * d_t)) for j in range(N2/2 + 1)], smooth_period(int(0.1 * N)), 'k')
plt.show()
