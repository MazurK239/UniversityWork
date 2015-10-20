#! usr/local/bin/python
# coding: utf-8

import math
import numpy as np

def matrix(N, a, d, e):
	ar = np.empty([N, N])
	for i in range(N):
		for k in range(N):
			ar[i][k] = math.sqrt(a**2 + (i + k + 2)**2) if (i != k) else math.sqrt(a**2 + 2 * (i+1)**2) + 1.0 / (d + e * (i+1)**2)
	return ar

def max_eigVal(matr):
	N = len(matr[0])
	X = [1 for dummy_idx in range(N)]
	X0 = [0 for dummy_idx in range(N)]
	while (abs(X[0] - X0[0]) > 0.00000001):
		X0 = X
		X = np.dot(matr, map(lambda item: item / X0[0], X))
	return X[0]

def min_eigVal(matr):
	N = len(matr[0])
	


Ar = matrix(2, 1, 1, 1)
print max(np.linalg.eigvalsh(Ar)), max_eigVal(Ar)
