package edu.kit.aifb.proksy.Sortierer;

/**
 * @version 1.0
 * @author ProkSy-Team
 *
 */
public class Punkt implements Comparable<Punkt> {
	private int x;
	private int y;
	
	public Punkt(int x, int y) {
		this.x = x;
		this.y = y;
	}
	
	public int getX() {
		return x;
	}
	
	public int getY() {
		return y;
	}
	
	public String toString() {
		return "X: "+x+", Y: "+y;
	}

	@Override
	public int compareTo(Punkt comparePunkt) {
		// Rückgabewert
        int compareValue =-2;
        // Vergleich auf Gleichheit
        if(this.x == comparePunkt.getX()) {
            compareValue = 0;
        }
        // Vergleich auf kleiner
        if(this.x < comparePunkt.getX()) {
            compareValue = -1;
        }
        // Vergleich auf größer
        if(this.x > comparePunkt.getX()) {
            compareValue = 1;
        }
        return compareValue;
	}	
}
