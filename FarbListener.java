import java.awt.*;
import java.awt.event.*;

class FarbListener implements ActionListener {
  private Color col;
  private Component comp; 
  FarbListener(Color col, Component comp) {
    this.col = col;
    this.comp = comp;
  }
  public void actionPerformed(ActionEvent e) {
    comp.setBackground(col);
  }
}
