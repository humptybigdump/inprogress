public class GenPaarDemo2 {
  public static void main(String[] args) {
    Ohrring o = new Ohrring();
    Socke s = new Socke();
    GenPaar<Socke> mix = new GenPaar<Socke>(o,s);  // unzulaessig
  }
}
