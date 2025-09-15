import java.awt.*;
import javax.swing.*;

/** Erzeuge ein Swing-Fenster mit ScrollTextArea */
public class FrameMitScrollText extends JFrame {
  Container c;            // Container dieses Frames
  JLabel info;            // Label
  JTextArea ta;           // TextArea
  JScrollPane sp;         // ScrollPane
  
  public FrameMitScrollText() {    // Konstruktor
    c = getContentPane();             // Container bestimmen
    
    // Erzeuge Label und TextArea
    info = new JLabel("Hier kann Text bearbeitet werden");
    ta = new JTextArea("Einiges an Text steht auch schon hier rum.");

    // Setze die Schriftart
    Font schrift = new Font("SansSerif",Font.BOLD+Font.ITALIC,16);
    ta.setFont(schrift);
    
    ta.setLineWrap(true);        // Automatischer Zeilenumbruch
    ta.setWrapStyleWord(true);   // wortweise

    sp = new JScrollPane(ta);    // Scrollpane erzeugen

    // Fuege die Komponenten hinzu
    c.add(info,BorderLayout.NORTH);
    c.add(sp);
  }
  
  public static void main(String[] args) {
    FrameMitScrollText fenster = new FrameMitScrollText();
    fenster.setTitle("Frame mit ScrollTextArea");
    fenster.setSize(250,160);
    fenster.setVisible(true);
    fenster.setLocation(300,300);
    fenster.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
  }
}
