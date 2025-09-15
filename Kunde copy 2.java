package edu.kit.aifb.proksy.mietenKaufenWohnen;

import java.rmi.*;
import java.rmi.registry.LocateRegistry;
import java.rmi.registry.Registry;
import java.io.*;

/**
 * Klasse, die den Client der Registry repräsentiert.
 * 
 * @author ProkSy-Team
 * @version 1.0
 */
public class Kunde {
	public static final int PORT = 1234;
	public static final String EXIT = "exit";

	/**
	 * main-Methode der Klasse
	 * 
	 * @param args
	 */
	public static void main(String[] args) {

		BufferedReader vonKonsole;
		Registry registry;
		Wohnungsmarkt w = null;
		String eingabe = null;
		String ausgabe = null;
		boolean isRunning = false;
		String[] liste = null;

		try {
			registry = LocateRegistry.getRegistry("localhost", PORT);
			liste = registry.list();
			System.out.println("Angebot:" + liste.length);
			for (int i = 0; i < liste.length; i++) {
				System.out.println(liste[i]);
			}
			isRunning = true;
			vonKonsole = new BufferedReader(new InputStreamReader(System.in));
			
			while (isRunning) {
				System.out.println("Bitte geben Sie die gewuenschte Wohnung ein. "
						+ "Sollten Sie das Programm beenden wollen, geben Sie 'exit' an. ");
				eingabe = vonKonsole.readLine();
				
				if (eingabe != null && !eingabe.equalsIgnoreCase(EXIT)) {
					try {
						w = (Wohnungsmarkt) registry.lookup("rmi://localhost:" + PORT + "/" + eingabe);
					} catch (NotBoundException nbe) {
						System.out.println("Die angefragte Wohnung existiert nicht! Bitte geben Sie eine Wohnung aus dem Angebot an.");
						continue;
					}
					ausgabe = w.getWohnung();
					System.out.println(ausgabe);
				} else {
					System.out.println("Das Programm wurde beendet. Wir hoffen Ihre Wohnungssuche war erfolgreich.");
					isRunning = false;
				}
			}
		} catch (RemoteException re) {
			System.out.println(re);
		} catch (IOException ioe) {
			System.out.println(ioe);
		}
	}
}
