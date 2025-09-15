package edu.kit.aifb.proksy.trainingstagebuch.controller;

import java.util.*;

import edu.kit.aifb.proksy.trainingstagebuch.model.Krafttraining;
import edu.kit.aifb.proksy.trainingstagebuch.model.Lauftraining;
import edu.kit.aifb.proksy.trainingstagebuch.model.Trainingseinheit;

/**
 * Klasse Trainingsverwaltung
 * 
 * @version 1.0
 * @author ProkSy-Team
 *
 */
public class TrainingsverwaltungSet {

	private static TreeSet<Lauftraining> lauftrainingseinheiten;
	private static TreeSet<Krafttraining> krafttrainingseinheiten;
	private static TreeSet<Trainingseinheit> trainingseinheiten;

	/**
	 * Main-Methode der Klasse Trainingsverwaltung
	 * 
	 * @param args
	 *            Kommandozeilenparameter
	 */
	public static void main(String[] args) {
		lauftrainingseinheiten = new TreeSet<Lauftraining>();
		krafttrainingseinheiten = new TreeSet<Krafttraining>();
		trainingseinheiten = new TreeSet<Trainingseinheit>();
		lauftrainingseinheiten.add(new Lauftraining(new GregorianCalendar(2024, Calendar.APRIL, 10, 8, 57, 16).getTime(), 8.889, 3600));
		lauftrainingseinheiten.add(new Lauftraining(new GregorianCalendar(2024, Calendar.APRIL, 8, 8, 46, 56).getTime(), 8.889, 3400));
		lauftrainingseinheiten.add(new Lauftraining(new GregorianCalendar(2024, Calendar.APRIL, 8, 0, 43, 36).getTime(), 8.889, 3280));
		lauftrainingseinheiten.add(new Lauftraining(new GregorianCalendar(2024, Calendar.APRIL, 17, 5, 3, 36).getTime(), 8.889, 3300));
		lauftrainingseinheiten.add(new Lauftraining(new GregorianCalendar(2024, Calendar.APRIL, 17, 22, 3, 36).getTime(), 8.889, 3250));

		krafttrainingseinheiten.add(new Krafttraining(new GregorianCalendar(2024, Calendar.APRIL, 20, 23, 3, 36).getTime(), 3));
		krafttrainingseinheiten.add(new Krafttraining(new GregorianCalendar(2024, Calendar.APRIL, 15, 4, 3, 36).getTime(), 5));
		krafttrainingseinheiten.add(new Krafttraining(new GregorianCalendar(2024, Calendar.APRIL, 10, 8, 3, 36).getTime(), 6));

		System.out.println("=================== Absolvierte Lauf-Trainingseinheiten ======================");
		System.out.println("==============================================================================");
		for (Lauftraining te : lauftrainingseinheiten) {
			System.out.println(te);
		}
		System.out.println();
		System.out.println();

		System.out.println("=================== Absolvierte Kraft-Trainingseinheiten =====================");
		System.out.println("==============================================================================");
		for (Krafttraining te : krafttrainingseinheiten) {
			System.out.println(te);
		}

		trainingseinheiten.addAll(lauftrainingseinheiten);
		trainingseinheiten.addAll(krafttrainingseinheiten);
		System.out.println();
		System.out.println();
		System.out.println("================== Absolvierte Trainingseinheiten (gesamt) ===================");
		System.out.println("==============================================================================");
		for (Trainingseinheit te : trainingseinheiten) {
			System.out.println(te);
		}

	}

}
