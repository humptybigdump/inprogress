public class TollesPaarDemoWild1 {
  public static void paarAusgeben1(TollesPaar<Kleidung> tp){
    System.out.println(tp);
  }
  public static void main(String [] args) {
    Hose ho1 = new Hose();
    Hose ho2 = new Hose();
    TollesPaar<Hose> p1 = new TollesPaar<Hose> (ho1,ho2);
    paarAusgeben1(p1);
  }
}
