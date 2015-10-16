#! usr/bin/python

from math import sqrt, cos, sin
import sys

def runge_kutta(num_of_eq, fun, X, X0, dt, int_end):
    X.append(X0)
    for i in range(int(int_end / dt) - 1):
        ti = i * dt
        k1 = []
        k2 = []
        k3 = []
        k4 = []
        X.append([])
        for j in range(num_of_eq):
            k1.append(dt * fun(j, ti, X[i]))
        for j in range(num_of_eq):
            k2.append(dt * fun(j, ti + 0.5*dt, [X[i][idx] + 0.5*k1[idx] for idx in range(num_of_eq)]))
        for j in range(num_of_eq):
            k3.append(dt * fun(j, ti + 0.5*dt, [X[i][idx] + 0.5*k2[idx] for idx in range(num_of_eq)]))
        for j in range(num_of_eq):
		    k4.append(dt * fun(j, ti + dt, [X[i][idx] + k3[idx] for idx in range(num_of_eq)]))
        for j in range(num_of_eq):
            X[i+1].append(X[i][j] + 1/6.0 * (k1[j] + 2*k2[j] + 2*k3[j] + k4[j]))

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
        geo_sys.append(abs_sys[3] * cos(S) + abs_sys[4] * sin(S) + omega * geo_sys[1])
        geo_sys.append(-abs_sys[3] * sin(S) + abs_sys[4] * cos(S) - omega * geo_sys[0])
        geo_sys.append(abs_sys[5])

def fun(num, time, vect):
	MU = 398600.4418
	C20 = 1082.62575e-6
	Ae = 6378.136
	R0 = sqrt(vect[0]**2 + vect[1]**2 + vect[2]**2)
	Ro = Ae / R0
	MU /= R0**2
	temp_dict = { 0: vect[3],
   		  		  1: vect[4],
				  2: vect[5],
				  3: -MU * vect[0] / R0 + 1.5 * C20 * MU * vect[0] * Ro**2 * (1 - 5 * (vect[2]/R0)**2) / R0,# - 0.279396772385e-08,
				  4: -MU * vect[1] / R0 + 1.5 * C20 * MU * vect[1] * Ro**2 * (1 - 5 * (vect[2]/R0)**2) / R0,# + 0.931322574616e-09,
				  5: -MU * vect[2] / R0 + 1.5 * C20 * MU * vect[2] * Ro**2 * (3 - 5 * (vect[2]/R0)**2) / R0 }# - 0.186264514923e-08 }
	return(temp_dict[num])

filename = sys.argv[1]
i_file = open(filename, 'r')

geo_vect0 = [float(i_file.readline()) for dummy_idx in range(6)]
t_begin = float(i_file.readline())
t_end = float(i_file.readline())
s_time = float(i_file.readline())

abs_vect0 = []
ref_frame_transfer(1, geo_vect0, abs_vect0, s_time, t_begin)

X = []
runge_kutta(6, fun, X, abs_vect0, 0.04, t_end - t_begin)

geo_vect = []
ref_frame_transfer(-1, geo_vect, X[-1], s_time, t_end)

print 'X = ', geo_vect[0]
print 'Y = ', geo_vect[1]
print 'Z = ', geo_vect[2]
