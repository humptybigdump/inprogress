import java.awt.*;
import javax.swing.*;

/** Erzeuge ein einfaches Swing-Fenster mit einem Textlabel */
public class FrameMitText extends JFrame {
  Container c;          // Container dieses Frames
  JLabel beschriftung;  // Label, das im Frame erscheinen soll

  // Konstruktor fuer unseren Frame mit Textlabel
  public FrameMitText() {
    // Bestimme die Referenz auf den eigenen Container           
    c = getContentPane();
    // Setze das Layout
    c.setLayout(new FlowLayout());
    // Erzeuge das Labelobjekt mit Uebergabe des Labeltextes
    beschriftung = new JLabel("Label-Text im Frame");
    // Fuege das Label dem Frame hinzu
    c.add(beschriftung);
  }
  
  public static void main(String[] args) {
    FrameMitText fenster = new FrameMitText();
    fenster.setTitle("Frame mit Text im Label");
    fenster.setSize(300,150);
    fenster.setVisible(true);
    fenster.setLocation(300,300);
    fenster.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
  }
}
