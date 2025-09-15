package edu.kit.aifb.proksy.iOSuperTools;

/**
 * 
 * Diese Klasse testet die IOSuperTools
 * 
 * @author ProkSy-Team
 * @version 1.0
 * 
 */
public class SuperIOMain {

	/**
	 * Main-Methode
	 * 
	 * @param args Kommandozeilenargumente
	 */
	public static void main(String[] args) {
		String string = IOSuperTools.stringEinlesen("Bitte Zeichenkette eingeben");
		int intWert = IOSuperTools.intEinlesen("Bitte Ganzzahl eingeben");
		double doubleWert = IOSuperTools.doubleEinlesen("Bitte Dezimalzahl eingeben");
		System.out.println("String: " + string);
		System.out.println("Integer: " + intWert);
		System.out.println("Double: " + doubleWert);
	}
}
