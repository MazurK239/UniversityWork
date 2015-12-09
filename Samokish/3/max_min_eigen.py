#! usr/local/bin/python
# coding: utf-8

###
# Данная программа находит наибольшее и наименьшее (не по модулю)
# Собственные числа матрицы, заданной методом matrix.
# Программа использует простейший степенной метод со сдвинутой матрицей
###

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
		X = np.dot(matr, map(lambda item: item / X[0], X))
	return X[0]

def min_eigVal(matr):
	N = len(matr[0])
	X = np.ones([N])
	X0 = np.zeros([N])
	while (abs(X[0] - X0[0]) > 0.00000001):
		X0 = X
		X = np.linalg.solve(matr, map(lambda item: item / X[0], X))
	return 1 / X[0]


Ar = matrix(4, 1, 1, 1)
print np.linalg.eigvalsh(Ar)

M = max_eigVal(Ar)
Ar += M * np.eye(4)

print max_eigVal(Ar) - M
print min_eigVal(Ar) - M
