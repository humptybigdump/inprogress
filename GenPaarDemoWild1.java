public class GenPaarDemoWild1 {
  public static void genPaarAusgeben1(GenPaar<? extends Hose> gp){
    System.out.println(gp);
  }
  public static void main(String [] args) {
    Jeans j1 = new Jeans();
    Jeans j2 = new Jeans();
    GenPaar<Jeans> p1 = new GenPaar<Jeans> (j1,j2);
    genPaarAusgeben1(p1);
  }
}
