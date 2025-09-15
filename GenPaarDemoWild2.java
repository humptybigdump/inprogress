public class GenPaarDemoWild2 {
  public static void genPaarAusgeben2(GenPaar<? super Hose> gp){
    System.out.println(gp);
  }
  public static void main(String [] args) {
    Kleidung k1 = new Kleidung();
    Kleidung k2 = new Kleidung();
    GenPaar<Kleidung> p1 = new GenPaar<Kleidung> (k1,k2);
    genPaarAusgeben2(p1);
  }
}
