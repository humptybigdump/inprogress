import java.util.*;
public class StringTokens {
  public static void main(String[] args) throws Exception {
    String text = "Ein toller Text";  // zu zerlegende Zeichenkette
    StringTokenizer st1 = new StringTokenizer(text);
    String delim = "eo";  // Trennzeichen zwischen den Tokens
    StringTokenizer st2 = new StringTokenizer(text, delim);
    while (st1.hasMoreTokens())
      System.out.println(st1.nextToken());
    while (st2.hasMoreTokens())
      System.out.println(st2.nextToken());  
  }
}

