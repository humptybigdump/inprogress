import java.awt.*;
import javax.swing.*;
public class FrameMitGridLayout extends JFrame {
  Container c;
  JLabel l[] = new JLabel[6];
  public FrameMitGridLayout() {
    c = getContentPane();
    c.setLayout(new GridLayout(2,3,10,40));
    for (int i = 0; i < 6; i++) {
      l[i] = new JLabel("Nummer " + (i+1)); 
      l[i].setForeground(Color.RED); 
      l[i].setBackground(Color.YELLOW);
      l[i].setFont(new Font("Serif",Font.ITALIC,10 + i*3));
      l[i].setOpaque(true);
      c.add(l[i]);
    }
  }
  
  public static void main(String[] args) {
    FrameMitGridLayout fenster = new FrameMitGridLayout();
    fenster.setTitle("Frame mit Grid-Layout");
    fenster.setSize(300,150);
    fenster.setVisible(true);
    fenster.setLocation(300,300);
    fenster.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
  }
}
