package edu.kit.aifb.proksy.maiwanderung;

/**
 * Klasse modelliert jeweils einen Rucksack, der Platz für eine Einheit einer
 * Unterklasse von Proviant besitzt. Für die Aufgabe muss nur diese Klasse inkl.
 * Methoden angepasst werden.
 * 
 * Klasse enthält zugleich die main-Methode.
 * 
 * @author ProkSy-Team
 * @version 1.0
 * @param <T> Parameter beschreibt Inhalt des Rucksacks
 *
 */
public class Rucksack<T extends Proviant> {

	T inhalt = null;

	/**
	 * Prüft, ob im Rucksack noch Inhalt vorhanden ist.
	 * 
	 * @return true, falls kein Inhalt vorhanden ist, false sonst
	 */
	public boolean isEmpty() {
		return (inhalt == null);
	}

	/**
	 * Liefern den Inhalt des Rucksacks, ohne diesen zu leeren.
	 * 
	 * @return Inhalt des Rucksacks.
	 */
	public T getInhalt() {
		return inhalt;
	}

	/**
	 * Füllt den Rucksack mit dem Inhalt im Parameter, unabhängig davon, ob bereits
	 * etwas im Rucksack liegt.
	 * 
	 * @param inhalt
	 *            Inhalt für den Rucksack
	 */
	public void packen(T inhalt) {
		this.inhalt = inhalt;
	}

	/**
	 * Liefert den aktuellen Inhalt des Rucksackes und leert diesen.
	 * 
	 * @return Inhalt des Rucksackes
	 */
	public T verzehren() {
		T result = inhalt;
		inhalt = null;
		return result;
	}

	/**
	 * Methode liefert den Namen des Inhaltes eines Rucksacks zurück. Die Methode
	 * soll dabei nur mit Rucksäcken aufrufbar sein, welche Grillgut beinhalten.
	 * 
	 * @param rucksack
	 *            Rucksack, dessen Inhalt geprüft werden soll
	 * @return Klassenname des Inhaltes.
	 */
	public static <I extends Grillgut> String wasIstDrin(Rucksack<I> rucksack) {
		return rucksack.getInhalt().getClass().getName();
	}

	/**
	 * Hauptteil des Programms
	 * 
	 * @param unwichtigeArgumente
	 */
	public static void main(String[] unwichtigeArgumente) {
		// Angabe des Parameters bei der Erzeugung (rechte Seite) optional
		Rucksack<Bier> rucksack1 = new Rucksack<Bier>();
		rucksack1.packen(new Bier("Wiwi-Braeu"));
		System.out.println("Inhalt von Rucksack 1 vernichtet: " + rucksack1.verzehren());
		if (rucksack1.isEmpty())
			System.out.println("Rucksack 1 ist leer und kann neu befuellt werden");
		rucksack1.packen(new Bier("Maurersekt"));
		System.out.println("Inhalt von Rucksack 1: " + rucksack1.getInhalt() + "\n");
		
		// Aufruf von Rucksack.wasIstDrin(rucksack1); ist nicht möglich

		// Hier wurde auf die Angabe des Inhalts verzichtet
		Rucksack<Grillgut> rucksack2 = new Rucksack<>();
		rucksack2.packen(new Grillkaese("Schafskaese"));
		// Aufruf der generischen Klassenmethode
		System.out.println("Inhalt von Rucksack 2: " + Rucksack.wasIstDrin(rucksack2));
		rucksack2.packen(new Bratwurst("Schlesische Landbratwurst"));
		System.out.println("Inhalt von Rucksack 2 vernichtet: " + rucksack2.verzehren() + "\n");

		Rucksack<Bratwurst> rucksack3 = new Rucksack<>();
		rucksack3.packen(new Bratwurst("Waadtlaender Bratwurst"));
		System.out.println("Inhalt von Rucksack 3: " + Rucksack.wasIstDrin(rucksack3));
	}
}