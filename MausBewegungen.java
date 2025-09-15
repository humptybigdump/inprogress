import java.awt.*;
import java.awt.event.*;
import javax.swing.*;
public class MausBewegungen extends JFrame {
  Container c;
  public MausBewegungen() {    
    c = getContentPane();
    Lauscher audi = new Lauscher();
    c.addMouseListener(audi);
  }
  
  // Innere Lauscher-Klasse
  class Lauscher implements MouseListener {
    public void mousePressed(MouseEvent e) {
      System.out.println("pressed at " + e.getX() + "|" + e.getY());
    }
    public void mouseReleased(MouseEvent e) {
      System.out.println("released at " + e.getX() + "|" + e.getY());
    }
    public void mouseClicked(MouseEvent e) { 
      System.out.println("clicked at " + e.getX() + "|" + e.getY());
    }
    public void mouseEntered(MouseEvent e) {
      System.out.println("entered");
    }
    public void mouseExited(MouseEvent e) {
      System.out.println("exited");
    }
  }
  
  // main-Methode
  public static void main(String[] args) {
     MausBewegungen fenster = new MausBewegungen();
     fenster.setTitle("Mausbewegungen");
     fenster.setSize(200,100);
     fenster.setVisible(true);
     fenster.setLocation(300,300);
     fenster.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
  }
}
