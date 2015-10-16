#! /usr/local/bin/python
# coding: utf-8

import orb_elements
from math import sin, cos, sqrt, atan, tan, degrees
import sys

def Kepler_iter(M, e):
	E0 = -1
	E = M
	while abs(E - E0) > 0.0000000001:
		E0 = E
		E = M + e * sin(E0)
	return E

def ref_frame_transfer(Type, geo_sys, abs_sys, s_time, em_time):
	omega = 0.7292115e-4
	S = s_time + omega * (em_time - 3 * 3600)
	if (Type == 1):
		abs_sys.append(geo_sys[0] * cos(S) - geo_sys[1] * sin(S))
		abs_sys.append(geo_sys[0] * sin(S) + geo_sys[1] * cos(S))
		abs_sys.append(geo_sys[2])
		abs_sys.append(geo_sys[3] * cos(S) - geo_sys[4] * sin(S) - omega * abs_sys[1])
		abs_sys.append(geo_sys[3] * sin(S) + geo_sys[4] * cos(S) + omega * abs_sys[0])
		abs_sys.append(geo_sys[5])
	elif (Type == -1):
		geo_sys.append(abs_sys[0] * cos(S) + abs_sys[1] * sin(S))
		geo_sys.append(-abs_sys[0] * sin(S) + abs_sys[1] * cos(S))
		geo_sys.append(abs_sys[2])

MU = 398600.4418

i_file_name = sys.argv[1]
i_file = open(i_file_name, 'r')

vect = [float(i_file.readline()) for dummy_idx in range(6)]
t_oe = float(i_file.readline()) # Эпоха
t_obs = float(i_file.readline()) # Время наблюдений
s_time = float(i_file.readline()) 

vect1 = []
ref_frame_transfer(1, vect, vect1, s_time, t_oe)

input_vect = orb_elements.elements_est(vect1[0:3], vect1[3:6])

e = input_vect[0] # Эксцентриситет
A = input_vect[1] # Большая полуось орбиты
OMEGA = input_vect[2] # Долгота восходящего узла на время эпохи
i = input_vect[3] # Наклонение орбиты на время эпохи
omega = input_vect[4] # Аргумент перигея
M0 = input_vect[5] # Средняя аномалия на начало эпохи

print 'e = ', e
print 'a = ', A
print 'i = ', degrees(i)
print 'OMEGA = ', degrees(OMEGA)
print 'omega = ', degrees(omega)
print 'M = ', degrees(M0)
print '-----------------------------'

n = sqrt(MU / A**3) # Среднее движение
t = t_obs - t_oe # Время от начала эпохи

if t < -302400:
	t += 604800
elif t > 302400:
	t -= 604800

M = M0 + n*t # Средняя аномалия
E = Kepler_iter(M, e) # Эксцентрическая аномалия
nu = 2 * atan(sqrt((1 + e) / (1 - e)) * tan(E/2)) # Истинная аномалия
u = nu + omega # Аргумент широты

r = A * (1 - e * cos(E)) # Радиусвектор

X_orb = r * cos(u) # Координаты спутника в
Y_orb = r * sin(u) # орбитальной плоскости

X = X_orb * cos(OMEGA) - Y_orb * cos(i) * sin(OMEGA) # Координаты спутника
Y = X_orb * sin(OMEGA) + Y_orb * cos(i) * cos(OMEGA) # в земной
Z = Y_orb * sin(i)                                   # системе координат

final_coord = []
ref_frame_transfer(-1, final_coord, [X, Y, Z], s_time, t_obs)

print 'X = ', final_coord[0]
print 'Y = ', final_coord[1]
print 'Z = ', final_coord[2]
