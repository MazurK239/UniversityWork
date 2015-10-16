#! /usr/local/bin/python
# coding: utf-8

import math
import sys

def Kepler_iter(M, e):
	E0 = -1
	E = M
	while abs(E - E0) > 0.0000000001:
		E0 = E
		E = M + e * math.sin(E0)
	return E


i_file_name = sys.argv[1]
o_file_name = sys.argv[2]

MU = 3.986004418 * 10**14
c = 299792458
OMEGA_dot_e = 7.2921151467 * 10**(-5)

i_file = open(i_file_name, 'r')
o_file = open(o_file_name, 'a')

SAT_NAME = i_file.readline() # Имя спутника
t_oe = float(i_file.readline()) # Эпоха
WN = float(i_file.readline()) # Неделя
e = float(i_file.readline()) # Эксцентриситет
A = float(i_file.readline()) ** 2 # Большая полуось орбиты
OMEGA0 = float(i_file.readline()) # Долгота восходящего узла на время эпохи
i0 = float(i_file.readline()) # Наклонение орбиты на время эпохи
omega = float(i_file.readline()) # Аргумент перигея
M0 = float(i_file.readline()) # Средняя аномалия на начало эпохи
delta_n = float(i_file.readline()) # Отклонение значения среднего движения
OMEGA_dot = float(i_file.readline()) # Скорость изменения долготы восходящего узла
IDOT = float(i_file.readline()) # Скорость изменения наклонения орбиты
C_uc = float(i_file.readline()) # Амплитуда квадратурной поправки аргумента широты
C_us = float(i_file.readline()) # Амплитуда синфазной поправки аргумента широты
C_rc = float(i_file.readline()) # Амплитуда квадратурной поправки радиуса орбиты
C_rs = float(i_file.readline()) # Амплитуда синфазной поправки радиуса орбиты
C_ic = float(i_file.readline()) # Амплитуда квадратурной поправки наклонения орбиты
C_is = float(i_file.readline()) # Амплитуда синфазной поправки наклонения орбиты
P = float(i_file.readline()) # Псевдодальность
t_obs = float(i_file.readline()) # Время наблюдений


n0 = math.sqrt(MU / A**3) # Среднее движение
t_em = t_obs - P/c # Время испускания сигнала
t = t_em - t_oe # Время от начала эпохи

if t < -302400:
	t += 604800
elif t > 302400:
	t -= 604800

n = n0 + delta_n # Исправленное среднее движение
M = M0 + n*t # Средняя аномалия
E = Kepler_iter(M, e) # Эксцентрическая аномалия
nu = 2 * math.atan(math.sqrt((1 + e) / (1 - e)) * math.tan(E/2)) # Истинная аномалия
fi = nu + omega # Аргумент широты

delta_u = C_us * math.sin(2*fi) + C_uc * math.cos(2*fi) # Поправка аргумента широты
delta_r = C_rs * math.sin(2*fi) + C_rc * math.cos(2*fi) # Поправка радиуса
delta_i = C_is * math.sin(2*fi) + C_ic * math.cos(2*fi) # Поправка наклонения

u = fi + delta_u # Исправленное значение аргумента широты
r = A * (1 - e * math.cos(E)) + delta_r # Исправленное значение радиуса
i = i0 + delta_i + IDOT * t # Исправленное значение наклонения

print u, r, i

X_orb = r * math.cos(u) # Координаты спутника в
Y_orb = r * math.sin(u) # орбитальной плоскости

OMEGA = OMEGA0 + (OMEGA_dot - OMEGA_dot_e) * t - OMEGA_dot_e * t_oe # Исправленная долгота восходящего узла

X = X_orb * math.cos(OMEGA) - Y_orb * math.cos(i) * math.sin(OMEGA) # Координаты спутника
Y = X_orb * math.sin(OMEGA) + Y_orb * math.cos(i) * math.cos(OMEGA) # в земной
Z = Y_orb * math.sin(i)                                             # системе координат

o_file.write(SAT_NAME)
o_file.write(str(X) + '\n')
o_file.write(str(Y) + '\n')
o_file.write(str(Z) + '\n')
o_file.write(str(P) + '\n')
