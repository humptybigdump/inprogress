package edu.kit.aifb.proksy.goToCinema;

/**
 * Die Klasse enthält die main-Methode der Aufgabe
 * 
 * @author ProkSy-Team
 * @version 1.0
 * 
 */
public class GoToCinema {

	private static BoxOffice boxOffice;

	/**
	 * main-Methode der Aufgabe
	 * 
	 * @param args
	 *            Kommandozeilenargumente
	 */
	public static void main(String[] args) {
		boxOffice = new BoxOffice(); // Erzeuge Kinokasse

		// Erzeuge fünf Freunde
		Friend georgina = new Friend("Georgina", boxOffice, Speed.FAST);
		Friend julian = new Friend("Julian", boxOffice, Speed.MEDIUM);
		Friend richard = new Friend("Richard", boxOffice, Speed.FAST);
		Friend anne = new Friend("Anne", boxOffice, Speed.MEDIUM);
		Friend timmy = new Friend("Timmy", boxOffice, Speed.SLOW);

		// Erzeuge Threads und Übergebe die fünf Freunde
		Thread georginaThread = new Thread(georgina);
		Thread julianThread = new Thread(julian);
		Thread richardThread = new Thread(richard);
		Thread anneThread = new Thread(anne);
		Thread timmyThread = new Thread(timmy);

		// Starte Threads
		georginaThread.start();
		julianThread.start();
		richardThread.start();
		anneThread.start();
		timmyThread.start();

		//Aufgabenteil b) Warten auf das Ende der Threads
		try {
			georginaThread.join();
			julianThread.join();
			richardThread.join();
			anneThread.join();
			timmyThread.join();
			System.out.println("Der Film kann beginnen!");
		} catch (InterruptedException e) {
			e.printStackTrace();
		}

	}
}
