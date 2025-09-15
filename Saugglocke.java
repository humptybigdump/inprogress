package edu.kit.aifb.proksy.toilettenterror;

/**
 * Modelliert Saugglocken-Objekt, auf welches mehrere Threads versuchen,
 * zeitgleich darauf zuzugreifen.
 * 
 * @author ProkSy-Team
 * @version 1.0
 */
public class Saugglocke {

	/**
	 * Modelliert Saugglockennutzung
	 * 
	 * @param name
	 *            Name des aufrufenden Objekts
	 */
	public void abflussReinigen(String name) {
		System.out.println(name + "\t hat sich die Saugglocke gesichert");
		try {
			Thread.sleep((int) (Math.random() * 1000));
		} catch (InterruptedException ie) {
		}
		System.out.println(name + "\t hat den Abfluss erfolgreich gereinigt");
	}
}
