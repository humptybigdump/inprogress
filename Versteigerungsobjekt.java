package edu.kit.aifb.proksy.auktion;

/**
 * Diese Klasse repräsentiert das zu versteigernde Objekt
 * 
 * @author ProkSy-Team
 * @version 1.0
 * 
 */
public class Versteigerungsobjekt {

	private Bieter hoechstbietender;
	private int hoechstgebot;
	private boolean verkauft;

	/**
	 * Konstruktor der Klasse
	 */
	public Versteigerungsobjekt() {
		this.hoechstbietender = null;
		this.hoechstgebot = 0;
		this.verkauft = false;
	}

	/**
	 * Trägt ein gebot als aktuelles Höchstgebot ein
	 * 
	 * @param bieter
	 *            Bieter, der das Gebot abgegeben hat
	 * @param gebot
	 *            Höhe des Gebotes
	 */
	public void gebotEintragen(Bieter bieter, int gebot) {
		if (!verkauft) {
			this.hoechstbietender = bieter;
			this.hoechstgebot = gebot;
		}
	}

	/**
	 * Wird aufgerufen, wenn das Objekt verkauft wurde
	 */
	public void verkaufen() {
		verkauft = true;
		System.out.println(hoechstbietender + ": MEINS!");
		System.out.println("Objekt wurde fuer " + this.hoechstgebot + " an "
				+ this.hoechstbietender + " verkauft");
	}

	/**
	 * Getter-Methode für den Höchstbietenden
	 * 
	 * @return Höchstbietender
	 */
	public Bieter getHoechstbietender() {
		return hoechstbietender;
	}

	/**
	 * Getter-Methode für das höchste Gebot
	 * 
	 * @return höchstes Gebot
	 */
	public int getHoechstgebot() {
		return hoechstgebot;
	}

	/**
	 * Getter-Methode für das verkauft-Flag
	 * 
	 * @return verkauft-Flag
	 */
	public boolean isVerkauft() {
		return verkauft;
	}
}
