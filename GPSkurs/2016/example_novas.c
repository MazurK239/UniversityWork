#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include "eph_manager.h"
#include "novas.h"

int main(void) {

	double ter[3];
	double cel[] = {0.0, 1000.0, 10000.0};
	const double tta = 2457508.20833;

	short int error;
	error = cel2ter(tta, 0.0, 0.0, 0, 0, 0, -0.002, 0.529, cel, ter);

	printf("NOVAS\n");
	printf("The celestial coordinates are:\n");
	printf("Xc = %f\n", cel[0]); // 
	printf("Yc = %f\n", cel[1]); // Terrestrial coordinates
	printf("Zc = %f\n", cel[2]); //
	printf("\n");

	printf("The terrestrial coordinates are:\n");
	printf("Xt = %f\n", ter[0]); // 
	printf("Yt = %f\n", ter[1]); // Terrestrial coordinates
	printf("Zt = %f\n", ter[2]); //
	return 0;

}
