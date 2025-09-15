import java.awt.*;
import java.awt.event.*;
import javax.swing.*;

/** Erzeuge ein Swing-Fenster, das mit Buttons und 
 *  Combo-Box sein Look and feel aendern kann
 */
public class LookAndFeel extends JFrame {
  Container c;              // Container dieses Frames
  JButton b1, b2, b3, b4;   // Buttons
  JComboBox<String> cb;     // Combo-Box
  JFrame f = this;          // Referenz auf dieses Frame
  
  public LookAndFeel() {  // Konstruktor
    c = getContentPane();             // Container bestimmen
    c.setLayout(new FlowLayout());    // Layout setzen
    
    // Erzeuge die Buttons und die Combo-Box
    b1 = new JButton("Metal");
    b2 = new JButton("Motif");
    b3 = new JButton("Windows");
    b4 = new JButton("Nimbus");
    cb = new JComboBox<String>();
    cb.addItem("Metal");
    cb.addItem("Motif");
    cb.addItem("Windows");
    cb.addItem("Nimbus");

    // Fuege die Komponenten dem Frame hinzu
    c.add(b1);
    c.add(b2);
    c.add(b3);
    c.add(b4);
    c.add(cb);
    
    // Erzeuge den Listener und registriere ihn
    LafListener ll = new LafListener();
    b1.addActionListener(ll);
    b2.addActionListener(ll);
    b3.addActionListener(ll);
    b4.addActionListener(ll);
    cb.addItemListener(ll);
  }
  
  // Innere Listener-Klasse
  public class LafListener implements ItemListener,ActionListener {
    //
    String[] laf = 
               {"javax.swing.plaf.metal.MetalLookAndFeel",
                "com.sun.java.swing.plaf.motif.MotifLookAndFeel",
                "com.sun.java.swing.plaf.windows.WindowsLookAndFeel",
                "javax.swing.plaf.nimbus.NimbusLookAndFeel"};
        
    // Fuer das ItemListener-Interface
    public void itemStateChanged(ItemEvent e) {
      try {
        int i = cb.getSelectedIndex();
        UIManager.setLookAndFeel(laf[i]);
      }
      catch (Exception ex) {
        System.err.println(ex);
      }
      SwingUtilities.updateComponentTreeUI(f);
    }

    // Fuer das ActionListener-Interface
    public void actionPerformed(ActionEvent e) {
      try {
        int i;
        if (e.getSource() == b1)
          i = 0;
        else if (e.getSource() == b2) 
          i = 1;
        else if (e.getSource() == b3) 
          i = 2;
        else 
          i = 3;
        UIManager.setLookAndFeel(laf[i]);
        cb.setSelectedIndex(i);
      }
      catch (Exception ex) {
        System.err.println(ex);
      }
      SwingUtilities.updateComponentTreeUI(f);
    }
  }  
  
  public static void main(String[] args) {
    LookAndFeel fenster = new LookAndFeel();
    fenster.setTitle("Look and feel einstellen");
    fenster.setSize(500,100);
    fenster.setLocation(300,300);
    fenster.setVisible(true);
    fenster.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
  }
}
