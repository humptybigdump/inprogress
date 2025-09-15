import java.awt.*;
import java.awt.event.*;
import javax.swing.*;

/** Farbwechsel-Klasse selbst als Listener */
public class Farbwechsel3 extends JFrame implements ActionListener {
  Container c;           // Container dieses Frames
  JButton button;        // Knopf
  
  // Konstruktor
  public Farbwechsel3() {    
    // Container bestimmen
    c = getContentPane();        
    // Button erzeugen und dem Container hinzufuegen
    button = new JButton("Hintergrundfarbe wechseln");
    c.add(button, BorderLayout.NORTH);

    // Eigenes Objekt beim Button als Listener registrieren
    button.addActionListener(this);
  }
  
  // Implementierung der Methode des ActionListener-Interface
  public void actionPerformed(ActionEvent e) {
    // Hintergrundfarbe des Containers zufaellig aendern
    float zufall = (float) Math.random();             
    Color grauton = new Color(zufall,zufall,zufall);
    c.setBackground(grauton);
  }

  // main-Methode
  public static void main(String[] args) {
     Farbwechsel3 fenster = new Farbwechsel3();
     fenster.setTitle("Farbwechsel");
     fenster.setSize(200,100);
     fenster.setVisible(true);
     fenster.setLocation(300,300);
     fenster.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
  }
}
