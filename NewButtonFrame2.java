import javax.swing.*;
import java.awt.event.*; 
import java.awt.*; 
public class NewButtonFrame2 extends JFrame {
  Container c; 
  JButton b;
  
  public NewButtonFrame2() {
    c = getContentPane(); 
    c.setLayout(new FlowLayout(FlowLayout.LEFT));
    b = new JButton("Drueck mich!");
    b.addActionListener(new ButtonBearbeiter());
    c.add(b);
  }
  
  class ButtonBearbeiter implements ActionListener {
    public void actionPerformed(ActionEvent e) { 
      c.add(new JButton("noch einer"));
      c.revalidate();
    }  
  }

  public static void main(String[] args) {
    JFrame fenster = new NewButtonFrame2();
    fenster.setTitle("Buttons hinzufuegen");
    fenster.setSize(500,300);
    fenster.setLocation(300,300);
    fenster.setVisible(true);
    fenster.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
  }
}

