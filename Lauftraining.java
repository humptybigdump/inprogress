package edu.kit.aifb.proksy.trainingstagebuch.model;

import java.util.Date;
import java.text.*;

/**
 * Diese Klasse repräsentiert ein Lauftraining
 * 
 * @version 1.0
 * @author ProkSy-Team
 *
 */
public class Lauftraining extends Trainingseinheit {

	private double distance; // Strecke in Kilometern
	private int time; // Dauer in Sekunden

	/**
	 * Konstruktor der Klasse Lauftraining
	 * 
	 * @param date
	 *            Zeitpunkt, an dem das Training begonnen hat
	 * @param distance
	 *            zurückgelegte Distanz
	 * @param time
	 *            benötigte Zeit für die Strecke
	 */
	public Lauftraining(Date date, double distance, int time) {
		super(date);
		this.distance = distance;
		this.time = time;
	}

	/**
	 * Gibt die Geschwindigkeit des Läufers in km/h zurück
	 * 
	 * @return Geschwindigkeit in km/h
	 */
	public double getSpeed() {
		return distance / time * 3600;
	}

	/**
	 * Gibt die zurückgelegte Distanz zurück
	 * 
	 * @return zurückgelegte Distanz in Kilometern
	 */
	public double getDistance() {
		return distance;
	}

	/**
	 * Setzt die zurückgelegte Distanz
	 * 
	 * @param distance
	 *            zurückgelegte Distanz in Kilometern
	 */
	public void setDistance(double distance) {
		this.distance = distance;
	}

	/**
	 * Gibt die benötigte Zeit zurück
	 * 
	 * @return benötigte Zeit in Sekunden
	 */
	public int getTime() {
		return time;
	}

	/**
	 * Setzt die benötigte Zeit
	 * 
	 * @param time
	 *            benötigte Zeit in Sekunden
	 */
	public void setTime(int time) {
		this.time = time;
	}

	/*
	 * (non-Javadoc)
	 * 
	 * @see edu.kit.aifb.proksy.Trainingstagebuch.Trainingseinheit#toString()
	 */
	public String toString() {
		DecimalFormat dfSpeed = new DecimalFormat("#.00 km/h");
		DecimalFormat dfDistance = new DecimalFormat("#.000 km");
		return super.toString() + " - Lauf: "
				+ dfDistance.format(this.getDistance()) + " ("
				+ dfSpeed.format(this.getSpeed()) + ")";
	}

}