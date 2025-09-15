package edu.kit.aifb.proksy.Erdkunde.server.controller;

import java.io.*;
import java.net.Socket;

import edu.kit.aifb.proksy.Erdkunde.server.model.*;

/**
 * Die Klasse kümmert sich um die Kommunikation mit dem Client.
 * 
 * @author ProkSy-Team
 * @version 1.0
 */
public class ServerProtokoll {

	private Topographie t;
	private boolean isRunning;
	private PrintWriter zumClient = null;
	private BufferedReader vomClient = null;
	private static boolean bundesland;

	/**
	 * Konstruktor der Klasse; öffnet die Ströme
	 * 
	 * @param s
	 */
	public ServerProtokoll(Socket s) {
		try {
			vomClient = new BufferedReader(new InputStreamReader(s.getInputStream()));
			zumClient = new PrintWriter(s.getOutputStream(), true);
		} catch (IOException e) {
			e.printStackTrace();
		}
	}

	/**
	 * Methode, mit der das ServerProtokoll eine Instanz des Datenmodells zugeordnet
	 * bekommt.
	 * 
	 * @param t
	 */
	public void setTopographie(Topographie t) {
		this.t = t;
	}

	/**
	 * Methode, die den Ablauf des Protokolls beinhaltet
	 */
	public void transact() {
		System.out.println("Erdkunde-Protokoll gestartet");
		isRunning = true;
		while (isRunning) {
			try {
				if (vomClient.readLine().equalsIgnoreCase("bundesland")) {
					bundesland = true;
				} else {
					bundesland = false;
				}
				String eingabe = vomClient.readLine();
				String ausgabe = topographie(eingabe, bundesland);
				zumClient.println(ausgabe);
			} catch (IOException e) {
				isRunning = false;
			}
		}
		System.out.println("Erdkunde-Protokoll beendet");
	}

	/**
	 * Die Methode kümmert sich um die Datenverarbeitung der Client-Eingabe
	 * 
	 * @param eingabe
	 * @param bundesland
	 * @return ausgabe
	 */
	public String topographie(String eingabe, boolean bundesland) {
		String ausgabe = null;
		if (bundesland == true) {
			ausgabe = t.getStadt(eingabe);
			return ausgabe;
		} else {
			ausgabe = t.getLand(eingabe);
			return ausgabe;
		}
	}

}
