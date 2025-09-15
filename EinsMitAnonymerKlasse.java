class EinsMitAnonymerKlasse {
  int x;
  void meth1 () {
  }
  
  Zwei v = new Zwei() {
    int q = 555;
    public void meth3 () {
      x = q++;
    }
  };

}

