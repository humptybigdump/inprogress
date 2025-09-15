package edu.kit.aifb.proksy.fibonacciThread;

/**
 * @version 1.0
 * @author ProkSy-Team
 *
 */
public class FibonacciSchreiber extends Thread {
	private String name;
	private Fibonacci fib;

	public FibonacciSchreiber(String name, Fibonacci fib) {
		super(name);
		this.name = name;
		this.fib = fib;
	}

	@Override
	public void run() {
		System.out.println("Thread " + name + " ist gestartet.");
		for (int k = 1; k <= 10; k++) {
			if (k % 2 == 1) {
				fib.fibonacciA();
			} else {
				fib.fibonacciB();
			}
		}
	}
}
