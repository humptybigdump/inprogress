public class PaarDemo2 {
  public static void main(String[] args) {
    Ohrring o = new Ohrring();
    Socke s = new Socke();
    Paar komischesPaar = new Paar(o,s);
    System.out.println("Komisches Paar: " + komischesPaar);
    s = (Socke) komischesPaar.getL();
    System.out.println("Links ist " + s);
  }
}
