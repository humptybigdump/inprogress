package edu.kit.aifb.proksy.trainingstagebuch.controller;

import java.util.*;

import edu.kit.aifb.proksy.trainingstagebuch.model.Lauftraining;

/**
 * @version 1.0
 * @author ProkSy-Team
 *
 */
public class TrainingsverwaltungListe {

	private static LinkedList<Lauftraining> lauftrainingseinheiten;
	private static boolean running;

	/**
	 * @param args
	 */
	public static void main(String[] args) {
		Scanner scan = new Scanner(System.in);
		
		lauftrainingseinheiten = new LinkedList<Lauftraining>();
		lauftrainingseinheiten.add(new Lauftraining(new GregorianCalendar(2024, Calendar.APRIL, 10, 8, 57, 16).getTime(), 8.889, 3600));
		lauftrainingseinheiten.add(new Lauftraining(new GregorianCalendar(2024, Calendar.APRIL, 8, 8, 46, 56).getTime(), 8.889, 3400));
		lauftrainingseinheiten.add(new Lauftraining(new GregorianCalendar(2024, Calendar.APRIL, 8, 0, 43, 46).getTime(), 8.889, 3280));
		lauftrainingseinheiten.add(new Lauftraining(new GregorianCalendar(2024, Calendar.APRIL, 17, 5, 3, 36).getTime(), 8.889, 3300));
		running = true;
		while (running) {
			System.out.println("================== Absolvierte Trainingseinheiten (gesamt) ===================");
			System.out.println("==============================================================================");
			for (Lauftraining te : lauftrainingseinheiten) {
				System.out.println(lauftrainingseinheiten.indexOf(te) + ": " + te);
			}
			System.out.println();
			System.out.println("Welchen Eintrag moechten Sie loeschen? Bitte Nummer eingeben. (Zum Beenden -1 eingeben)");
			String eintragString = scan.next();
			try {
				int eintrag = Integer.parseInt(eintragString);
				if (eintrag == -1) {
					running = false;
				} else {
					lauftrainingseinheiten.remove(eintrag);
				}
			} catch (NumberFormatException e) {
				System.out.println("Bitte geben Sie eine gueltige Zahl ein (Buchstaben sind nicht erlaubt!)");
			} catch (IndexOutOfBoundsException e) {
				System.out.println("Bitte geben Sie eine Zahl ein, die im zulaessigen Bereich liegt");
			}
		}
	}
}
