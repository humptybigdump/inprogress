import java.io.*;
public class ZahlenSumme {
  public static void main (String args []){
    BufferedReader r = new BufferedReader(new InputStreamReader(System.in));
    StreamTokenizer st = new StreamTokenizer(r);
    System.out.println("Addiere alle Zahlen in einer Zeichenfolge");
    System.out.println("Eingabe der Zeichenfolge mit STOP abschliessen");
    StringBuffer woerter = new StringBuffer(); 
    int tokenType; 	
    double sum = 0.0; 	
    boolean stop = false;
    try {
      do {
        switch(tokenType = st.nextToken()) {
          case StreamTokenizer.TT_NUMBER:	
            sum += st.nval; 
            break;				
          case StreamTokenizer.TT_WORD: 
            if (!(stop=st.sval.equals("STOP"))) 
              woerter.append(st.sval); 
            break;
        }
      } while (!stop);
    } 
    catch (IOException e){
    };
    System.out.println("\nSumme aller Zahlen: " + sum);
    System.out.println("Text: " + woerter.toString());
  }
}  

