# coding: utf-8
import math
import numpy as np
import Slozhna as sl
import matplotlib.pyplot as plt

alpha = 0.35
N = 5 # количество координатных функций
nodes = 20 # количество узлов в формуле Гаусса

def K(x,t):
	return math.log(1 + alpha*x*t)
	
def f(x):
	return math.log(2 + x)

leg_roots = sl.Leg_roots(nodes)	
prav = []
for i in range(N):
	tmp = [f(root) * sl.Leg_pol(i,root) for root in leg_roots]
	prav.append(sl.Gauss_integr_ar(nodes, tmp))


A = np.empty([N,N])

for i in range(N):
	for k in range(i,N):
		ar = []
		for root1 in leg_roots:
			tmp = [K(root1, root) * sl.Leg_pol(k+1, root) for root in leg_roots]
			ar.append(-sl.Gauss_integr_ar(nodes, tmp) * sl.Leg_pol(i+1, root1))
		A[i][k] = sl.Gauss_integr_ar(nodes, ar)
	A[i][i] += 2 / float(2*i+3)
	for k in range(i):
		A[i][k] = A[k][i]

c = np.linalg.solve(A, prav)

u = []
for i in range(nodes):
	pols = sl.Leg_pol_list(N, leg_roots[i])
	u.append(sum([c[k]*pols[k+1] for k in range(N)]))
	
#u1 = [sum([c[k]*sl.Leg_pol(k+1, idx/100.0) for k in range(N)]) for idx in range(-100,101)]

print
print A

#plt.figure(1)
#plt.plot(leg_roots, u)
#plt.plot([i/100.0 for i in range(-100, 101)], u1)
#plt.show()
