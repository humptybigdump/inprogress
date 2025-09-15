import javax.swing.*;

/** Erzeuge ein einfaches Swing-Fenster auf dem Bildschirm */
public class GrafischeOberfl extends JFrame {
  // Konstruktor fuer unseren Frame
  public GrafischeOberfl () {
    // Hier werden spaeter die Komponenten hinzugefuegt
  }
  
  public static void main(String[] args) {
    // Erzeuge eine Instanz unseres Frames
    GrafischeOberfl fenster = new GrafischeOberfl();
    // Titelleiste definieren
    fenster.setTitle("Grafische Oberflaechen");
    // Setze die Groesse des Frames
    fenster.setSize(300,150);
    // Schalte den Frame sichtbar
    fenster.setVisible(true);
    fenster.setLocation(300,300);
    // Setze das Verhalten des Frames beim Schliessen
    fenster.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
  }
}
