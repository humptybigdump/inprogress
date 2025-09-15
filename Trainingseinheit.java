package edu.kit.aifb.proksy.trainingstagebuch.model;

import java.util.*;
import java.text.*;

/**
 * @version 1.0
 * @author ProkSy-Team
 *
 */
public class Trainingseinheit implements Comparable<Trainingseinheit> {
	private Date date;

	/**
	 * Konstruktor der Klasse Trainingseinheit
	 * 
	 * @param date
	 *            Zeitpunkt, an dem die Trainingseinheit begonnen wurde
	 */
	public Trainingseinheit(Date date) {
		this.date = date;
	}

	/**
	 * Gibt den Zeitpunkt, an dem die Trainingseinheit begonnen wurde, zurück
	 * 
	 * @return Zeitpunkt der Trainingseinheit
	 */
	public Date getDate() {
		return date;
	}

	/**
	 * Setzt den Zeitpunkt, an dem die Trainingseinheit begonnen wurde
	 * 
	 * @param date
	 *            Zeitpunkt , an dem die Trainingseinheit begonnen wurde
	 */
	public void setDate(Date date) {
		this.date = date;
	}

	/*
	 * (non-Javadoc)
	 * 
	 * @see java.lang.Comparable#compareTo(java.lang.Object)
	 */
	@Override
	public int compareTo(Trainingseinheit te) {
		return this.getDate().compareTo(te.getDate());
	}

	/**
	 * Prüft auf Gleichheit
	 * 
	 * @param te
	 *            zu vergleichende Trainingseinheit
	 * @return gibt zurück, ob beide Objekte gleich sind
	 */
	public boolean equals(Object obj) {
		if (obj == null)
			return false;
		if (obj == this)
			return true;
		if (!obj.getClass().equals(this.getClass()))
			return false;
		Trainingseinheit te = (Trainingseinheit) obj;
		return this.getDate().equals(te.getDate());
	}

	/*
	 * (non-Javadoc)
	 * 
	 * @see java.lang.Object#toString()
	 */
	public String toString() {
		SimpleDateFormat sdf = new SimpleDateFormat(
				"'Einheit am 'EEEE', den 'd'. 'MMMM' 'yyyy' um 'HH':'mm' Uhr'");
		return sdf.format(this.getDate());
	}

}
