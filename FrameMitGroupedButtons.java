import java.awt.*;
import javax.swing.*;

/** Erzeuge ein Swing-Fenster mit gruppierten Toggle-Buttons */
public class FrameMitGroupedButtons extends JFrame {
  Container c;            // Container dieses Frames
  // Feld fuer Toggle-Buttons, die im Frame erscheinen sollen
  JToggleButton b[] = new JToggleButton[4];
  
  public FrameMitGroupedButtons() {  // Konstruktor
    c = getContentPane();             // Container bestimmen
    c.setLayout(new FlowLayout());    // Layout setzen
    
    // Gruppe erzeugen
    ButtonGroup bg = new ButtonGroup();

    // Erzeuge die Button-Objekte und fuege
    // sie dem Frame und der Gruppe hinzu
    for (int i = 0; i < 4; i++) {
      b[i] = new JToggleButton("Schalter " + (i+1));
      b[i].setFont(new Font("SansSerif",Font.ITALIC,24));
      c.add(b[i]);   // dem Frame hinzufuegen
      bg.add(b[i]);  // der Gruppe hinzufuegen
    }
    
    b[1].setSelected(true);
    
  }
  
  public static void main(String[] args) {
    FrameMitGroupedButtons fenster = new FrameMitGroupedButtons();
    fenster.setTitle("Frame mit gruppierten Buttons");
    fenster.setSize(330,130);
    fenster.setVisible(true);
    fenster.setLocation(300,300);
    fenster.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
  }
}
