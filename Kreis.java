class Kreis extends Figur {
  int radius;
  Kreis (int r, int x, int y) {
    super("Kreis");     // Bezug auf Konstruktor der Oberklasse
    radius=r; ort.x=x; ort.y=y; // Variable ort geerbt 
  }
  void show () {
    System.out.println(name + " mit Radius " + radius);
  }
  boolean contains (int x, int y) {
    return (ort.x-x)*(ort.x-x)+
           (ort.y-y)*(ort.y-y) <=  radius*radius;
  }
}
