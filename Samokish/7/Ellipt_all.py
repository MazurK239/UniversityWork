# coding: utf-8

import numpy as np

eps = .0000001
n = 10
h = 1./n

A = np.array([[((i*h)**2 + 1) / h**2 - i / 2. for i in range(n+1)] for k in range(2*n+1)])
B = np.array([[((k*h)**2 + 1) / h**2 + k / 2. for i in range(n+1)] for k in range(2*n+1)])
D = np.array([[((i*h)**2 + 1) / h**2 + i / 2. for i in range(n+1)] for k in range(2*n+1)])
C = np.array([[((k*h)**2 + 1) / h**2 - k / 2. for i in range(n+1)] for k in range(2*n+1)])
E = np.array([[2 / h**2 * ((i*h)**2 + (k*h)**2 + 2) for i in range(n+1)] for k in range(2*n+1)])
F = np.array([[(k*h * (i*h - 1))**2 for i in range(n+1)] for k in range(2*n+1)])

A[0] = [((i*h)**2 + 1) / (2*h) - i*h / 4 for i in range(n+1)]
D[0] = [((i*h)**2 + 1) / (2*h) + i*h / 4 for i in range(n+1)]
B[0] = [0 for i in range(n+1)]
C[0] = [1 / h for i in range(n+1)]
E[0] = [((i*h)**2 + 1) / h + 1 for i in range(n+1)]

U_next = np.array([[ -F[i][k] / E[i][k] for k in range(n+1)] for i in range (2*n+1)])
U = np.zeros([2*n+1,n+1])

def classic(ar, ar_next):
	iter = 0
	U = np.array(ar) ; U_next = np.array(ar_next)
	while (np.max(abs(U_next - U)) > eps):
		U = [[U_next[i][k] for k in range(n+1)] for i in range(2*n+1)]
		for i in range(n+1):
			U_next[i][0] = 0
			for k in range(1,n):
				U_next[i][k] = (A[i][k] * U[i-1][k] + B[i][k] * U[i][k-1] + C[i][k] * U[i][k+1] + D[i][k] * U[i+1][k] - F[i][k]) / E[i][k]
			U_next[i][n] = 1
		for i in range(n+1,2*n+1):
			for k in range(i-n):
				U_next[i][k] = 0
			U_next[i][i-n] = (i-n)*h
			for k in range(i-n+1,n):
				U_next[i][k] = (A[i][k] * U[i-1][k] + B[i][k] * U[i][k-1] + C[i][k] * U[i][k+1] + D[i][k] * U[i+1][k] - F[i][k]) / E[i][k]
			U_next[i][n] = 1
		iter += 1
	print 'Итераций:', iter
	print np.flipud(U_next)
	
def Zeydel(ar, ar_next):
	iter = 0
	U = np.array(ar) ; U_next = np.array(ar_next)
	while (np.max(abs(U_next - U)) > eps):
		U = [[U_next[i][k] for k in range(n+1)] for i in range(2*n+1)]
		for i in range(n+1):
			U_next[i][0] = 0
			for k in range(1,n):
				U_next[i][k] = (A[i][k] * U_next[i-1][k] + B[i][k] * U_next[i][k-1] + C[i][k] * U[i][k+1] + D[i][k] * U[i+1][k] - F[i][k]) / E[i][k]
			U_next[i][n] = 1
		for i in range(n+1,2*n+1):
			for k in range(i-n):
				U_next[i][k] = 0
			U_next[i][i-n] = (i-n)*h
			for k in range(i-n+1,n):
				U_next[i][k] = (A[i][k] * U_next[i-1][k] + B[i][k] * U_next[i][k-1] + C[i][k] * U[i][k+1] + D[i][k] * U[i+1][k] - F[i][k]) / E[i][k]
			U_next[i][n] = 1
		iter += 1
	print 'Итераций:', iter
	print np.flipud(U_next)
	
def upper_relax(ar, ar_next, omega, it=False):
	iter = 0
	U = np.array(ar) ; U_next = np.array(ar_next)
	while (np.max(abs(U_next - U)) > eps):
		U = [[U_next[i][k] for k in range(n+1)] for i in range(2*n+1)]
		for i in range(n+1):
			U_next[i][0] = 0
			for k in range(1,n):
				tmp = (A[i][k] * U_next[i-1][k] + B[i][k] * U_next[i][k-1] + C[i][k] * U[i][k+1] + D[i][k] * U[i+1][k] - F[i][k]) / E[i][k]
				U_next[i][k] = U[i][k] + omega * (tmp - U[i][k])
			U_next[i][n] = 1
		for i in range(n+1,2*n+1):
			for k in range(i-n):
				U_next[i][k] = 0
			U_next[i][i-n] = (i-n)*h
			for k in range(i-n+1,n):
				tmp = (A[i][k] * U_next[i-1][k] + B[i][k] * U_next[i][k-1] + C[i][k] * U[i][k+1] + D[i][k] * U[i+1][k] - F[i][k]) / E[i][k]
				U_next[i][k] = U[i][k] + omega * (tmp - U[i][k])
			U_next[i][n] = 1
		iter += 1
	if it:
		return iter
	else:
		print 'Итераций:', iter
		print np.flipud(U_next)
	
def omega_search():
	omega0 = .95; omega = 1.
	while (omega <= 2):
		omega0 = omega
		omega += .01
		if (upper_relax(U, U_next, omega, True) - upper_relax(U, U_next, omega0, True) > 0):
			return omega0
	return omega
	
print 'Метод простых итераций:'
classic(U, U_next)
print
print 'Метод Зейделя:'
Zeydel(U, U_next)
print
print 'Метод верхней релаксации:'
omega = omega_search()
print omega
upper_relax(U, U_next, omega)
			
