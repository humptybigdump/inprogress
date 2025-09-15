import java.awt.*;
public class StartStopButton extends Button {
  private String alternateText;
  public StartStopButton (Color c) {
    setBackground(c);
    setFont(new Font("Arial",Font.PLAIN,25));
    setLabel("START");
    alternateText = "STOP";
  }
  public boolean isStart () {
    return getLabel().equals("START");
  }
  public void switchText () {
    String hlp = getLabel();
    setLabel(alternateText);
    alternateText = hlp;
  }
}

