import java.util.*;
public class Stoppuhr {
  static Scanner in = new Scanner(System.in);
  public static void main (String[] args) {
    System.out.print("Stoppuhr starten mit Eingabetaste!");
    in.nextLine();
    Date start = new Date();
    System.out.println("Startzeitpunkt: " + start);
    System.out.println();
    System.out.println("Die Stoppuhr laeuft ...");
    System.out.println();
    System.out.print("Stoppuhr anhalten mit Eingabetaste!");
    in.nextLine();
    Date stopp = new Date();
    System.out.println("Stoppzeitpunkt: " + stopp);
    System.out.println();
    long laufzeit = stopp.getTime() - start.getTime();
    System.out.println("Gesamtlaufzeit: " + laufzeit + " ms");
  }
}
