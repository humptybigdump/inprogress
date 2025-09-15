public class GenPaarDemo1 {
  public static void main(String[] args) {
    Socke s1 = new Socke();
    Socke s2 = new Socke();
    GenPaar<Socke> sockenPaar = new GenPaar<Socke>(s1,s2);
    System.out.println("1. Paar: " + sockenPaar);
    Ohrring o1 = new Ohrring();
    Ohrring o2 = new Ohrring();
    GenPaar<Ohrring> ohrringPaar = new GenPaar<Ohrring>(o1,o2);
    System.out.println("2. Paar: " + ohrringPaar);
    Socke s = sockenPaar.getL();
    System.out.println(s);
  }
}
