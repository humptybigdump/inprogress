class SleeperDemo {
  static void check (Sleeper s) {
    s.wakeUp();
  }
  public static void main(String[] args) {
    Sleeper s = new Circle(5,0,0);
    check(s);
    s = new Student();
    check(s);
  }
}
