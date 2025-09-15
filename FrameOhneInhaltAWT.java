import java.awt.*;

/** Erzeugt ein einfaches AWT-Fenster auf dem Bildschirm */
public class FrameOhneInhaltAWT {
  // Hauptmethode
  public static void main(String[] args) {
    // Erzeuge ein Fenster-Objekt
    Frame fenster = new Frame();
    // Setze den Titel des Fensters
    fenster.setTitle("Mein erstes AWT-Fenster");
    // Setze die Groesse des Fensters
    fenster.setSize(300,150);
    // Stelle das Fenster dar  
    fenster.setVisible(true);
    fenster.setLocation(300,300);
  }
}
