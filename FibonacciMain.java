package edu.kit.aifb.proksy.fibonacciThread;

/**
 * 
 * @author ProkSy-Team
 * @version 1.0
 * 
 *          Klasse mit main-Methode
 */

public class FibonacciMain {
	/**
	 * main-Methode des Programmes
	 * 
	 * @param args
	 */
	public static void main(String[] args) {
		Fibonacci fib = new Fibonacci();
		Thread schreiber = new FibonacciSchreiber("Schreiber", fib);
		Thread leser = new FibonacciLeser("Leser", fib);

		schreiber.start();
		leser.start();
	}
}
