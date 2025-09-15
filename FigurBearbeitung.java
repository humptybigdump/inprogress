class FigurBearbeitung {
  static void check (Figur f) {
    f.show();
    if (f.contains(1,2))
      System.out.println("Punkt (1,2) liegt drin.");
  }
  public static void main(String[] args) {
    Figur f = new Kreis(5,0,0);
    check(f);
    f = new RechtEckchen(10,10,6,17);
    check(f);
  }
}
