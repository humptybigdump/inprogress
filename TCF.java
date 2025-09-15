class TCF {
  public static int[] feld = {1,2,3};
  public static void m(int i) {
    System.out.println ("m(" + i + ") Start");
    try {
      System.out.println("try!");
      System.out.println(1/i);
      System.out.println(feld[i]);
    }  
    catch (ArithmeticException ae) {
      System.out.println("Erstes catch!");
    }
    catch (ArrayIndexOutOfBoundsException aie) {
      System.out.println("Zweites catch!");
      return;
    }
    finally {
      System.out.println("finally!");
    }
    System.out.println ("m(" + i + ") Ende");
  }
  public static void main(String args[]){
    m(1);
    m(0);
    m(5);
  }
}
