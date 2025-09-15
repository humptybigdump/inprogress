package edu.kit.aifb.proksy.iOSuperTools;

import java.io.*;

/**
 * Diese Klasse stellt eine Sammlung von Methoden zur Verfügung, die beim
 * Auslesen von Benutzereingaben hilft
 * 
 * @author ProkSy-Team
 * @version 1.0
 * 
 */
public class IOSuperTools {

	/**
	 * Diese Methode gibt eine Nachricht auf der Konsole aus und liest dann eine
	 * Benutzereingabe (Zeichenkette) aus
	 * 
	 * @param nachricht Meldung, die als Eingabeaufforderung ausgegeben wird.
	 * @return eingegebene Zeichenkette
	 */
	public static String stringEinlesen(String nachricht) {
		System.out.print(nachricht + " ? ");
		BufferedReader in = new BufferedReader(new InputStreamReader(System.in));
		String eingabe = "";
		try {
			eingabe = in.readLine();
		} catch (IOException e) {
			e.printStackTrace();
		} 
		return eingabe;
	}

	/**
	 * Diese Methode gibt eine Nachricht auf der Konsole aus und liest dann eine
	 * Benutzereingabe (Integer) aus
	 * 
	 * @param nachricht Meldung, die als Eingabeaufforderung ausgegeben wird.
	 * @return eingegebene Ganzzahl
	 */
	public static int intEinlesen(String nachricht) {
		return Integer.valueOf(stringEinlesen(nachricht)).intValue();
	}

	/**
	 * Diese Methode gibt eine Nachricht auf der Konsole aus und liest dann eine
	 * Benutzereingabe (Double) aus
	 * 
	 * @param nachricht Meldung, die als Eingabeaufforderung ausgegeben wird.
	 * @return eingegebene Dezimalzahl
	 */
	public static double doubleEinlesen(String nachricht) {
		return Double.valueOf(stringEinlesen(nachricht)).doubleValue();
	}

}
