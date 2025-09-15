class Student extends Mensch implements Sleeper {
  int matrNr;
  public void wakeUp() {
    for (long i=1; i<=ONE_MINUTE; i++)
      System.out.println("Chhrrrzzzzz..."); 
    System.out.println("Richtig wach bin ich immer noch nicht!"); 
  }
}
