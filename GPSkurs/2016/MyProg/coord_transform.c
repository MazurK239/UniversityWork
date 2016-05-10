#include <stdio.h>
#include <math.h>
int main(void) {

	double coord[]={10000.0,20000.0,30000.0};
	void transform(double, double, double, double*, double*, double*, double, double, double);
	double Xc, Yc, Zc, Xt, Yt, Zt;
	Xc = 10000.0; Yc = 20000.0; Zc = 30000.0; // Celestial coordinates
	transform(Xc, Yc, Zc, &Xt, &Yt, &Zt, 0.15937029, 86400.0, 0.0);
	printf("Xt = %f\n", Xt); // 
	printf("Yt = %f\n", Yt); // Terrestrial coordinates
	printf("Zt = %f\n", Zt); //
	return 0;

}

double poly(double koef1, double koef2, double koef3, double koef4, double koef5, double t) {
	return (koef1 * t + koef2 * t*t + koef3 * t*t*t + koef4 * t*t*t*t + koef5 * t*t*t*t*t) / 206265;
}

void transform(double Xc, double Yc, double Zc, double* Xt, double* Yt, double* Zt, double j_cent, double t, double s) {
	double fi;
	const double Omega_dot = 7.2921151467e-05;
	double eps0 = 84381.406 / 206265;
	double psyA = poly(5038.481507, -1.0790069, -0.00114045, 0.000132851, -0.0000000951, j_cent);
	double omegaA = eps0 - poly(0.025754, -0.0512623, 0.00772503, 0.000000467, -0.0000003337, j_cent);
	double xiA = poly(10.556403, -2.3814292, -0.00121197, 0.000170663, -0.0000000560, j_cent);

	double X = Xc * (cos(psyA)*cos(xiA) + sin(psyA)*cos(omegaA)*sin(xiA)) + Yc * (cos(eps0)*sin(psyA)*cos(xiA) - cos(eps0)*cos(psyA)*cos(omegaA)*sin(xiA) - sin(eps0)*sin(omegaA)*sin(xiA)) + Zc * (-cos(eps0)* sin(omegaA)*sin(xiA) - sin(eps0)*sin(psyA)*cos(xiA) + sin(eps0)*cos(psyA)*cos(omegaA)*sin(xiA));
	double Y = Xc * (cos(psyA)*sin(xiA) - sin(psyA)*cos(omegaA)*cos(xiA)) + Yc * (cos(eps0)*sin(psyA)*sin(xiA) + cos(eps0)*cos(psyA)*cos(omegaA)*cos(xiA) + sin(eps0)*sin(omegaA)*cos(xiA)) + Zc * (cos(eps0)* sin(omegaA)*cos(xiA) - sin(eps0)*sin(psyA)*sin(xiA) - sin(eps0)*cos(psyA)*cos(omegaA)*cos(xiA));
	double Z = Xc * sin(psyA)*sin(omegaA) + Yc * (sin(eps0)*cos(omegaA) - cos(eps0)*cos(psyA)*sin(omegaA)) + Zc * (sin(eps0)*cos(psyA)*sin(omegaA) + cos(eps0)*cos(omegaA));

	fi = Omega_dot * (t - s);
	*Xt = cos(fi) * X - sin(fi) * Y;
	*Yt = sin(fi) * X + cos(fi) * Y;
	*Zt = Z;
}
