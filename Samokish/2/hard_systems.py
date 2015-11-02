import math
import numpy as np
import matplotlib.pyplot as plt

eps = 0.000001
n = 10
h = 1.0 / n
gamma = (3 + math.sqrt(15)) / 6.0
A = 1
agh = A * gamma * h
znam = agh - 1

def findK1(x, y, z):
	tmp = ((1.5 - 2*agh/znam)*y + (agh/znam - 1)*A*z + agh/znam * ost(x + gamma*h)) / (1 + 2*gamma*h*agh/znam - 1.5*gamma*h)
	k0 = 0
	k = tmp
	while abs(k - k0) > eps:
		k0 = k
		k = tmp + math.sqrt((y + gamma*h*k)**2 + 1) / (1 + 2*gamma*h*agh/znam - 1.5*gamma*h)
	return k
	
def findK2(x, y, z, k1, l1):
	tmp = ((1.5 - 2*agh/znam)*(y + h*(1-2*gamma)*k1) + (agh/znam - 1)*A*(z + h*(1-2*gamma*l1)) + agh/znam * ost(x + (1-gamma)*h)) / (1 + 2*gamma*h*agh/znam - 1.5*gamma*h)
	k0 = 0
	k = tmp
	while abs(k - k0) > eps:
		k0 = k
		k = tmp + math.sqrt((y + h*(1-2*gamma)*k1 + gamma*h*k)**2 + 1) / (1 + 2*gamma*h*agh/znam - 1.5*gamma*h)
	return k
	
def ost(x):
	return x * math.sqrt(x**2 + 1)


y = []; y.append(10)
z = []; z.append(-1)

x = 0
for i in range(1, n + 1):
	x += h
	k1 = findK1(x, y[-1], z[-1])
	l1 = (2 * (y[-1] + gamma * h * k1) - A * z[-1] - ost(x + gamma*h)) / znam
	k2 = findK2(x, y[-1], z[-1], k1, l1)
	l2 = (2*y[-1] + 2*h*(1-2*gamma)*k1 + 2*h*gamma*k2 - A*z[-1] - A*h*(1-2*gamma)*l1 - ost(x + (1-gamma)*h)) / znam
	y.append(y[-1] + h / 2 * (k1 + k2))
	z.append(z[-1] + h / 2 * (l1 + l2))
	print 'y[', i, '] = ', y[-1], ';   z[', i, '] = ', z[-1]

plt.figure(1)
plt.subplot(211)
plt.plot([i/h for i in range(n+1)], y)
plt.subplot(212)
plt.plot([i/h for i in range(n+1)], z)
plt.show()
