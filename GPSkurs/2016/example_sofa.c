#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include "sofa.h"

int main(void) {

	double ter[3] = {};
	double cel[] = {0.0, 1000.0, 10000.0};
	double matr[3][3];
	const double tta = 2457508.20833;

	iauC2t00a(tta, 0.0, tta, 0.0, -0.002/206265.0, 0.529/206265.0, matr);
	ter[0] = matr[0][0] * cel[0] + matr[0][1] * cel[1] + matr[0][2] * cel[2];
	ter[1] = matr[1][0] * cel[0] + matr[1][1] * cel[1] + matr[1][2] * cel[2];
	ter[2] = matr[2][0] * cel[0] + matr[2][1] * cel[1] + matr[2][2] * cel[2];

	printf("SOFA\nThe celestial coordinates are:\n");
	printf("Xc = %f\n", cel[0]); // 
	printf("Yc = %f\n", cel[1]); // Terrestrial coordinates
	printf("Zc = %f\n", cel[2]); //

	printf("\nThe terrestrial coordinates are:\n");
	printf("Xt = %f\n", ter[0]); // 
	printf("Yt = %f\n", ter[1]); // Terrestrial coordinates
	printf("Zt = %f\n", ter[2]); //
	return 0;

}
