package edu.kit.aifb.proksy.umrechner.model;

/**
 * Diese Klasse repräsentiert eine Längeneinheit
 * 
 * @version 1.0
 * @author ProkSy-Team
 *
 */
public class UnitOfLength implements Comparable<UnitOfLength> {
	private String name;
	private double inMm;

	/**
	 * Konstruktor, dem ein Name und der Umrechnungsfaktor zu Millimetern übergeben
	 * wird
	 * 
	 * @param name Name der Längeneinheit
	 * @param inMm Umrechnungsfaktor zu Millimeter
	 */
	public UnitOfLength(String name, double inMm) {
		this.name = name;
		this.inMm = inMm;
	}

	/**
	 * Liefert den Namen der Längeneinheit zurück
	 * 
	 * @return Name der Längeneinheit
	 */
	public String getName() {
		return name;
	}

	/**
	 * Legt den Namen der Längeneinheit fest
	 * 
	 * @param name einzustellender Name
	 */
	public void setName(String name) {
		this.name = name;
	}

	/**
	 * Liefert den Umrechnungsfaktor zurück
	 * 
	 * @return Umrechnungsfaktor
	 */
	public double getInMm() {
		return inMm;
	}

	/**
	 * Setzt den Umrechnungsfaktor
	 * 
	 * @param inMm Umrechnungsfaktor
	 */
	public void setInMm(double inMm) {
		this.inMm = inMm;
	}

	@Override
	public int compareTo(UnitOfLength unit) {
		return this.toString().compareTo(unit.toString()); // Sortiert alphabetisch
	}

	/*
	 * (non-Javadoc)
	 * 
	 * @see java.lang.Object#toString()
	 */
	public String toString() {
		return name;
	}

}
