import java.awt.*;
import javax.swing.*;
public class FrameMitFlowLayout extends JFrame {
  Container c;                  
  JLabel l[] = new JLabel[4];   // Feld fuer Labels
  Font schrift = new Font("Serif",Font.ITALIC,28);
  public FrameMitFlowLayout() { 
    c = getContentPane();        
    c.setLayout(new FlowLayout());
    for (int i = 0; i < 4; i++) {
      l[i] = new JLabel("Nr. " + (i+1));
      l[i].setForeground(Color.WHITE); 
      l[i].setBackground(Color.BLACK);
      l[i].setFont(schrift);
      l[i].setOpaque(true);
      c.add(l[i]);
    }
  }
  
  public static void main(String[] args) {
    FrameMitFlowLayout fenster = new FrameMitFlowLayout();
    fenster.setTitle("Frame mit Flow-Layout");
    fenster.setSize(150,150);
    fenster.setVisible(true);
    fenster.setLocation(300,300);
    fenster.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
  }
}
