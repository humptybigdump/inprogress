#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <math.h>
#include <string.h>


double f0(double x) {
} 

double f1(double x) {
}                                                                                                             

double f2(double x) {
} 
                                                                                                              
double f3(double x) {                                                                                         
}                                                                                                             
                                                                                                              
double f4(double x) {                                                                                         
}

double QuadraturInner(double (*func)(double), double a, double b, int n, char *verfahren) {
	//Die QuadraturInner-Funktion ist auf die Quadratur eines einzelnen Intervalls spezialisiert. 
	//func = funktion; 
	//a,b Intervallgrenzen
  //n = Anzahl Stützstellen-1
  double summe = 0.0;                                                                 
  double h_i=(b-a);                                                                   
  double WEIGHTS[5][5] = {                                                            
                {1.0,0.0,0.0,0.0,0.0},                                                                        //Werte für Unter-Mittel und Obersumme
                {0.0,0.0,0.0,0.0,0.0},                                                                        //Werte für Trapez Regel                                                                                              
                {0.0,0.0,0.0,0.0,0.0},                                                                        //Werte für Simpson Regel                                                                                            
                {0.0,0.0,0.0,0.0,0.0},                                                                        //Werte für Newton Regel                                                                                             
                {0.0,0.0,0.0,0.0,0.0},                                                                        //Werte für Miln's Regel                                                                     
        };                                                                                                      
          
  if (strcmp(verfahren,"Trapez")==0  || strcmp(verfahren,"Simpson")==0 || strcmp(verfahren,"Newton")==0 || strcmp(verfahren,"Miln's-Regel")==0) {
                                                                                                              //Berechnungsformel für Trapez-, Simpson-, Newton-, und Miln's Regel
  } else if (strcmp(verfahren,"Untersumme")==0){                                                                                                              
      summe =WEIGHTS[0][0] * func(a + h_i * 0.0);                                                             //Berechnungsformel für Untersumme
  } else if (strcmp(verfahren,"Mittelsumme")==0){                                                             
                                                                                                              //Berechnungsformel für Mittelsumme
  } else if (strcmp(verfahren,"Obersumme")==0){                                                               
                                                                                                              //Berechnungsformel für Obersumme
  }                                                                                                           
}                                                                                                          

double CheckQuadraturInner(double (*func)(double), double a, double b, int NInterv, int n, char *verfahren) {
  double h = (b - a) / NInterv;      
  double summe = (QuadraturInner(func,a, a+h, n, verfahren)+QuadraturInner(func,a+h, a+2*h, n, verfahren));
  return summe;
}

double QuadraturOuter(double (*func)(double), double a, double b, int NInterv, int n, char *verfahren) {   
  //Die QuadOuter-Funktion ist verantwortlich für die Berechnung der numerischen Integration über mehrere Intervalle. 
  //a: linke Intervallgrenze                                                                              
  //b: rechte Intervallgrenze                                                                             
  //NInterv: Anzahl der verwendeten Intervalle                                                            
	                                                                                                         
	double h = (b - a) / NInterv;                                                                            
  double summe = 0.0;                                                                                      
	double x_i;                                                                                              
	double x_iP1;                                                                                            
                                                                                                           
                                                                                                              
  return summe;                                                                       
}
 
