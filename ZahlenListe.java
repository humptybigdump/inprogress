import java.util.*;
class ZahlenListe {
 public static void main(String[] args) {
    Collection<Double> c = new ArrayList<Double>();
    c.add(4.4);
    c.add(2.2);
    c.add(3.3);
    c.add(0.0);
    c.add(3.3);
    c.add(1.1);
    System.out.println("vorher:\n" + c);
    c.remove(3.3);
    c.remove(0.0);
    c.remove(4.4);
    System.out.println("nachher:\n" + c);  
  }
}
