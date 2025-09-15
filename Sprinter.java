package edu.kit.aifb.proksy.staffellauf;

import java.text.DecimalFormat;

/**
 * Diese Klasse repräsentiert einen Sprinter des Staffellaufs.
 * 
 * @author ProkSy-Team
 * @version 1.0
 */
public class Sprinter extends Thread {
	private String name;
	private Sprinter vorlaeufer;
	private double laufzeit;

	DecimalFormat format = new DecimalFormat("#.00");

	/**
	 * Konstruktor der Klasse
	 * 
	 * @param name
	 * @param vorlaeufer
	 */
	public Sprinter(String name, Sprinter vorlaeufer) {
		this.name = name;
		this.vorlaeufer = vorlaeufer;
		laufzeit = Math.random() * 4 + 9;
	}

	/**
	 * run-Methode: steuert das Verhalten des Sprinters
	 */
	public void run() {

		try {
			if (vorlaeufer != null) {
				vorlaeufer.join();
				System.out.println("Staffelstab an " + name + " uebergeben!");
			}
			System.out.println(name + " gestartet.");
			System.out.println(name + " laeuft die Strecke in " + format.format(laufzeit) + " s.");
			Thread.sleep((int) laufzeit);
		} catch (InterruptedException e) {
			System.out.println("Es ist eine Ausnahme aufgetreten.");
		}
		System.out.println(name + " erreicht sein Ziel.");
	}
}
