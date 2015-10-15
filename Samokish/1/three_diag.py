#! usr/local/bin/python
# coding: utf-8

###
# Данная программа решает систему линейных уравнений,
# задающуюся трехдиагональной матрицей. Использует метод разностной прогонки.
# На вход функции solution(a, b, c, d) подаются:
# массивы a, b, c чисел, стоящих на диагоналях матрицы
# (b - главная диагональ) и массив d чисел, стоящих в правых частях уравнений.
# Возвращает данная функция вектор решений данной системы уравнений.
###

def solution(a, b, c, d):
	n = len(b) - 1
	y = [0]
	alpha = []
	beta = []
	alpha.append(c[0] / b[0])
	beta.append(-d[0] / b[0])
	for k in range(1, n + 1):
		alpha.append(c[k] / (b[k] - a[k] * alpha[k-1]))
		beta.append((a[k] * beta[k-1] - d[k]) / (b[k] - a[k] * alpha[k-1]))
		y.append(0)

	y[n] = beta[n]
	for k in range(n-1, -1, -1):
		y[k] = alpha[k] * y[k+1] + beta[k]

	return y, alpha, beta
