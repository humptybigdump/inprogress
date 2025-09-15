  class Werts {
    private int wert;
    private boolean verfuegbar = false;
    public synchronized int get() {
      if (!verfuegbar)
        try {
          wait();
        }
        catch (InterruptedException ie) {
        }
      verfuegbar = false;
      notify();
      return wert;
    }
    public synchronized void put (int w) {
      if (verfuegbar)
        try {
          wait();
        }
        catch (InterruptedException ie) {
        }
      wert = w;
      verfuegbar = true;
      notify();
    }
  }

  class Erzeugers extends Thread {
    Werts w;
    public Erzeugers (Werts w) {
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

  class Verbrauchers extends Thread {
    Werts w;
    public Verbrauchers (Werts w) {
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

  public class EVTestNeu {
    public static void main (String args[]) {
      Werts        w = new Werts();
      Erzeugers    e = new Erzeugers(w);
      Verbrauchers v = new Verbrauchers(w);
      e.start();
      v.start();
    }
  }

