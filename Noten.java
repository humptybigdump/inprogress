package typen;
public enum Noten {
  C, CIS, D, DIS, E, F, FIS, G, GIS, A, AIS, H;
  
  public String tastenFarbe() {
    switch (this) {
      case CIS: 
      case DIS: 
      case FIS: 
      case GIS: 
      case AIS:
        return "schwarz";
      default:
        return "weiss";
    }
  }
}
