package edu.kit.aifb.proksy.threads;

/**
 * 
 * @author ProkSy-Team
 * @version 1.0
 *
 */
public class ExtendsThread extends Thread {

	private int wiederholungen;
	
	/**
	 * Konstruktor der Klasse
	 */
	public ExtendsThread() {
		super("ExtendsThread");
		wiederholungen = (int) (Math.random() * 10) + 1;
	}
	
	@Override
	public void run() {
		for (int i = 1; i <= wiederholungen; i++) {
			System.out.println(this.getName()+ " - Wiederholung "+i);
			try {
				sleep(1000);
			} catch (InterruptedException e) {
				// Tue nichts
			}
		}
	}

}
