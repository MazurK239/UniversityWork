#! usr/local/bin/python
# coding: utf-8

###
# Программа численно решает линейное неоднородное дифференциальное
# уравнение второго порядка с граничными условиями третьего типа.
# Программа использует разностный метод или метод сеток.
# y'' + p(x) * y' + q(x) * y = f(x)
# y'(a) = alpha * y(a) + A ; y'(b) = beta * y(b) + B
# 
# В качестве первых двух аргументов программе подается промежуток
# изменения х, третий аргумент - количество узлов в сетке интегрирования.
# Последний аргумент - файл, в который будет производиться вывод результатов.
# Параметры уравнения (p(x), q(x), f(x), alpha, A, beta, B) задаются внутри программы.
###

import math
import sys
import three_diag as td
import matplotlib.pyplot as plt

aa = float(sys.argv[1])
bb = float(sys.argv[2])
n = int(sys.argv[3])
output_f_name = sys.argv[4]

out_file = open(output_f_name, 'w')

def p(x):
	return x + 1 / (1 + x)

def q(x):
	return math.sqrt(1 + x**2)

def f(x):
	return 1 - x**2

alpha = 0
A = 0
beta = -2
B = 1

h = (bb - aa) / n

a = []
b = []
c = []
d = []

a.append(0)
b.append(1 / h + p(aa) / 2 - q(aa) * h / 2 + alpha)
c.append(1 / h + p(aa) / 2)
d.append(A + f(aa) * h / 2)

for k in range(1, n):
	x_k = aa + h * k
	a.append(1 / h**2 - p(x_k) / (2 * h))
	b.append(2 / h**2 - q(x_k))
	c.append(1 / h**2 + p(x_k) / (2 * h))
	d.append(f(x_k))

a.append(p(bb) / 2 - 1 / h)
b.append(p(bb) / 2 - 1 / h + q(bb) * h / 2 + beta)
c.append(0)
d.append(B - f(bb) * h / 2)

y, alphak, betak = td.solution(a, b, c, d)

for idx in range(n+1):
	out_file.write('y_' + str(idx) + ' = ' + str(y[idx]) + '\n')
out_file.write('------------------------------------' + '\n')
for idx in range(n+1):
	out_file.write('a_' + str(idx) + ' = ' + str(a[idx]) + '\n')
out_file.write('------------------------------------' + '\n')
for idx in range(n+1):
	out_file.write('b_' + str(idx) + ' = ' + str(b[idx]) + '\n')
out_file.write('------------------------------------' + '\n')
for idx in range(n+1):
	out_file.write('c_' + str(idx) + ' = ' + str(c[idx]) + '\n')
out_file.write('------------------------------------' + '\n')
for idx in range(n+1):
	out_file.write('d_' + str(idx) + ' = ' + str(d[idx]) + '\n')
out_file.write('------------------------------------' + '\n')
for idx in range(n+1):
	out_file.write('alpha_' + str(idx) + ' = ' + str(alphak[idx]) + '       beta_' + str(idx) + ' = ' + str(betak[idx]) + '\n')

# plt.plot([aa + h * k for k in range(n+1)], y)
# plt.axis([0,1,-6,0])
# plt.show()
