public class GenPaarDemo3 {
  public static <T> boolean linksGleichRechts (GenPaar<T> x){
    return x.getL().equals(x.getR());
  }
  public static <T> T links (GenPaar<T> x){
    return x.getL();
  }
   public static void main(String [] args) {
      Hose h1 = new Hose();
      Jeans j1 = new Jeans();
      GenPaar<Hose> p1 = new GenPaar<Hose> (h1,j1);
      System.out.println(linksGleichRechts(p1));
      System.out.println(links(p1));
  }
}
