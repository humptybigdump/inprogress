import java.awt.*;
import javax.swing.*;
import java.awt.event.*;

public class FarbComboBox extends JFrame {
  Container c;
  JComboBox<String> farben;
  public FarbComboBox() {
    c = getContentPane();
    c.setLayout(new FlowLayout());
    farben = new JComboBox<String>();
    farben.addItem("Blau");
    farben.addItem("Gelb");
    farben.addItem("Rot");
    farben.addItem("Grau");
    c.add(farben);
    farben.addItemListener(new ColorListener(c));
  }
  
  public static void main(String[] args) {
    FarbComboBox fenster = new FarbComboBox();
    fenster.setTitle("FarbComboBox");
    fenster.setSize(240,160);
    fenster.setVisible(true);
    fenster.setLocation(300,300);
    fenster.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
  }
}
