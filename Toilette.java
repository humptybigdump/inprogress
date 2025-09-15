package edu.kit.aifb.proksy.toilettenterror;

/**
 * Modelliert Toiletten-Objekt, auf welches mehrere Threads versuchen,
 * zeitgleich darauf zuzugreifen.
 * 
 * @author ProkSy-Team
 * @version 1.0
 */
public class Toilette {

	/**
	 * Modelliert Toilettennutzung
	 * 
	 * @param name Name des aufrufenden Objekts
	 */
	public void benutzen(String name) {
		System.out.println(name + "\t hat die Toilette besetzt");
		try {
			Thread.sleep((int) (Math.random() * 1000));
		} catch (InterruptedException ie) {
		}
		System.out.println(name + "\t hat seinen Darm erfolgreich geleert");
	}
}
