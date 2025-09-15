import java.awt.*;
import java.awt.event.*;
import javax.swing.*;

/** Erzeuge ein Swing-Fenster mit einem Button, der in der Lage
    ist die Hintergrundfarbe des Frames zufaellig zu aendern */
public class Farbwechsel extends JFrame {
  Container c;           // Container dieses Frames
  JButton button;        // Knopf
  
  // Konstruktor
  public Farbwechsel() {    
    // Container bestimmen
    c = getContentPane();        
    // Button erzeugen und dem Container hinzufuegen
    button = new JButton("Hintergrundfarbe wechseln");
    c.add(button, BorderLayout.NORTH);

    // Listener-Objekt erzeugen und beim Button registrieren
    ButtonListener bL = new ButtonListener();
    button.addActionListener(bL);
  }
  
  // Innere Button-Listener-Klasse
  class ButtonListener implements ActionListener {
    public void actionPerformed(ActionEvent e) {
      // Hintergrundfarbe des Containers zufaellig aendern
      float zufall = (float) Math.random();             
      Color grauton = new Color(zufall,zufall,zufall);
      c.setBackground(grauton);  // Zugriff auf c moeglich, da
    }                            // ButtonListener innere Klasse
  }
  
  // main-Methode
  public static void main(String[] args) {
     Farbwechsel fenster = new Farbwechsel();
     fenster.setTitle("Farbwechsel");
     fenster.setSize(200,100);
     fenster.setVisible(true);
     fenster.setLocation(300,300);
     fenster.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
  }
}
