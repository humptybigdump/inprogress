import javax.swing.*;

/** Erzeuge ein einfaches Swing-Fenster auf dem Bildschirm */
public class FrameOhneInhalt extends JFrame {
  // Konstruktor fuer unseren Frame
  public FrameOhneInhalt () {
    // Hier werden spaeter die Komponenten hinzugefuegt
  }
  
  public static void main(String[] args) {
    // Erzeuge eine Instanz unseres Frames
    FrameOhneInhalt fenster = new FrameOhneInhalt();
    // Titelleiste definieren
    fenster.setTitle("Frame ohne Inhalt");
    // Setze die Groesse des Frames
    fenster.setSize(300,150);
    // Schalte den Frame sichtbar
    fenster.setVisible(true);
    fenster.setLocation(300,300);
    // Setze das Verhalten des Frames beim Schliessen
    fenster.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
  }
}
