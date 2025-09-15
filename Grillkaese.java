package edu.kit.aifb.proksy.maiwanderung;

/**
 * Diese Klasse modelliert einen Grillkäse und ist eine Unterklasse von
 * Grillgut. Jedes Objekt besitzt einen Namen, welcher die genaue Speise festlegt.
 * 
 * @author ProkSy-Team
 * @version 1.0
 *
 */
public class Grillkaese extends Grillgut {
	/**
	 * Konstruktor legt Bezeichnung des Grillkäses fest.
	 * 
	 * @param bezeichnung Name des Grillkäses.
	 */
	public Grillkaese(String bezeichnung) {
		super(bezeichnung);
	}

}