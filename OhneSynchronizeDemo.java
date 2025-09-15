public class OhneSynchronizeDemo {
  public static void main(String[] args) {
    Punkt p = new Punkt();
    Schreiber s = new Schreiber(p);
    Leser l = new Leser(p);
    s.start();
    l.start();
  }
}

class Punkt {
  private int x = 0, y = 0;
    
  public String toString() { // Leser-Methode
    return "Punkt ["+x+"|"+y+"]";
  }
  public void setXY(int x, int y) { // Schreiber-Methode
    this.x = x;
    try {  
        Thread.sleep((int)(Math.random() * 100));
    } catch (InterruptedException e) { }        
    this.y = y;
  }
}

class Schreiber extends Thread {
  public Punkt p;
  public int z = 0;
  public Schreiber(Punkt p) {
    this.p = p;
  }
  public void run() {
    for(int i = 0; i < 5; i++) {
      z++; 
      p.setXY(z, z); // Der Schreiber schreibt
      try {  
          sleep(100);
      } catch (InterruptedException e) { }
    }
  }
}

class Leser extends Thread {
  public Punkt p;
  public Leser(Punkt p) {
    this.p = p;
  }
  public void run() {
    for(int i = 0; i < 5; i++) {
      System.out.println(p); // Der Leser liest
      try {  
          sleep(200);
      } catch (InterruptedException e) { }
    }
  }
}
