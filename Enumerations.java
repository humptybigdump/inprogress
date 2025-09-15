import typen.Noten;
import static typen.Noten.*;
public class Enumerations {
  public static void main(String[] args) {
    for (Noten n : Noten.values()) {
      System.out.println( n + " liegt auf einer " + 
                          n.tastenFarbe() + "en Taste" );
    }
  }
}
