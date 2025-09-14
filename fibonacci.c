#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>


int useplotter;

/**
 * @brief X,Y in eine Datei schreiben
 *
 * @param Y        y Wert
 * @param X        x Wert
 * @param file     Ausgabedatei
 */
void writeDatFile(double X, double Y, FILE* file) {
  fprintf(file, "%f %f\n",  X, Y);
}







int main() {

  FILE* file = fopen("GoldenerSchnitt.dat","w");
  useplotter=1;
 
 
  // -------------------------------------------------------------------------------
  // -  Implementieren Sie die Vorschrift zur Berechnung der Fibonacci-Zahlen
  // -  Berechnen Sie die 50. Fibonacci-Zahl
  // -  Berechnen Sie den Quotienten aus zwei benachbarten Fibonacci-Zahlen, 
  //    welcher in die Datei GoldenerSchnitt.dat ruasgeschrieben wird.
  // -  Aktivieren sie den plotter, indem die Variable useplotter=1 gesetzt wird.



  // ----------------------------------------------------------------------------

  fclose(file);

  if (useplotter==1){
    
    FILE *gp = popen("gnuplot -p", "w");
    fprintf(gp, "set key right bottom box; set xlabel \"index i\"; set ylabel \"Goldener Schnitt\";\n");
    fprintf(gp, ";\n");
    fprintf(gp, "plot \"GoldenerSchnitt.dat\" with lines;\n");
    pclose(gp);
  }

  return 0;
}
