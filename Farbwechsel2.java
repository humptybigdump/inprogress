import java.awt.*;
import java.awt.event.*;
import javax.swing.*;

/** Farbwechsel-Klasse mit anonymer Listener-Klasse */
public class Farbwechsel2 extends JFrame {
  Container c;           // Container dieses Frames
  JButton button;        // Knopf
  
  // Konstruktor
  public Farbwechsel2() {    
    // Container bestimmen
    c = getContentPane();        
    // Button erzeugen und dem Container hinzufuegen
    button = new JButton("Hintergrundfarbe wechseln");
    c.add(button, BorderLayout.NORTH);

    // Listener-Objekt erzeugen und beim Button registrieren
    ActionListener bL = new ActionListener() {
        public void actionPerformed(ActionEvent e) {
          // Hintergrundfarbe des Containers zufaellig aendern
          float zufall = (float) Math.random();             
          Color grauton = new Color(zufall,zufall,zufall);
          c.setBackground(grauton);
        }
      }; // Ende der anonymen Klassendefinition
    button.addActionListener(bL);
  }
  
  // main-Methode
  public static void main(String[] args) {
     Farbwechsel2 fenster = new Farbwechsel2();
     fenster.setTitle("Farbwechsel");
     fenster.setSize(200,100);
     fenster.setVisible(true);
     fenster.setLocation(300,300);
     fenster.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
  }
}
