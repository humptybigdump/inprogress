public class GenPaarDemo5 {
  public static <T,S extends T> GenPaar<T> linksPaar 
                                        (GenPaar<T> x, GenPaar<S> y){
    return new GenPaar<T>(x.getL(),y.getL());
  }
  public static void main(String [] args) {
    Hose h1 = new Hose();
    Hose h2 = new Hose();
    Jeans j1 = new Jeans();
    Jeans j2 = new Jeans();
    GenPaar<Hose> p1 = new GenPaar<Hose> (h1,h2);
    GenPaar<Jeans> p2 = new GenPaar<Jeans> (j1,j2);
    System.out.println(linksPaar(p1,p2));
  }
}
