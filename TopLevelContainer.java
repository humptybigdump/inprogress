import javax.swing.*;

/** Erzeuge Top-Level-Container auf dem Bildschirm */
public class TopLevelContainer {
  public static void main(String[] args) {
    // Hauptfenster erzeugen und beschriften
    JFrame f = new JFrame();
    f.getContentPane().add(new JLabel("Frame",JLabel.CENTER));
    f.setTitle("Frame");
    f.setSize(300,150);
    f.setLocation(100,100);
    f.setVisible(true);
    f.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
    
    // Unterfenster (Window) erzeugen und beschriften
    JWindow w = new JWindow(f);
    w.getContentPane().add(new JLabel("Window",JLabel.CENTER));
    w.setSize(150,150);
    w.setLocation(410,100);
    w.setVisible(true);

    // Modales Unterfenster (Dialog) erzeugen und beschriften
    JDialog d = new JDialog(f,true);
    d.getContentPane().add(new JLabel("Dialog",JLabel.CENTER));
    d.setTitle("Dialog");
    d.setSize(150,100);
    d.setLocation(300,180);
    d.setVisible(true);
    d.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
  }
}
