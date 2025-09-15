import java.awt.*;
import javax.swing.*;
public class FrameMitToolTipUndOpak extends JFrame {
  Container c; 
  JLabel l1, l2, l3;
  public FrameMitToolTipUndOpak() {
    c = getContentPane();
    c.setLayout(new FlowLayout());
    l1 = new JLabel("  Label-Text  ");
    c.add(l1);
    l1.setToolTipText("Des isch nur en Tescht!");
    l2 = new JLabel("  Nicht opak  ");
    l2.setBackground(Color.YELLOW);
    c.add(l2);
    l3 = new JLabel("  Opak  ");
    l3.setOpaque(true);
    l3.setBackground(Color.YELLOW);
    c.add(l3);
  }
  
  public static void main(String[] args) {
    FrameMitToolTipUndOpak fenster = new FrameMitToolTipUndOpak();
    fenster.setTitle("Frame mit Text im Label mit Tooltip");
    fenster.setSize(300,100);
    fenster.setVisible(true);
    fenster.setLocation(300,300);
    fenster.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
  }
}
