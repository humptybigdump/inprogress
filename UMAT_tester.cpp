#include <iostream>
#include <fstream>
#include "umat.h"
using namespace std;

// compile with "g++ -g -std=c++0x UMAT_tester umat.cpp -o outputfile"

// explanation of compiler options:
// -o outputfile: Specifies output file as outputfile
// -std=c++0x: Language standard specification (2011 ISO C++ standard)
// -g: Necessary for valgrind to produce line numbers. Useful when debugging segfaults.
// also see https://gcc.gnu.org/onlinedocs/gcc/Option-Summary.html for further information

// to use umat with abaqus, use the makefile

class UmatTester{
public:
// Output
    double* stress; // Cauchy stress; relevant for results
    double* statev; // Internal variables
    double* ddsdde; // Consistent algorithmic tangent; relevant for convergence
    double* sse; // Specific strain energy; output only
    double* spd; // Specific plastic dissipation; output only
    double* scd; // Specific creep dissipation; output only
    double* rpl, *ddsddt, *drplde, *drpldt; // Thermal output
// Input
    double* stran; // Strain before timestep
    double* dstran; // Strain increment during timestep
    double time[2] = {0}; // [Step time (or frequency), total time]
    double* dtime; // Time increment
    double* temp,* dtemp; // Thermal
    double* predef,* dpred; // Predefined fields
    char cmname[5] = {'t', 'e', 's', 't', '\0'}; // User-defined material name
    int* ndi; 
    int* nshr;
    int* ntens; // Tensor dimension (in 3D: 6)
    int* nstatv; // Number of internal variables
    int* nprops; // Number of material properties
    double* props; // Material properties
    double coords[3] = {0}; // Spatial coordinates (X or x if NLGEOM)
    double drot[9] = {0}; // Increment of rotation of the material point. Stress and strain are already so rotated. (I if not NLGEOM)
    double* pnewdt;
    double* celent; // Characteristic element length
    double dfgrd0[9] = {0}; // Deformation gradient F before timestep
    double dfgrd1[9] = {0}; // Deformation gradient F after timestep
    int* noel; // Element number
    int* npt; // Integration point number
    int* layer, *kspt; // For composite shells
    int jstep[4] = {0}; // [Step number, procedure type, NLGEOM, linear perturbation]
    int* kinc; // Increment number
    short cmname_len = 5;

	ofstream data_file;
    
    // Default constructor
    explicit UmatTester(int dim){
        // Tensor values
        ntens = new int(dim*(dim+1)/2);
        ndi = new int(dim);
        nshr = new int(*ntens-*ndi);
        stress = new double[*ntens]{0};
        ddsdde = new double[*ntens*(*ntens)]{0};
        stran = new double[*ntens]{0};
        dstran = new double[*ntens]{0};

        ddsddt = new double[*ntens]{0};
        drplde = new double[*ntens]{0};

        drot[0] = 1;
        drot[4] = 1;
        drot[8] = 1;

        // Material properties
        nprops = new int(7);
        props = new double[*nprops]{0};
	    props[0] = 210000.0; //E
	    props[1] = 0.3; //nu
	    props[2] = 10000.0; //h
	    props[3] = 100.0; //sigma_F0
	    props[4] = 50000.0; //h0
	    props[5] = 3000.0; //hinf
	    props[6] = 500.0; //sigma_Finf

        // state variables
        nstatv = new int(7);
        statev = new double[*nstatv]{0};

        // Time step variables
        dtime = new double(0);
        jstep[0] = 0;
        jstep[1] = 1;
        kinc = new int(0);

        // Energy and other scalars
        sse = new double(0);
        spd = new double(0);
        scd = new double(0);
        rpl = new double(0);
        drpldt = new double(0);
        temp = new double(0);
        dtemp = new double(0);
        pnewdt = new double(0);

        // Element information
        noel = new int(1);
        npt = new int(1);
        layer = new int(1);
        kspt = new int(1);
        celent = new double(1);
    };

    void step(double* dstran_new, double dtime_new){
        jstep[0] ++;
        dstran = dstran_new;
        *dtime = dtime_new;
		umat_(stress,statev,ddsdde,sse,spd,scd,rpl,ddsddt,drplde,drpldt,
		stran,dstran,time,dtime,temp,dtemp,predef,dpred,cmname,ndi,nshr,
		ntens,nstatv,props,nprops,coords,drot,pnewdt,celent,dfgrd0,dfgrd1,noel,npt,
		layer,kspt,jstep,kinc,cmname_len);
        data_file << time[0] << " " << stress[0] << " " << stran[0] << " " << statev[0] << "\n";
    }; 

    double strain_function(double t){
    	return 0.02*t;
    };

    void simulate(){
	    double tmax = 1.0;
	    dtime[0] = 0.0;
        for (int i=0; i<6; i++){
            stran[i] = 0.0;   
        }
	    *dtime = 0.01;

    	data_file.open("output.dat");
        data_file << time[0] << " " << stress[0] << " " << stran[0] << " " << statev[0] << "\n";
    	while (time[0]<tmax) {
		    stran[0] = strain_function(time[0]);
		    stran[1] = -0.5*strain_function(time[0]);
		    stran[2] = -0.5*strain_function(time[0]);
		    time[0] += *dtime;
		    dstran[0] = strain_function(time[0])-stran[0];
		    dstran[1] = -0.5*strain_function(time[0])-stran[1];
		    dstran[2] = -0.5*strain_function(time[0])-stran[2];
            step(dstran, *dtime);
    	};
        data_file.close();
    };
};


int main(){
	UmatTester tester(3);
    tester.simulate();
	return 0;
}

