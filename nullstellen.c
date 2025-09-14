#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <math.h>
#include <string.h>

#ifndef M_PI
#    define M_PI 3.14159265358979323846
#endif

double f1(double x) {
//#  return /* Hier f_1(x) */;
}

double df1(double x) {
} 

double f2(double x) {
} 

double df2(double x) { 
}
 
 
double Bisektion(double (*f)(double), double xa, double xb) {
  double m;

  //Kopfzeile für die Ausgabe
  printf("  n:  l                 r                 f(l)          f(r)\n"); 
  return m; //Rückgabe der gefundenen Nullstelle
}

double Sekanten(double (*f)(double), double x0, double x1) {
    
}

double Newton(double (*f)(double), double (*dfdx)(double), double x0) {
}

int main() {
  double result;

  printf("\n\nBisektion\n–––––––––\n");
  result = Bisektion(f1, -3.0, -0.5);
  printf("Nullstelle Bisektion: %.14lf\n", result);

  printf("\n\nSekanten\n––––––––\n");
  result = Sekanten(f1, -3.0, -0.5);
  printf("Nullstelle Sekanten: %.14lf\n", result);

  printf("\n\nNewton\n––––––\n");
  result = Newton(f1, df1, -0.5);
  printf("Nullstelle: %.14lf\n", result);

  return 0;
}
