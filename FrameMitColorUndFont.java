import java.awt.*;
import javax.swing.*;

public class FrameMitColorUndFont extends JFrame {
  Container c;
  JLabel text1, text2;
  Color hell = new Color(250,250,250);
  Font mono = new Font("Monospaced",Font.BOLD+Font.ITALIC,30);

  public FrameMitColorUndFont() {  // Konstruktor
    c = getContentPane();               // Container bestimmen
    c.setLayout(new FlowLayout());      // Layout setzen

    c.setBackground(Color.BLACK);
    
    text1 = new JLabel("Helle Schrift");
    text1.setForeground(hell);
    
    text2 = new JLabel("Monospaced Text");
    text2.setForeground(hell);
    text2.setFont(mono);

    c.add(text1);
    c.add(text2);
  }

  public static void main(String[] args) {
    FrameMitColorUndFont fenster = new FrameMitColorUndFont();
    fenster.setTitle("Frame mit Color und Font");
    fenster.setSize(300,100);
    fenster.setVisible(true);
    fenster.setLocation(300,300);
    fenster.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
  }
}
