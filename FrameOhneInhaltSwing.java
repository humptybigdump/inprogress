import javax.swing.*;

/** Erzeuge ein einfaches Swing-Fenster auf dem Bildschirm */
public class FrameOhneInhaltSwing {
  // Hauptmethode
  public static void main(String[] args) {
    // Erzeuge ein Fenster-Objekt
    JFrame fenster = new JFrame();
    // Setze den Titel des Fensters
    fenster.setTitle("Mein erstes Swing-Fenster");
    // Setze die Groesse des Fensters
    fenster.setSize(300,150);
    // Stelle das Fenster dar  
    fenster.setVisible(true);
    fenster.setLocation(300,300);
    // Setze das Verhalten des Frames beim Schliessen
    fenster.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
  }
}
