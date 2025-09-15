package edu.kit.aifb.proksy.mietenKaufenWohnen;

import java.rmi.*;
import java.rmi.registry.*;

/**
 * Klasse, die die Serverseite der RMI-Programmierung repräsentiert.
 * 
 * @author ProkSy-Team
 * @version 1.0
 */
public class Immobilienmakler {
	public static final int PORT = 1234;

	/**
	 * main-methode der Klasse
	 * 
	 * @param args
	 */
	public static void main(String[] args) {
		Wohnung w1 = null;
		Wohnung w2 = null;
		Wohnung w3 = null;
		Wohnung w4 = null;
		Wohnung w5 = null;

		try {
			w1 = new Wohnung("Huebsche 3-Zimmer Wohnung", 3, 632.3);
			w2 = new Wohnung("Abgeranzte Bude", 3, 100.1);
			w3 = new Wohnung("Lichtdurchfluteter Palast", 6, 1100.73);
			w4 = new Wohnung("Klein aber fein", 1, 400.67);
			w5 = new Wohnung("Ohne Moos nix los", 2.5, 1000.5);

			Registry registry = LocateRegistry.createRegistry(1234);

			registry.rebind("rmi://localhost:" + PORT + "/Wohnung_1", w1);
			registry.rebind("rmi://localhost:" + PORT + "/Wohnung_2", w2);
			registry.rebind("rmi://localhost:" + PORT + "/Wohnung_3", w3);
			registry.rebind("rmi://localhost:" + PORT + "/Wohnung_4", w4);
			registry.rebind("rmi://localhost:" + PORT + "/Wohnung_5", w5);
		}
		/*
		 * catch(MalformedURLException me) { System.out.println(me); }
		 */
		catch (RemoteException re) {
			System.out.println(re);
		}

		System.out.println("Der Server ist aktiv");

	}
}
