public class WurzelMultiCatch {
  public static void main (String[] args) {
    try {
        double erg = Math.sqrt(Double.parseDouble(args[0]));
        System.out.println(erg);
    } catch (ArrayIndexOutOfBoundsException 
             | NumberFormatException me) {
        System.out.println("Aufruf unzulaessig, da kein " +
                           "double-Parameter angegeben!");
    } catch (Exception e) {
        e.printStackTrace();
    }
  }
}


/*


java WurzelMultiCatch 17
4.123105625617661

java WurzelMultiCatch a46
Aufruf unzulaessig, da kein double-Parameter angegeben!

java WurzelMultiCatch
Aufruf unzulaessig, da kein double-Parameter angegeben!

java WurzelMultiCatch -4
NaN


*/
