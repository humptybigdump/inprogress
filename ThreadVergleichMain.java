package edu.kit.aifb.proksy.threads;

/**
 * Klasse, die die Main-Methode enthält
 * 
 * @author ProkSy-Team
 * @version 1.0
 * 
 */
public class ThreadVergleichMain {
	
	public static boolean verfuegbar;

	/** 
	 * Main-Methode
	 * @param args Kommandozeilenargumente
	 * 
	 */
	public static void main(String[] args) {
		verfuegbar = false;
		Thread extendsThread = new ExtendsThread();
		Thread runnableThread = new Thread(new RunnableThread("RunnableThread"));
		extendsThread.start();
		runnableThread.start();		

	}

}
