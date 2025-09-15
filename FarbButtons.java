import java.awt.*;
import java.awt.event.*;
import javax.swing.*;

public class FarbButtons extends JFrame {
  Container c; 
  JButton blau, gelb, rot, grau;
  
  public FarbButtons() {    
    c = getContentPane();
    c.setLayout(new FlowLayout());
    c.add(blau = new JButton("Blau"));
    blau.addActionListener(new FarbListener(Color.BLUE, c));
    c.add(gelb = new JButton("Gelb"));
    gelb.addActionListener(new FarbListener(Color.YELLOW, c));
    c.add(rot = new JButton("Rot"));
    rot.addActionListener(new FarbListener(Color.RED, c));
    c.add(grau = new JButton("Grau"));
    grau.addActionListener(new FarbListener(Color.GRAY, c));
  }
  
  // main-Methode
  public static void main(String[] args) {
     FarbButtons fenster = new FarbButtons();
     fenster.setTitle("FarbButtons");
     fenster.setSize(300,80);
     fenster.setVisible(true);
     fenster.setLocation(300,300);
     fenster.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
  }
}
