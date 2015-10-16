#! usr/bin/pyton

from math import sqrt, cos, sin, asin, atan2, atan, tan, degrees
import sys

def elements_est(r_vect, v_vect):
	
	kappa = sqrt(398600.4418)

	R = sqrt(r_vect[0]**2 + r_vect[1]**2 + r_vect[2]**2)
	V = sqrt(v_vect[0]**2 + v_vect[1]**2 + v_vect[2]**2)

	a = 1 / (2 / R - V**2 / kappa**2)

	c_vect = [r_vect[1] * v_vect[2] - r_vect[2] * v_vect[1],
			  r_vect[2] * v_vect[0] - r_vect[0] * v_vect[2],
			  r_vect[0] * v_vect[1] - r_vect[1] * v_vect[0]]
	C = sqrt(c_vect[0]**2 + c_vect[1]**2 + c_vect[2]**2)

	i = atan2(sqrt((c_vect[0])**2 + (c_vect[1])**2), c_vect[2])
	OMEGA = atan2(c_vect[0] / sin(i), -c_vect[1] / sin(i))

	p = C**2 / kappa**2

	r_dot = sum([r_vect[idx] * v_vect[idx] for idx in range(3)]) / R

	e = sqrt((p / R - 1)**2 + (r_dot * sqrt(p) / kappa)**2)

	teta = atan2(r_dot * sqrt(p) / kappa, (p / R - 1))

	u = atan2(r_vect[2] / sin(i), r_vect[0] * cos(OMEGA) + r_vect[1] * sin(OMEGA))

	omega = u - teta

	E = 2 * atan(sqrt((1 - e) / (1 + e)) * tan(teta / 2))

	M = E - e * sin(E)

	return [e, a, OMEGA, i, omega, M]
