package edu.kit.aifb.proksy.maiwanderung;

/**
 * Klasse modelliert ein Grillgut als Überbegriff von Bratwurst und Grillkäse.
 * 
 * @author ProkSy-Team
 * @version 1.0
 *
 */
public class Grillgut extends Proviant {
	private String bezeichnung;

	/**
	 * Methode liefert Bezeichnung des Grittlgutes zurück.
	 * 
	 * @return Bezeichnung des Grillgutes.
	 */
	public String getHerkunft() {
		return bezeichnung;
	}

	public String toString() {
		return "Grillgut der Art " + bezeichnung;
	}

	/**
	 * Konstruktor legt Bezeichnung eines Gutes fest.
	 * 
	 * @param bezeichnung Name des Gutes
	 */
	public Grillgut(String bezeichnung) {
		this.bezeichnung = bezeichnung;
	}

}
