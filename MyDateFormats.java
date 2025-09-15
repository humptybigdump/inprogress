import java.text.*;
import java.util.*;
public class MyDateFormats {
  public static final SimpleDateFormat 
    eins = new SimpleDateFormat("dd.MM.yyyy' um 'HH:mm:ss:S"),
    zwei = new SimpleDateFormat("EE, MMM d, ''yy"),
    drei = new SimpleDateFormat("H:mm"),
    vier = new SimpleDateFormat("H' Uhr und 'm' Minuten'"),
    fuen = new SimpleDateFormat("d. MMMM yyyy'  'HH:mm"),
    sech = new SimpleDateFormat("EE, d. MMM yyyy HH:mm:ss"),
    sieb = new SimpleDateFormat("yyMMddHHmmssS");
  public static void main (String[] args) {
    Date d = new Date();
    System.out.println (eins.format(d));
    System.out.println (zwei.format(d));
    System.out.println (drei.format(d));
    System.out.println (vier.format(d));
    System.out.println (fuen.format(d));
    System.out.println (sech.format(d));
    System.out.println (sieb.format(d));
  }
}
