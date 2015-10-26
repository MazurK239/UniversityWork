#! usr/local/bin/python
# coding:utf-8

from MaxMin_eigenvalues import matrix
import math
import numpy as np

def givens(A, p, q):
	N = len(A[0])
	cos = A[p-1][p] / math.sqrt(A[p-1][p]**2 + A[p-1][q]**2)
	sin = A[p-1][q] / math.sqrt(A[p-1][p]**2 + A[p-1][q]**2)
	C = np.copy(A)
	for i in range(N):
		C[i][p] = cos * A[i][p] + sin * A[i][q]; C[p][i] = C[i][p]
		C[i][q] = -sin * A[i][p] + cos * A[i][q]; C[q][i] = C[i][q]
	C[p][p] = cos**2 * A[p][p] + 2 * cos * sin * A[p][q] + sin**2 * A[q][q]
	C[q][q] = sin**2 * A[p][p] - 2 * cos * sin * A[p][q] + cos**2 * A[q][q]
	C[p][q] = (cos**2 - sin**2) * A[p][q] + cos * sin * (A[q][q] - A[p][p]); C[q][p] = C[p][q]
	return C

def vedEl(A, t):
	N = len(A[0])
	C = A - t * np.eye(N)
	alpha = [C[0][0]]
	for k in range(1, N):
		alpha.append(C[k][k] - C[k-1][k]**2 / alpha[k-1])
	return alpha
	
def numNeg(lst):
	return sum([1 for item in lst if item < 0])

def findInitT(Ar):
	t = 0
	while (numNeg(vedEl(Ar, t)) > 0):
		t -= 1
	return t
	
def findLam(Ar, a, b, i):
	if (abs(a - b) <= eps): return a
	half = (a + b) / 2
	if (numNeg(vedEl(Ar, half)) == i):
		return findLam(Ar, a, half, i)
	else:
		return findLam(Ar, half, b, i)

	
s = 10
eps = 0.0000001

Ar = matrix(s, 1, 1, 1)

for p in range(1, s-1):
	for q in range(p+1, s):
		Ar = givens(Ar, p, q)
		
t0 = findInitT(Ar)

lam = []
for i in range(1, s+1):
	t = t0
	while (numNeg(vedEl(Ar, t)) != i):
		t += 0.1
	lam.append(findLam(Ar, t0, t, i))
	t0 = t
	
print [float("{0:.8f}".format(item)) for item in lam]
print np.linalg.eigvalsh(Ar)
