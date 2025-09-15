abstract class Figur {
  String name;
  Punkt ort = new Punkt();
  Figur (String name) {  // Konstruktor
    this.name = name;
  }
  abstract void show ();   
    // zeigt die Daten der Figur
    // kein Methodenrumpf!
  abstract boolean contains (int x, int y);
    // prüft ob der Punkt (x,y) innerhalb der Figur liegt
    // kein Methodenrumpf!
}
