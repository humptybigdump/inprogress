import javax.swing.*;
import java.awt.*;
import java.awt.event.*;

/** Spezielle JPanel-Klasse */
public class Zeichenbrett extends JPanel {
  private int[] x, y;  // Koordinaten der Maus-Klicks
  private int n;       // Anzahl Klicks

  // Konstruktor
  public Zeichenbrett() {
    n = 0;
    x = new int[1000];
    y = new int[1000];  
    addMouseListener(new ClickBearbeiter());
  }

  // paintComponent ueberschreiben
  public void paintComponent(Graphics g) { 
    g.drawPolyline(x,y,n);
  }
  
  // Listener-Klasse fuer Maus-Ereignisse
  class ClickBearbeiter extends MouseAdapter {
    public void mousePressed(MouseEvent e) { 
      x[n] = e.getX(); // speichere x-Koordinate
      y[n] = e.getY(); // speichere y-Koordinate
      n++;             // erhoehe Anzahl Klicks
      repaint();       // Neuzeichnen der Komponente beim 
                       // Repaint-Manager anfordern
    }
  }
}
