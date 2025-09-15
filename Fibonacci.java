package edu.kit.aifb.proksy.fibonacciThread;

/**
 * @version 1.0
 * @author ProkSy-Team
 *
 */
public class Fibonacci {
	private int a = 1;
	private int b = 1;
	private boolean verfuegbar = true;

	synchronized public void fibonacciA() {
		if (verfuegbar) {
			try {
				wait();
			} catch (InterruptedException e) {
			}
		}
		a = a + b;
		verfuegbar = true;
		notify();
	}

	synchronized public void fibonacciB() {
		if (verfuegbar) {
			try {
				wait();
			} catch (InterruptedException e) {
			}
		}
		b = a + b;
		verfuegbar = true;
		notify();
	}

	synchronized public int getA() {
		if (!verfuegbar) {
			try {
				wait();
			} catch (InterruptedException e) {
			}
		}
		verfuegbar = false;
		notify();
		return a;
	}

	synchronized public int getB() {
		if (!verfuegbar) {
			try {
				wait();
			} catch (InterruptedException e) {
			}
		}
		verfuegbar = false;
		notify();
		return b;
	}
}