double** Sensitivity(double (*func)(double),double int_sym, double a, double b, int n, char *verfahren) {
	//Die Sensitivität wird als prozentualer Fehler vom erwarteten integralen Wert (int_sym) berechnet.	
	//NoDoublingInterv: Die Anzahl der Iterationen, in denen die Anzahl der Intervalle verdoppelt wird.
	//NInterv: Die aktuelle Anzahl der Intervalle, initialisiert mit 2

  int NoDoublingInterv = 4;
  int NInterv = 2;

  //Dynamische Allokation für das Fehlerarray. 
  double** ErrorArray = (double**)malloc(NoDoublingInterv * sizeof(double*));
  for (int i = 0; i < NoDoublingInterv; i++) {
      ErrorArray[i] = (double*)malloc(2 * sizeof(double));
  }
  
  //Mit diesen zwei Aufrufen checken Sie, ob Ihre Implementierung der QuadraturInner Funktion richtig ist.
  ErrorArray[0][0] = NInterv;                                                 
  ErrorArray[0][1] = ((CheckQuadraturInner(func,a, b, NInterv, n, verfahren) - int_sym) / int_sym * 100.0);
	//Berechnung des Fehlers, speichern in Error-Array. Hinweis: Schauen Sie sich das Ende der Main Funktion an. Dort werden die Ergebnisse in eine Datei geschrieben und diese dann geplotten. Hieraus können Sie schließen, welche Daten in ErrorArray gespeichert werden. 
//   
    
  //Geben Sie das verwendete Verfahren, die Intervalle und den prozentualen Fehler aus. Hinweis: Sie benötigen hierfür keine neuen Variablen. 
  printf("\n--Error-Array der %s--\n", verfahren);                                                            
  printf("ErrorArray:\n");                                                                                    
  printf("Intervalle | Prozentualer Fehler \n");                                                              
  for (int i = 0; i < 4; i++) {                                                                               
      printf("%lf\t%lf\n", ErrorArray[i][0], ErrorArray[i][1]);                                               
  }                                                                                                           
                                                                                                            
                                                                                                            
  return ErrorArray;                                                                                        
}                                                                                                           
                                                                                                            
                                                                                                            
                                                                                                            
int main() {	                                                                                              
  double (*f)(double) =f0;                                                                                 
  char *str [] = {"Untersumme", "Mittelsumme", "Obersumme" ,"Trapez","Simpson","Newton","Miln's-Regel"};   
  double **ErrorArray_unter, **ErrorArray_mittel, **ErrorArray_ober, **ErrorArray_trapez, **ErrorArray_simpson, **ErrorArray_newton, **ErrorArray_miln;

  //Untersumme Nehmen Sie sich diesen Aufruf als Beispiel für die anderen Verfahren.                       
  ErrorArray_unter = Sensitivity(f,int_sym_value,a, b, 0, str[0]);                                
  //Mittelsumme                                                                                            
  //Obersumme                                                                                                         
  //Trapez                                                                                                            
  //Simpson                                                                                                   
  //Newton                                                                                                    
  //Milns-Regel                                                                                               

  //Hinweis: Ab hier ist nur noch die Variable plotflag zu ändern.   
	//Daten in eine Datei schreiben
	FILE *fp = fopen("plot_data.dat", "w");
	if (fp == NULL) {
		fprintf(stderr, "Fehler beim Öffnen der Datei zum Schreiben\n");
		return 1;
	}

  for (int i = 0; i < 4; i++) {
		fprintf(fp, "%lf %lf %lf %lf %lf %lf %lf %lf \n",ErrorArray_unter[i][0], ErrorArray_unter[i][1], ErrorArray_mittel[i][1], ErrorArray_ober[i][1], ErrorArray_trapez[i][1],  ErrorArray_simpson[i][1], ErrorArray_newton[i][1], ErrorArray_miln[i][1]);
	}

	fclose(fp);
  
  long plotflag = 1;

  if (plotflag) {
	//Gnuplot-Skript generieren
	FILE *gp = popen("gnuplot -p", "w");
	if (gp == NULL) {
		fprintf(stderr, "Fehler beim Öffnen des Gnuplot-Pipes\n");
		return 1;
	}

	fprintf(gp, "set key right top box\n");
	fprintf(gp, "set xlabel \"Intervalle\"\n");
	fprintf(gp, "set ylabel \"Fehler\"\n");

	fprintf(gp, "plot 'plot_data.dat' using 1:2 with lines lw 2 lc rgb 'red' title 'Untersumme', 'plot_data.dat' using 1:3  with lines lw 2 lc rgb 'green' title 'Mittelsumme', 'plot_data.dat' using 1:4 with lines lw 2 lc rgb 'blue' title 'Obersumme', 'plot_data.dat' using 1:5 with lines lw 2 lc rgb 'black' title 'Trapez', 'plot_data.dat' using 1:6  with lines lw 2 lc rgb 'orange' title 'Simpson', 'plot_data.dat' using 1:7 with lines lw 2 lc rgb 'yellow' title 'Newton', 'plot_data.dat' using 1:8 with lines lw 2 lc rgb 'brown' title 'Milne';\n");

	fclose(gp);
  }
	printf("Drücken Sie Enter zum Beenden...\n");
	getchar();
    return 0;
}
