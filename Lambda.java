package edu.kit.aifb.proksy.lambda;

import java.util.Arrays;
import java.util.List;

/**
 * @author ProkSy-Team
 * @version 1.0
 *
 */
public class Lambda {

	/**
	 * @param args Kommandozeilenargumente
	 */
	public static void main(String[] args) {
		// Erzeugt eine Liste mit Zahlen vom Typ Integer
		List<Integer> liste = Arrays.asList(11,21,24,36,41,55,62,66);
		
		// Gibt die Liste aus
		liste.forEach(e -> System.out.print(e + " "));
		
		// Sortiert die Liste nach dem Rest bei einer Division durch 8
		liste.sort((a,b) -> Integer.compare(a%8, b%8));
		
		// Zeilenumbruch
		System.out.println();
		
		// Gibt die Liste aus
		liste.forEach(e -> System.out.print(e + " "));
	}

}
