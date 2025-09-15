import java.awt.*;
import javax.swing.*;

/** Erzeuge ein Swing-Fenster mit RadioButtons */
public class FrameMitRadioButtons extends JFrame {
  Container c;            // Container dieses Frames
  // Feld fuer Radio-Buttons, die im Frame erscheinen sollen
  JRadioButton rb[] = new JRadioButton[4];
  
  public FrameMitRadioButtons() {  // Konstruktor
    c = getContentPane();             // Container bestimmen
    c.setLayout(new FlowLayout());    // Layout setzen
    
    // Gruppe erzeugen
    ButtonGroup bg = new ButtonGroup();

    // Erzeuge die Button-Objekte und fuege  
    // sie dem Frame und der Gruppe hinzu
    for (int i = 0; i < 4; i++) {
      rb[i] = new JRadioButton("Box " + (i+1)); // erzeugen
      bg.add(rb[i]); // der Gruppe hinzufuegen
      c.add(rb[i]);  // dem Frame hinzufuegen
    }
  }
  
  public static void main(String[] args) {
    FrameMitRadioButtons fenster = new FrameMitRadioButtons();
    fenster.setTitle("Frame mit RadioButtons");
    fenster.setSize(330,70);
    fenster.setVisible(true);
    fenster.setLocation(300,300);
    fenster.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
  }
}
