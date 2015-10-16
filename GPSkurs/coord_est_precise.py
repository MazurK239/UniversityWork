#! usr/local/bin/python
# coding: utf-8

import math, sys
import numpy as np

c = 299792458.0
a = 6378137.0
b = 6356752.0


i_file_name = sys.argv[1]
o_file_name = sys.argv[2]

i_file = open(i_file_name, 'r')
o_file = open(o_file_name, 'w')

sat_names = []
sat_X = []
sat_Y = []
sat_Z = []
sat_P = []
sat_t = []
delta_X = []
delta_Y = []
delta_Z = []
delta_P = []
sigma_X = []
sigma_Y = []
sigma_Z = []
sigma_P = []
A = []

number_of_sattelites = int(i_file.readline())

for dummy_idx in range(4):
	sat_names.append(i_file.readline())
	sat_X.append(float(i_file.readline()))
	sat_Y.append(float(i_file.readline()))
	sat_Z.append(float(i_file.readline()))
	sat_P.append(float(i_file.readline()))
	sat_t.append(float(i_file.readline()))

for idx in range(4):
	sat_P[idx] += c * sat_t[idx]

for idx in range(3):
	delta_P.append(sat_P[idx+1] - sat_P[idx])
	delta_X.append(sat_X[idx+1] - sat_X[idx])
	delta_Y.append(sat_Y[idx+1] - sat_Y[idx])
	delta_Z.append(sat_Z[idx+1] - sat_Z[idx])
	sigma_P.append(sat_P[idx+1] + sat_P[idx])
	sigma_X.append(sat_X[idx+1] + sat_X[idx])
	sigma_Y.append(sat_Y[idx+1] + sat_Y[idx])
	sigma_Z.append(sat_Z[idx+1] + sat_Z[idx])

for idx in range(3):
	A.append((delta_X[idx] * sigma_X[idx] + delta_Y[idx] * sigma_Y[idx] + delta_Z[idx] * sigma_Z[idx] - delta_P[idx] * sigma_P[idx])/2)

D = np.linalg.det(np.array([[delta_X[0], delta_Y[0], delta_Z[0]], [delta_X[1], delta_Y[1], delta_Z[1]], [delta_X[2], delta_Y[2], delta_Z[2]]]))
D1 = np.linalg.det(np.array([[A[0], delta_Y[0], delta_Z[0]], [A[1], delta_Y[1], delta_Z[1]], [A[2], delta_Y[2], delta_Z[2]]]))
D2 = np.linalg.det(np.array([[delta_X[0], A[0], delta_Z[0]], [delta_X[1], A[1], delta_Z[1]], [delta_X[2], A[2], delta_Z[2]]]))
D3 = np.linalg.det(np.array([[delta_X[0], delta_Y[0], A[0]], [delta_X[1], delta_Y[1], A[1]], [delta_X[2], delta_Y[2], A[2]]]))
d1 = np.linalg.det(np.array([[-delta_P[0], delta_Y[0], delta_Z[0]], [-delta_P[1], delta_Y[1], delta_Z[1]], [-delta_P[2], delta_Y[2], delta_Z[2]]]))
d2 = np.linalg.det(np.array([[delta_X[0], -delta_P[0], delta_Z[0]], [delta_X[1], -delta_P[1], delta_Z[1]], [delta_X[2], -delta_P[2], delta_Z[2]]]))
d3 = np.linalg.det(np.array([[delta_X[0], delta_Y[0], -delta_P[0]], [delta_X[1], delta_Y[1], -delta_P[1]], [delta_X[2], delta_Y[2], -delta_P[2]]]))

X_sh = D1 / D
Y_sh = D2 / D
Z_sh = D3 / D
a_x = d1 / D
a_y = d2 / D
a_z = d3 / D

delta_X_sh = sat_X[3] - X_sh
delta_Y_sh = sat_Y[3] - Y_sh
delta_Z_sh = sat_Z[3] - Z_sh

a4 = 1 - a_x**2 - a_y**2 - a_z**2
b4 = sat_P[3] + delta_X_sh * a_x + delta_Y_sh * a_y + delta_Z_sh * a_z
c4 = -delta_X_sh**2 - delta_Y_sh**2 - delta_Z_sh**2 + sat_P[3]**2

eps1 = -b4 / a4 + math.sqrt(b4**2 - a4 * c4) / a4
eps2 = -b4 / a4 - math.sqrt(b4**2 - a4 * c4) / a4

delta_t_1 = eps1 / c
delta_t_2 = eps2 / c

if (-0.0005 < delta_t_1 < 0.0005):
	eps = eps1
elif (-0.0005 < delta_t_2 < 0.0005):
	eps = eps2
else:
	print 'None of delta_t match chosen criteria.'

X = X_sh + eps * a_x
Y = Y_sh + eps * a_y
Z = Z_sh + eps * a_z

e = math.sqrt((a**2 - b**2) / a**2)
e_sh = math.sqrt((a**2 - b**2) / b**2)

longitude = math.atan(Y / X)
teta = math.atan(a * Z / b / math.sqrt(X**2 + Y**2))
latitude = math.atan((Z + e_sh**2 * b * math.sin(teta)**3) / (math.sqrt(X**2 + Y**2) - e**2 * a * math.cos(teta)**3))

lon = longitude * 12 / math.pi
lat = latitude * 180 / math.pi

o_file.write('Longitude: ' + str(int(lon)) + 'h ' + str(int((lon - int(lon)) * 60)) + 'm ' + str(((lon - int(lon)) * 60 - int((lon - int(lon)) * 60)) * 60) + 's' + '\n')
o_file.write('Latitude: ' + str(int(lat)) + 'd ' + str(int((lat - int(lat)) * 60)) + 'm ' + str(((lat - int(lat)) * 60 - int((lat - int(lat)) * 60)) * 60) + 's' + '\n')

