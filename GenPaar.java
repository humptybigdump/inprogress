public class GenPaar<T> {

  private T l, r;

  public GenPaar (T l, T r) {
    this.l = l;
    this.r = r;
  }
  public T getL() {
    return l;
  }
  public T getR() {
    return r;
  }
  public String toString() {
    return "(l,r) = (" + l + "," + r +")";
  }
}
