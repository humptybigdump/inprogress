package edu.kit.aifb.proksy.ErdkundeRMI.server.model;

import java.util.HashMap;

/**
 * Klasse, die das Datenmodell repräsentiert.
 * 
 * @author ProkSy-Team
 * @version 1.0
 */
public class Topographie {
	HashMap<String, String> bundesland = new HashMap<String, String>();
	HashMap<String, String> hauptstadt = new HashMap<String, String>();

	/**
	 * Konstruktor, der die Datensätze erstellt
	 */
	public Topographie() {
		bundesland.put("Baden-Württemberg", "Stuttgart");
		bundesland.put("Bayern", "München");
		bundesland.put("Berlin", "Berlin");
		bundesland.put("Brandenburg", "Potsdam");
		bundesland.put("Bremen", "Bremen");
		bundesland.put("Hamburg", "Hamburg");
		bundesland.put("Hessen", "Wiesbaden");
		bundesland.put("Mecklenburg-Vorpommern", "Schwerin");
		bundesland.put("Niedersachsen", "Hannover");
		bundesland.put("Nordrhein-Westfalen", "Düsseldorf");
		bundesland.put("Rheinland-Pfalz", "Mainz");
		bundesland.put("Saarland", "Saarbrücken");
		bundesland.put("Sachsen", "Dresden");
		bundesland.put("Sachsen-Anhalt", "Magdeburg");
		bundesland.put("Schleswig-Holstein", "Kiel");
		bundesland.put("Thüringen", "Erfurt");

		hauptstadt.put("Berlin", "Berlin");
		hauptstadt.put("Bremen", "Bremen");
		hauptstadt.put("Dresden", "Sachsen");
		hauptstadt.put("Düsseldorf", "Nordrhein-Westfalen");
		hauptstadt.put("Erfurt", "Thüringen");
		hauptstadt.put("Hamburg", "Hamburg");
		hauptstadt.put("Hannover", "Niedersachsen");
		hauptstadt.put("Kiel", "Schleswig-Holstein");
		hauptstadt.put("Magdeburg", "Sachsen-Anhalt");
		hauptstadt.put("Mainz", "Rheinland-Pfalz");
		hauptstadt.put("München", "Bayern");
		hauptstadt.put("Potsdam", "Brandenburg");
		hauptstadt.put("Saarbrücken", "Saarland");
		hauptstadt.put("Schwerin", "Mecklenburg-Vorpommern");
		hauptstadt.put("Stuttgart", "Baden-Württemberg");
		hauptstadt.put("Wiesbaden", "Hessen");
	}

	/**
	 * Die Methode gibt das angefragte Bundesland oder bei einer falschen Eingabe
	 * eine Fehlermeldung zurück.
	 * 
	 * @param key
	 * @return angefragtes Bundesland
	 */
	public String getLand(String key) {
		if (!hauptstadt.containsKey(key)) {
			return "Gibts nicht!";
		}
		return hauptstadt.get(key);
	}

	/**
	 * Die Methode gibt die angefragte Hauptstadt oder bei einer falschen Eingabe
	 * eine Fehlermeldung zurück.
	 * 
	 * @param key
	 * @return angefragte Hauptstadt
	 */
	public String getStadt(String key) {
		if (!bundesland.containsKey(key)) {
			return "Gibts nicht!";
		}
		return bundesland.get(key);
	}
}
