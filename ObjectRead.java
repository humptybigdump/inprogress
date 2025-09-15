import java.io.*;
public class ObjectRead {
  public static void main (String[] summand) {
    try {
      // Dateiname fuer die Speicherung festlegen
      String dateiname = "MeineDaten.dat";
      // Datenstrom zum Lesen aus der Datei erzeugen
      FileInputStream datEin = new FileInputStream(dateiname);
      // Objektstrom darueberlegen
      ObjectInputStream oEin = new ObjectInputStream(datEin);
      // Datensaetze aus der Datei lesen und deren Datensatzfelder 
      // zur Kontrolle auf den Bildschirm ausgeben
      int anzahl = oEin.readInt();
      System.out.println("Die Datei " + dateiname + " enthaelt " + 
                          anzahl + " Datensaetze");
      for (int i=1; i<=anzahl; i++) {
        Datensatz gelesen = (Datensatz) oEin.readObject(); 
        System.out.println(gelesen);
      }
      // Dateistrom schliessen
      oEin.close();
    }
    catch (Exception e) {
      System.out.println("Fehler beim Lesen: " + e);
    }
  }
}
