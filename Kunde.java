package edu.kit.aifb.proksy.baeckerei;

/**
 * @author ProkSy-Team
 * @version 1.0
 * 
 *         Die Klasse ist eine Unterklasse von Thread und simuliert einen
 *         Kunden. Dieser wird einer Bäckerei zugeordnet und kauft bei dieser
 *         Brote, entspricht also einem Verbraucher.
 *
 */
public class Kunde {
	private Baeckerei b;

	/**
	 * Konstruktor legt Bezeichnung des Kunden fest und weist eine Bäckerei zu.
	 * 
	 * @param name Bezeichnung des Threads
	 * @param b    Zugewiesene Bäckerei
	 */
	public Kunde(String name, Baeckerei b) {
		// TODO
	}

	/**
	 * Der Kunde kauft 10 Brote pro Durchlauf. Nach jedem gekauften Brot wird eine
	 * Pause von zufälliger Länge eingelegt, bis der nächste Kauf erfolgt
	 */
	@Override
	public void run() {
		for (int i = 0; i < 10; i++) {
			// TODO
		}
	}
}
