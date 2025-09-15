public class PaarDemo1 {
  public static void main(String[] args) {
    Socke s1 = new Socke();
    Socke s2 = new Socke();
    Paar sockenPaar = new Paar (s1,s2);
    System.out.println("1. Paar: " + sockenPaar);
    Ohrring o1 = new Ohrring();
    Ohrring o2 = new Ohrring();
    Paar ohrringPaar = new Paar (o1,o2);
    System.out.println("2. Paar: " + ohrringPaar);
    Socke s = (Socke) sockenPaar.getL();
    System.out.println("Links in Paar 1: " + s);
  }
}
