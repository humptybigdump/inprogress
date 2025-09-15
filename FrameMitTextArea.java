import java.awt.*;
import javax.swing.*;

/** Erzeuge ein Swing-Fenster mit TextArea */
public class FrameMitTextArea extends JFrame {
  Container c;            // Container dieses Frames
  JLabel info;            // Label
  JTextArea ta;           // TextArea
  
  public FrameMitTextArea() {    // Konstruktor
    c = getContentPane();             // Container bestimmen
    
    // Erzeuge Label und TextArea
    info = new JLabel("Hier kann Text bearbeitet werden");
    ta = new JTextArea("Einiges an Text steht auch schon hier rum.");

    // Setze die Schriftart
    Font schrift = new Font("SansSerif",Font.BOLD+Font.ITALIC,16);
    ta.setFont(schrift);
    
    // Automatischen Umbruch aktivieren
    ta.setLineWrap(true);
    ta.setWrapStyleWord(true);

    // Fuege die Komponenten hinzu
    c.add(info,BorderLayout.NORTH);
    c.add(ta);
  }
  
  public static void main(String[] args) {
    FrameMitTextArea fenster = new FrameMitTextArea();
    fenster.setTitle("Frame mit TextArea");
    fenster.setSize(200,160);
    fenster.setVisible(true);
    fenster.setLocation(300,300);
    fenster.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
  }
}
