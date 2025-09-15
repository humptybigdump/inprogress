import java.awt.*;
import javax.swing.*;
public class FrameMitBorderLayout extends JFrame {
  Container c;
  JLabel l[] = new JLabel[5];
  public FrameMitBorderLayout() {    // Konstruktor
    c = getContentPane();
    c.setLayout(new BorderLayout());
    l[0] = new JLabel("Hier ist der total kalte Norden");
    l[1] = new JLabel("Hier ist der echt warme Sueden");
    l[2] = new JLabel("Osten");
    l[3] = new JLabel("Westen");
    l[4] = new JLabel("Zentrum");
    
    l[4].setBackground(Color.YELLOW);
    l[4].setOpaque(true);
    c.add(l[0],BorderLayout.NORTH);
    c.add(l[1],BorderLayout.SOUTH);
    c.add(l[2],BorderLayout.EAST);
    c.add(l[3],BorderLayout.WEST);
    c.add(l[4],BorderLayout.CENTER);
  }
  
  public static void main(String[] args) {
    FrameMitBorderLayout fenster = new FrameMitBorderLayout();
    fenster.setTitle("Frame mit Border-Layout");
    fenster.setSize(200,100);
    fenster.setVisible(true);
    fenster.setLocation(300,300);
    fenster.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
  }
}

