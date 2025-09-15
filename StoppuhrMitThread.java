import java.util.*;
public class StoppuhrMitThread {
  static Scanner in = new Scanner(System.in);
  public static void main (String[] args) {
    // Auf Betaetigen der Eingabetaste warten
    System.out.println("Stoppuhr starten mit Eingabetaste!");
    in.nextLine();
    // Aktuellen Zeitpunkt im Date-Objekt start festhalten
    Date start = new Date();
    // Zeitpunkt ausgeben
    System.out.println("Startzeitpunkt: " + start);
    System.out.println();
    System.out.println("Stoppuhr anhalten mit Eingabetaste!");
    // Anzeige-Thread starten
    Thread t = new UhrzeitThread();
    t.start();    
    // Auf Betaetigen der Eingabetaste warten
    in.nextLine();
    // Aktuellen Zeitpunkt im Date-Objekt stopp festhalten
    Date stopp = new Date();
    // Anzeige-Thread anhalten
    t.interrupt();
    // Zeitpunkt ausgeben
    System.out.println("Stoppzeitpunkt: " + stopp);
    System.out.println();
    // Laufzeit als Differenz von stopp und start bestimmen
    long laufzeit = stopp.getTime() - start.getTime();
    // Laufzeit ausgeben
    System.out.println("Gesamtlaufzeit: " + laufzeit + " ms");
  }
}
