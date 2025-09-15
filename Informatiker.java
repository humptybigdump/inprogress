package edu.kit.aifb.proksy.toilettenterror;

/**
 * Klasse ist Unterklasse von Thread.
 * 
 * @author ProkSy-Team
 * @version 1.0
 *
 */

public class Informatiker extends Thread {
	private Toilette toilette;
	private Saugglocke saugglocke;

	/**
	 * Konstruktor legt Eigenschaften der Klasse fest
	 * 
	 * @param name       Name des Maschinenbauers
	 * @param toilette   Referenz auf Toiletten-Objekt
	 * @param saugglocke Referenz auf Saugglocken-Objekt
	 */

	public Informatiker(String name, Toilette toilette, Saugglocke saugglocke) {
		super(name);
		this.toilette = toilette;
		this.saugglocke = saugglocke;
	}

	/**
	 * Methode arbeitet mit einem Lock auf das Toiletten-Objekt. Dies hindert andere
	 * Threads daran, zeitgleich auf das Objekt zuzugreifen. Die Reihenfolge der
	 * Befehle innerhalb des synchronized-Blocks sind frei festzulegen. Wichtig für
	 * einen korrekten Ablauf ist, dass alle Threads sich wechselseitig beim selben
	 * Objekt ausschließen. Eine Lösung, in welcher das Saugglocken-Objekt im
	 * synchronized-Block steht, ist analog möglich.
	 */
	public void erleichtern() {
		synchronized (toilette) {
			saugglocke.abflussReinigen(this.getName());
			toilette.benutzen(this.getName());
		}
	}

	/**
	 * Methode ruft dreimal die erleichtern-Methode auf und wartet anschließend eine
	 * zufällige Zeitspanne lang.
	 */
	@Override
	public void run() {
		for (int i = 0; i < 3; i++) {
			erleichtern();
			try {
				Thread.sleep((long) (Math.random() * 1000));
			} catch (InterruptedException e) {
				e.printStackTrace();
			}
		}
	}

}
