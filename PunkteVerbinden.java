import java.awt.*;
import java.awt.event.*;
import javax.swing.*;

/** Erzeuge ein Swing-Fenster mit einem Zeichenbrett */
public class PunkteVerbinden extends JFrame {
  Container c;           // Container dieses Frames
  Zeichenbrett z;        // Zeichenbrett zum Linien Malen
  
  // Konstruktor
  public PunkteVerbinden() {
    // Bestimme die Referenz auf den eigenen Container
    c = getContentPane();
    // Erzeuge neues Zeichenbrett und fuege es dem Frame hinzu
    z = new Zeichenbrett();
    c.add(z);
  }
  
  // main-Methode
  public static void main(String[] args) {
     PunkteVerbinden fenster = new PunkteVerbinden();
     fenster.setTitle("Punkte verbinden");
     fenster.setSize(250,200);
     fenster.setLocation(300,300);
     fenster.setVisible(true);
     fenster.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
  }
}
