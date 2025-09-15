import java.awt.*;
import java.awt.event.*;
import javax.swing.*;

/** Farbwechsel-Klasse mit separater Listener-Klasse */
public class Farbwechsel4 extends JFrame {
  Container c;           // Container dieses Frames
  JButton button;        // Knopf
  
  // Konstruktor
  public Farbwechsel4() {    
    // Container bestimmen
    c = getContentPane();        
    // Button erzeugen und dem Container hinzufuegen
    button = new JButton("Hintergrundfarbe wechseln");
    c.add(button, BorderLayout.NORTH);

    // Listener-Objekt erzeugen und beim Button registrieren
    ButtonListener bL = new ButtonListener(c);
    button.addActionListener(bL);
  }
  
  // main-Methode
  public static void main(String[] args) {
     Farbwechsel4 fenster = new Farbwechsel4();
     fenster.setTitle("Farbwechsel");
     fenster.setSize(200,100);
     fenster.setVisible(true);
     fenster.setLocation(300,300);
     fenster.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
  }
}
