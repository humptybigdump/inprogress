// Core umat function
extern "C" void umat_(double *stress, double *statev, double *ddsdde, double *sse, double *spd,
		double *scd, double *rpl, double *ddsddt, double *drplde, double *drpldt,
		double *stran, double *dstran, double *time, double *dtime, double *temp,
		double *dtemp, double *predef, double *dpred, char *cmname, int *ndi, int *nshr,
		int *ntens, int *nstatv, double *props, int *nprops, double *coords, double *drot,
		double *pnewdt, double *celent, double *dfgrd0, double *dfgrd1, int *noel, int *npt,
		int *layer, int *kspt, int *kstep, int *kinc, short cmname_len){
};

// Declaration for Windows
extern "C" void umat(double *stress, double *statev, double *ddsdde, double *sse, double *spd,
		double *scd, double *rpl, double *ddsddt, double *drplde, double *drpldt,
		double *stran, double *dstran, double *time, double *dtime, double *temp,
		double *dtemp, double *predef, double *dpred, char *cmname, int *ndi, int *nshr,
		int *ntens, int *nstatv, double *props, int *nprops, double *coords, double *drot,
		double *pnewdt, double *celent, double *dfgrd0, double *dfgrd1, int *noel, int *npt,
		int *layer, int *kspt, int *kstep, int *kinc, short cmname_len){
    umat_(stress, statev,  ddsdde,  sse,  spd,
		 scd,  rpl,  ddsddt,  drplde,  drpldt,
		 stran,  dstran,  time,  dtime,  temp,
		 dtemp,  predef,  dpred, cmname,  ndi,  nshr,
		 ntens,  nstatv,  props,  nprops,  coords,  drot,
		 pnewdt,  celent,  dfgrd0,  dfgrd1,  noel,  npt,
		 layer,  kspt,  kstep,  kinc, cmname_len);
};
