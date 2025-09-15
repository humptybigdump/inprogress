public class StandardFormat {
  public static void main (String[] args) {
    double x = 1e-15;
    for (int i=1; i<=13; i++) {
      System.out.println(x);
      x = 111 * x;
    }
  }
}
