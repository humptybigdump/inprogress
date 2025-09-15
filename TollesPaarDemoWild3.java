public class TollesPaarDemoWild3 {
  public static void paarAusgeben3(TollesPaar<?> tp){
    Object o = tp;
    System.out.println(o);
  }
  public static void main(String [] args) {
    Hose ho1 = new Hose();
    Hose ho2 = new Hose();
    TollesPaar<Hose> p1 = new TollesPaar<Hose> (ho1,ho2);
    paarAusgeben3(p1);
  }
}
