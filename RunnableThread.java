package edu.kit.aifb.proksy.threads;

/**
 *
 * @author ProkSy-Team
 * @version 1.0
 * 
 */
public class RunnableThread implements Runnable {

	private int wiederholungen;
	private String name;
	
	/**
	 * Konstruktor der Klasse
	 */
	public RunnableThread(String name) {
		wiederholungen = (int) (Math.random() * 10) + 1;
		this.name = name;
	}
	
	@Override
	public void run() {
		for (int i = 1; i <= wiederholungen; i++) {
			System.out.println(name+ " - Wiederholung "+i);
			try {
				Thread.sleep(1000);
			} catch (InterruptedException e) {
				// Tue nichts
			}
		}

	}

}
