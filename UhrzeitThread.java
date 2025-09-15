import java.util.*;
import java.text.*;
public class UhrzeitThread extends Thread {
  public static final SimpleDateFormat  
    hms = new SimpleDateFormat("HH:mm:ss");
    
  public void run() {
    System.out.println();
    while (true) {
      if (isInterrupted()) {
        System.out.println();
        break;
      }
      Date time = new Date();
      System.out.print(hms.format(time)+"\b\b\b\b\b\b\b\b");
      try {
        sleep(1000);
      }
      catch (InterruptedException ie) {
        interrupt();
      }
    }
  }
}
