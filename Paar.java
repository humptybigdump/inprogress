public class Paar {

  private Object l, r;

  public Paar (Object l, Object r) {
    this.l = l;
    this.r = r;
  }
  public Object getL() {
    return l;
  }
  public Object getR() {
    return r;
  }
  public String toString() {
    return "(l,r) = (" + l + "," + r +")";
  }
}
