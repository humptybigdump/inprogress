public class Rechteck {
  public int breite = 0;
  public int hoehe = 0;
  public Punkt ursprung;

  // vier Konstruktoren
  public Rechteck() {
    ursprung = new Punkt(0, 0); 
  }
  public Rechteck(Punkt p) {
    ursprung = p;
  }
  public Rechteck(int w, int h) {
    this(new Punkt(0, 0), w, h);
  }
  public Rechteck(Punkt p, int w, int h) {
    ursprung = p;
    breite = w; 
    hoehe = h; 
  }
  
  // Methoden ...
  // ... zum Bewegen des Rechtecks
  public void move(int x, int y) {
    ursprung.x = x;
    ursprung.y = y;
  } 

  // ... zur Flächenberechnung
  public int flaeche() {
    return breite * hoehe;
  }

  // ... zum Aufräumen!
  protected void finalize() throws Throwable {
    ursprung = null;
    super.finalize();
  }

} // Ende der Klasse Rechteck 

