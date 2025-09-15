public class GenPaarDemoWild3 {
  public static void genPaarAusgeben3(GenPaar<? super Hose> gp){
    System.out.println(gp);
  }
  public static void main(String [] args) {
    Jeans j1 = new Jeans();
    Jeans j2 = new Jeans();
    GenPaar<Jeans> p1 = new GenPaar<Jeans> (j1,j2);
    genPaarAusgeben3(p1);
  }
}
