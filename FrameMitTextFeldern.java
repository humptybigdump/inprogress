import java.awt.*;
import javax.swing.*;

/** Erzeuge ein Swing-Fenster mit Textfeldern */
public class FrameMitTextFeldern extends JFrame {
  Container c;            // Container dieses Frames
  JLabel name, passwd;    // Labels
  JTextField tf;          // Textfeld
  JPasswordField pf;      // Passwortfeld
  
  public FrameMitTextFeldern() {    // Konstruktor
    c = getContentPane();             // Container bestimmen
    c.setLayout(new GridLayout(2,2)); // Layout setzen
    
    // Erzeuge die Labels und Textfelder
    name = new JLabel("Name:",JLabel.RIGHT);
    passwd = new JLabel("Passwort:",JLabel.RIGHT);
    tf = new JTextField();
    pf = new JPasswordField();

    // Setze die Schriftart
    Font schrift = new Font("SansSerif",Font.BOLD,18);
    name.setFont(schrift);
    passwd.setFont(schrift);
    tf.setFont(schrift);
    pf.setFont(schrift);
    

    // Fuege die Komponenten hinzu
    c.add(name);
    c.add(tf);
    c.add(passwd);
    c.add(pf);
  }
  
  public static void main(String[] args) {
    FrameMitTextFeldern fenster = new FrameMitTextFeldern();
    fenster.setTitle("Frame mit Textfeldern");
    fenster.setSize(220,100);
    fenster.setVisible(true);
    fenster.setLocation(300,300);
    fenster.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
  }
}
