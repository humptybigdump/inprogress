class Point {
  int x, y;
  private Point() { 
    reset(); 
  }
  Point(int x, int y) {
    this.x = x;  this.y = y; 
  }
  private void reset() { 
    this.x = 0;  this.y = 0; 
  }
}

