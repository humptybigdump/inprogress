package edu.kit.aifb.proksy.staffellauf;

/**
 * Diese Klasse enthält die main-Methode.
 * 
 * @author ProkSy-Team
 * @version 1.0
 */
public class Staffellauf {

	/**
	 * main-Methode der Klasse
	 * 
	 * @param args
	 */
	public static void main(String[] args) {
		Sprinter laeufer1 = new Sprinter("Sprinter 1", null);
		Sprinter laeufer2 = new Sprinter("Sprinter 2", laeufer1);
		Sprinter laeufer3 = new Sprinter("Sprinter 3", laeufer2);
		Sprinter laeufer4 = new Sprinter("Sprinter 4", laeufer3);
		Sprinter laeufer5 = new Sprinter("Sprinter 5", laeufer4);

		laeufer1.start();
		laeufer2.start();
		laeufer3.start();
		laeufer4.start();
		laeufer5.start();
	}

}
