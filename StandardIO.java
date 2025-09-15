import java.io.*;
public class StandardIO {
 public static void main (String args [])throws IOException {
  BufferedReader in = new BufferedReader(new InputStreamReader(System.in));
  String s = ""; 
  System.out.print("Textzeile eingeben: "); 
  s = in.readLine();
  System.out.println("gelesen: " + s);
  int Zahl = 0; 
  System.out.print("Zahl eingeben: ");
  Zahl = Integer.parseInt(in.readLine()); // transformiert die Zeichenfolge nach int
  System.out.println("verdoppelt: " + Zahl*2);
 }
}

