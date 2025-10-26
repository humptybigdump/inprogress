/* mex function ROWCOLDEL                                           */
/* Usage within MATLAB:                                             */
/* Mmod=rowcoldel(M,which,symmetric)                                */
/* deletes rows and columns of a sparse matrix by inserting         */
/* zero entries into the corresponding off-diagonals and            */
/* unity entries into the main diagonal                             */
/* M : real, sparse matrix                                          */
/* which: vector of indices of the rows and columns to be deleted   */
/* symmetric: flag which indicates whether M has symmetric structure*/
/*         Note 0 => asymmetric structure, 1=> symmetric.           */
/* mexFunction is the gateway routine for the MEX-file.             */
/* returns the modied matrix                                        */

/* compile within MATLAB by: mex -O rowcoldel.c                     */
/* requires a valid C-compiler and correct setting in mexopts.sh    */

/* Test Code for Matlab                                             */
/* A=spdiags(rand(1e6,5),-2:2,1e6,1e6);                             */
/* t=cputime;Amod=rowcoldel(A,[17 26 33 89]);cputime-t              */
/* The speed-up by using the mex-file rather than standard MATLAB   */
/* was on a Linux-box with gcc-compiler a factor of 22.9            */

#include "mex.h"
#include <math.h>
void mexFunction( int nlhs, mxArray *plhs[],
             int nrhs,const mxArray *prhs[] )
{
  /* Declare variables. */
  int        i, pfir, plas, totn,which,nocol,nodel,idel,help,counter,symmetric,nopc,steps;
  mwIndex    *ir,*jc;
  double *pr, /* *pi, *si, *sr,*/ *pr2;
  int row_idx[27];

  /* Check for proper number of input and output arguments. */
  if (nrhs != 3) {
      mexErrMsgTxt("Three input arguments required.");
  }

 /* Check for proper data types. */
 if (mxIsSparse(prhs[0]) != 1){
     mexErrMsgTxt("First parameter must be a sparse matrix.");
 }
 symmetric=(int)mxGetScalar(prhs[2]);
 /* Copy the matrix */
 plhs[0]=mxDuplicateArray(prhs[0]);


 /* Determine number of rows/columns to delete. */
 nodel = mxGetN(prhs[1])*mxGetM(prhs[1]);
 pr2 =  mxGetPr(prhs[1]);

 /* Get the starting positions of all four data arrays. */
     pr = mxGetPr(plhs[0]);
     ir = mxGetIr(plhs[0]);
     jc = mxGetJc(plhs[0]);
     nocol  = mxGetN(plhs[0]);
     totn = jc[nocol];

 /* Loop over all entries to be deleted */
 for (idel=0;idel<nodel;idel++) {
     which = (int)pr2[idel]; 

     /* Determine first and last entry of the column. */
     pfir = jc[which-1];
     plas = jc[which];

   if(symmetric){/* SYMMETRIC structured (sparse) matrix*/
     /* Delete the column */
     counter=0;
     
     for (i=pfir; i<plas; i++) {
         if (ir[i] == which-1) {
           /*i==j -> diagonal element */
           pr[i] = 1;
      
         }
         else {
           pr[i] = 0;
           row_idx[counter]=ir[i];
           counter++;
         }
     }
     /*Delete the row*/
     for (i=0; i<counter; i++) {
       help=jc[row_idx[i]];
       nopc=jc[row_idx[i]+1]-help; /*nopc number of entries per column*/
       steps=0;
       while(ir[help]!=which-1) {help++; steps++;if(steps>=nopc)mexErrMsgTxt("Matrix is not symmetric");}
       pr[help]=0;
     }
   }else{ /* ASYMMETRIC structured (sparse) matrix*/
     
     /* Delete the column */
     for (i=pfir; i<plas; i++) {
         if (ir[i] == which-1) {
           /*i==j -> diagonal element */
           pr[i] = 1;
      
         }
         else {
           pr[i] = 0;
         }
     }

     /* Delete the row */
     for (i=0; i<pfir;i++){
         if (ir[i] == which-1) {
            pr[i]=0;
         }
     }

     for (i=plas; i<totn;i++){
         if (ir[i] == which-1) {
            pr[i]=0;
         }
     }

   }
  }
}

