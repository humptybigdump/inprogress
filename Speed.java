package edu.kit.aifb.proksy.goToCinema;

/**
 * Aufzählung, die die verschiedenen Schnelligkeitsstufen enthält
 * 
 * @author ProkSy-Team
 * @version 1.0
 * 
 */
public enum Speed {
	SLOW, MEDIUM, FAST;
	public int getDuration() {

		switch (this) {
		case SLOW:
			return 1500;
		case MEDIUM:
			return 1000;
		case FAST:
			return 500;
		default:
			return -1;
		}
	}
}