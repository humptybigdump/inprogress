class RechtEckchen extends Figur {
  int b, h;
  RechtEckchen (int x, int y, int b, int h) {
    super ("RechtEckchen");
    ort.x=x; ort.y=y; this.b=b; this.h=h;
  }
  void show () {
    System.out.println(name + " mit Breite " + b + 
                              " und Hoehe " + h);
  }
  boolean contains (int x, int y) {
    return ort.x <= x && x <= ort.x+b &&
           ort.y <= y && y <= ort.y+h;
  }
}

