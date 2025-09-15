package edu.kit.aifb.proksy.goToCinema;

/**
 * Die Klasse Friend repräsentiert einen Freund, der ins Kino geht
 * 
 * @author ProkSy-Team
 * @version 1.0
 * 
 */
public class Friend implements Runnable {
	private String name; // Name der Person
	private BoxOffice boxOffice; // Referenz auf die Kinokasse
	private Speed speed; // Schnelligkeitsstufe der Person

	/**
	 * Konstruktor der Klasse Friend
	 * 
	 * @param name
	 *            Name der Person
	 * @param boxOffice
	 *            Referenz auf die Kinokasse
	 * @param speed
	 *            Schnelligkeitsstufe der Person
	 */
	public Friend(String name, BoxOffice boxOffice, Speed speed) {
		super();
		this.name = name;
		this.boxOffice = boxOffice;
		this.speed = speed;
	}

	/*
	 * (non-Javadoc)
	 * 
	 * @see java.lang.Runnable#run()
	 */
	@Override
	public void run() {
		eat();
		getReady();
		moveToCinema();
		buyTicket();

	}

	/**
	 * Person isst
	 */
	private void eat() {
		try {
			System.out.println(name + " beginnt zu essen");
			Thread.sleep(speed.getDuration());
			System.out.println(name + " hat fertig gegessen");
		} catch (InterruptedException e) {
			e.printStackTrace();
		}
	}

	/**
	 * Person macht sich fertig
	 */
	private void getReady() {
		try {
			System.out.println(name + " beginnt sich fertig zu machen");
			Thread.sleep(speed.getDuration());
			System.out.println(name + " ist bereit");
		} catch (InterruptedException e) {
			e.printStackTrace();
		}
	}

	/**
	 * Person geht ins Kino
	 */
	private void moveToCinema() {
		try {
			System.out.println(name + " geht los");
			Thread.sleep(speed.getDuration());
			System.out.println(name + " ist im Kino angekommen");
		} catch (InterruptedException e) {
			e.printStackTrace();
		}
	}

	/**
	 * Person kauft Eintrittskarte
	 */
	private void buyTicket() {
		System.out.println(name + " geht zur Kasse");
		boxOffice.sellTicket();
		System.out.println(name + " hat eine Eintrittskarte gekauft");

	}
}
