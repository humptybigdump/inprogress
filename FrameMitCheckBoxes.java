import java.awt.*;
import javax.swing.*;

/** Erzeuge ein Swing-Fenster mit CheckBoxes */
public class FrameMitCheckBoxes extends JFrame {
  Container c;            // Container dieses Frames
  // Feld fuer Check-Boxes, die im Frame erscheinen sollen
  JCheckBox cb[] = new JCheckBox[4];
  
  public FrameMitCheckBoxes() {  // Konstruktor
    c = getContentPane();             // Container bestimmen
    c.setLayout(new FlowLayout());    // Layout setzen
    
    // Erzeuge die Button-Objekte
    for (int i = 0; i < 4; i++) {
      cb[i] = new JCheckBox("Box " + (i+1));
      c.add(cb[i]);
    }

    cb[0].setSelected(true);
    cb[2].setSelected(true);
    
  }
  
  public static void main(String[] args) {
    FrameMitCheckBoxes fenster = new FrameMitCheckBoxes();
    fenster.setTitle("Frame mit CheckBoxes");
    fenster.setSize(280,70);
    fenster.setVisible(true);
    fenster.setLocation(300,300);
    fenster.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
  }
}
