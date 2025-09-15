import java.awt.*;
import javax.swing.*;

/** Erzeuge ein einfaches Swing-Fenster mit mehreren Panels */
public class FrameMitPanels extends JFrame {
  Container c;          // Container dieses Frames
  JPanel jp1, jp2, jp3; // Panels

  // Konstruktor fuer unseren Frame mit Textlabel
  public FrameMitPanels() {
    c = getContentPane();            // Container bestimmen 

    // Panels erzeugen
    jp1 = new JPanel();
    jp2 = new JPanel();
    jp3 = new JPanel(new GridLayout(2,3));
    
    // Vier Tasten in Panel 1 einfuegen
    for (int i=1; i<=4; i++)
      jp1.add(new JButton("Taste " + i));

    // Bildobjekt erzeugen
    Icon bild = new ImageIcon("babycatSmall.jpg");

    // Bild drei mal in Panel 2 einfuegen
    for (int i=1; i<=3; i++)
      jp2.add(new JLabel(bild));

    // Sechs Haekchen-Kaestchen in Panel 3 einfuegen
    for (int i=1; i<=6; i++)
      jp3.add(new JCheckBox("B"+i));

    // Panels in den Container einfuegen
    c.add(jp1,BorderLayout.NORTH);
    c.add(jp2,BorderLayout.CENTER);
    c.add(jp3,BorderLayout.SOUTH);
  }
  
  public static void main(String[] args) {
    FrameMitPanels fenster = new FrameMitPanels();
    fenster.setTitle("Label mit Panels");
    fenster.setSize(350,200);
    fenster.setVisible(true);
    fenster.setLocation(300,300);
    fenster.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
  }
}
