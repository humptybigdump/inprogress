import java.io.*;
public class WriteToFile {
  // Liest alle Zeichen aus r und schreibt sie in w
  public static void r2w(Reader r, Writer w) throws IOException {
    int c;                        // Zeichen
    while ((c = r.read()) != -1)  // lesen und auf Strom-Ende testen
      w.write(c);                 // ausgeben
    r.close();
    w.close(); 
  }

  // Liest Zeichen von der Tastatur und speichert sie in einer Datei
  public static void main(String[] args) {
    try {
      File datei = new File(args[0]);
      Reader in = new InputStreamReader(System.in);
      Writer out = new FileWriter(datei);

      System.out.println("Geben Sie jetzt den Text ein.");
      System.out.println("(Ende/Speichern mit Ctrl-Z bzw. Strg-Z)");
      System.out.println();
      
      r2w(in,out);

      in = new FileReader(datei);
      out = new OutputStreamWriter(System.out);

      System.out.println();
      System.out.println("Der in " + args[0] + " gespeicherte Text:");
      System.out.println();

      r2w(in,out);
    }
    catch(ArrayIndexOutOfBoundsException ae) {
      System.out.println("Aufruf:  java WriteToFile <Datei>");
    }
    catch(IOException e) {
      System.out.println(e);
    }
  }
}

