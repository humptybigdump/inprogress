/* mexFunction is the gateway routine for the MEX-file. */
#include "mex.h"
#include <math.h>
#include <stdio.h>
void mexFunction( int nlhs, mxArray *plhs[],
             int nrhs,const mxArray *prhs[] )
{
  /* Declare variables. */
  int        i,j,in,jn,nodnum,neinod,totent,nx,ny,nzmax,nnod,hel[4];
  int        ii,jj,kk,ijel;
  mwIndex    *Ir,*Jc;
  double     *Pr, *Mel, *K, dummy;

  /* Check for proper number of input and output arguments. */
  if (nrhs != 2) {
      mexErrMsgTxt("Two input arguments required.");
  }

/* First argument: conductivity matrix */
K=mxGetPr(prhs[0]);
ny=mxGetM(prhs[0]);
nx=mxGetN(prhs[0]);

/* Second argument stiffness matrix of a single element */
Mel=mxGetPr(prhs[1]);
if (mxGetN(prhs[1])!= 4 | mxGetM(prhs[1])!= 4) {
    mexErrMsgTxt("Second argument must be 4x4 matrix");
}

nzmax=(nx-1)*(ny-1)*9 + (2*(nx-1) + 2*(ny-1))*6+ 4*4;

nnod=(nx+1)*(ny+1);

/* (void)printf("nx %i\n",nx);
(void)printf("ny %i\n",ny);
(void)printf("nnod %i\n",nnod);
(void)printf("nzmax %i\n",nzmax); */

plhs[0] = mxCreateSparse(nnod,nnod,nzmax,0);
Pr = mxGetPr(plhs[0]);
Ir = mxGetIr(plhs[0]);
Jc = mxGetJc(plhs[0]);

/* initialization total number of entries */
totent=0;

/* Loop over all nodes */
    for (i=0;i<nx+1;i++) {
        for (j=0;j<ny+1;j++) {
            nodnum = i*(ny+1) + j;
            Jc[nodnum]=totent;
            /* find the neighboring nodes */
            if (i>0) {
                in=i-1;
                if (j>0) {
                    jn=j-1;
                    neinod=in*(ny+1) + jn;
                    Ir[totent]=neinod;
                    Pr[totent]=0;
                    totent++;
                }
                jn=j;
                neinod=in*(ny+1) + jn;
                Ir[totent]=neinod;
                Pr[totent]=0;
                totent++;
                if (j<ny) {
                    jn=j+1;
                    neinod=in*(ny+1) + jn;
                    Ir[totent]=neinod;
                    Pr[totent]=0;
                    totent++;
                }
            }
            in=i;
            if (j>0) {
                jn=j-1;
                neinod=in*(ny+1) + jn;
                Ir[totent]=neinod;
                Pr[totent]=0;
                totent++;
            }
            jn=j;
            neinod=in*(ny+1) + jn;
            Ir[totent]=neinod;
            Pr[totent]=0;
            totent++;
            if (j<ny) {
                jn=j+1;
                neinod=in*(ny+1) + jn;
                Ir[totent]=neinod;
                Pr[totent]=0;
                totent++;
            }
            if (i<nx) {
                in=i+1;
                if (j>0) {
                    jn=j-1;
                    neinod=in*(ny+1) + jn;
                    Ir[totent]=neinod;
                    Pr[totent]=0;
                    totent++;
                }
                jn=j;
                neinod=in*(ny+1) + jn;
                Ir[totent]=neinod;
                Pr[totent]=0;
                totent++;
                if (j<ny) {
                    jn=j+1;
                    neinod=in*(ny+1) + jn;
                    Ir[totent]=neinod;
                    Pr[totent]=0;
                    totent++;
                }
            }
        }
    }

Jc[nnod]=totent;

/* Fill in entries */
/* Loop over all elemnst */
    for (i=0;i<nx;i++) {
        for (j=0;j<ny;j++) {
            hel[0]= i*(ny+1) + j;
            hel[1]= hel[0]+1;
            hel[2]= hel[0]+ny+1;
            hel[3]= hel[1]+ny+1;
            ijel  = i*ny + j;
            for (ii=0;ii<4;ii++) {
            for (jj=0;jj<4;jj++) {
                kk=Jc[hel[ii]];
                while (Ir[kk]!=hel[jj]) kk++;
                Pr[kk]+=Mel[ii*4+jj]*K[ijel];
            }
            }
        }
    }

}
 
