package edu.kit.aifb.proksy.auktion;

/**
 * Diese Klasse enthält die main-Methode der Auktionssimulation
 * 
 * @author ProkSy-Team
 * @version 1.0
 * 
 */
public class Versteigerung {

	static private Versteigerungsobjekt vase;
	static private Bieter bieter1;
	static private Bieter bieter2;
	static private Auktionator auktionator;

	/**
	 * main-Methode des Programms zur Auktionssimulation
	 * 
	 * @param args
	 *            Kommandozeilenparameter
	 */
	public static void main(String[] args) {
		vase = new Versteigerungsobjekt();
		auktionator = new Auktionator(vase);
		bieter1 = new Bieter(auktionator, "Peter", 3);
		bieter2 = new Bieter(auktionator, "Franziska", 5);
		auktionator.start();
		bieter1.start();
		bieter2.start();

	}

}
