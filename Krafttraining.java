package edu.kit.aifb.proksy.trainingstagebuch.model;

import java.util.Date;

/**
 * Diese Klasse repräsentiert ein Krafttraining
 * 
 * @version 1.0
 * @author ProkSy-Team
 *
 */
public class Krafttraining extends Trainingseinheit {

	private int numberOfExercises; // Anzahl der absolvierten Übungen

	/**
	 * Konstruktor der Klasse Lauftraining
	 * 
	 * @param date
	 *            Zeitpunkt, an dem das Training begonnen hat
	 * @param numberOfExercises
	 *            Anzahl der absolvierten Übungen
	 * 
	 */
	public Krafttraining(Date date, int numberOfExercises) {
		super(date);
		this.numberOfExercises = numberOfExercises;
	}

	/**
	 * Gibt die Anzahl der absolvierten Übungen zurück
	 * 
	 * @return Anzahl der absolvierten Übungen zurück
	 */
	public int getNumberOfExercises() {
		return numberOfExercises;
	}

	/**
	 * Setzt die Anzahl der absolvierten Übungen
	 * 
	 * @param numberOfExercises
	 *            Anzahl der absolvierten Übungen
	 */
	public void setNumberOfExercises(int numberOfExercises) {
		this.numberOfExercises = numberOfExercises;
	}

	/*
	 * (non-Javadoc)
	 * 
	 * @see edu.kit.aifb.proksy.Trainingstagebuch.Trainingseinheit#toString()
	 */
	public String toString() {
		return super.toString() + " - Kraft: "
				+ this.getNumberOfExercises() + " Uebungen";
	}

}