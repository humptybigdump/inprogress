import java.io.*;
public class ObjectWrite {
  public static void main (String[] summand) {
    try {
      // Dateiname fuer die Speicherung festlegen
      String dateiname = "MeineDaten.dat";
      // Datenstrom zum Schreiben in die Datei erzeugen
      FileOutputStream datAus = new FileOutputStream(dateiname);
      // Objektstrom darueber legen
      ObjectOutputStream oAus = new ObjectOutputStream(datAus);
      // Testdatensaetze erzeugen
      int anzahl = 2;  // Anzahl der Datensaetze
      Datensatz a = new Datensatz (99, 56, "Coca Cola");
      Datensatz b = new Datensatz (111, 1234.79, "Fahrrad");
      // Datensaetze in die Datei schreiben
      oAus.writeInt(anzahl);   // Anzahl der Datensaetze
      oAus.writeObject(a);     // Datensatz 1
      oAus.writeObject(b);     // Datensatz 2
      // Dateistrom schliessen
      oAus.close();
      System.out.println(anzahl + " Datensaetze in die Datei " + 
                         dateiname + " geschrieben");
      System.out.println(a);
      System.out.println(b);
    }
    catch (Exception e) {
      System.out.println("Fehler beim Schreiben: " + e);
    }
  }
}
