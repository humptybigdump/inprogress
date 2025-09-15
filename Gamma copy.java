package greek;
class Gamma {
  void accessMethod() {
    Alpha a = new Alpha();
    a.iAmProtected = 10;   // zulässig
    a.protectedMethod();   // zulässig
  }
}

