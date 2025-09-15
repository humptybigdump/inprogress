import javax.swing.*;
import static javax.swing.UIManager.*;

public class LookAndFeelTest {
  public static void main(String[] args) {
    for (LookAndFeelInfo info : UIManager.getInstalledLookAndFeels()) {
       System.out.println(info);
//         if ("Nimbus".equals(info.getName())) {
//            UIManager.setLookAndFeel(info.getClassName());
//            break;
    }
  }
}
