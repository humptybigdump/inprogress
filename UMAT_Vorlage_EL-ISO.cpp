#include <iostream>
using namespace std;

extern "C" void umat_(double *stress, double *statev, double *ddsdde, double *sse, double *spd,
		double *scd, double *rpl, double *ddsddt, double *drplde, double *drpldt,
		double *stran, double *dstran, double *time, double *dtime, double *temp,
		double *dtemp, double *predef, double *dpred, char *cmname, int *ndi, int *nshr,
		int *ntens, int *nstatv, double *props, int *nprops, double *coords, double *drot,
		double *pnewdt, double *celent, double *dfgrd0, double *dfgrd1, int *noel, int *npt,
		int *layer, int *kspt, int *kstep, int *kinc, short cmname_len){

// 	Zeros are to be replaced with code

// 	Elastic constants
	double E = 0;
	double NU = 0;
	double G = 0;
	double lambda = 0;

// 	User defined variables
	double eps [6];
	double trEps;

// 	Current strain
	for (int i = 0; i < 6; i++){
		eps[i] = 0;
	}

// 	Trace of strain tensor
	trEps = 0;

//	Setting stiffness matrix to zero
	for (int i = 0; i < 6; i++){
		for(int j = 0; j< 6; j++){
			ddsdde[6*i+j] = 0;
		}
	}

//	Isotropic elastic stiffness matrix
	for(int i = 0; i < 3; i++){
		ddsdde[6*i+i] = 0;
		ddsdde[6*(i+3)+(i+3)] = 0;
		for(int j = 0; j < 3; j++){
			ddsdde[6*i+j] += 0;
		}
	}

//	Update stress
	for(int i = 0; i < 3; i++){
		stress[i] = 0;
	}
	for(int i = 3; i < 6; i++){
		stress[i] = 0;
	}

}

