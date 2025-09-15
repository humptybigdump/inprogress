  class Wert {
    private int wert;
    public int get() {
      return wert;
    }
    public void put (int i) {
      wert = i;
    }
  }

  class Erzeuger extends Thread {
    Wert w;
    public Erzeuger (Wert w) {
      this.w = w;
    }
    public void run() {
      for (int i = 0; i < 5; i++) {
        w.put(i);
        System.out.println("Erzeuger put: " + i);
        try {
          sleep((int)(Math.random() * 100));
        } 
        catch (InterruptedException e) {
        }
      }
    }
  }

  class Verbraucher extends Thread {
    Wert w;
    public Verbraucher (Wert w) {
      this.w = w;
    }
    public void run() {
      int v;
      for (int i = 0; i < 5; i++) {
        v = w.get();
        System.out.println("Verbraucher get: " + v);
        try {
          sleep((int)(Math.random() * 100));
        } 
        catch (InterruptedException e) {
        }
      }
    }
  }

  public class EVTest {
    public static void main (String args[]) {
      Wert        w = new Wert();
      Erzeuger    e = new Erzeuger(w);
      Verbraucher v = new Verbraucher(w);
      e.start();
      v.start();
    }
  }

