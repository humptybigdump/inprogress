package edu.kit.aifb.proksy.Sortierer;

import java.util.*;

/**
 * @version 1.0
 * @author ProkSy-Team
 *
 */
public class PunktComparator implements Comparator<Punkt> {
	@Override
	public int compare(Punkt comparePunkt1, Punkt comparePunkt2) {
		// Rückgabewert
        int compareValue =-2;
        // Vergleich auf Gleichheit
        if(comparePunkt1.getY() == comparePunkt2.getY()) {
            compareValue = 0;
        }
        // Vergleich auf kleiner
        if(comparePunkt1.getY() < comparePunkt2.getY()) {
            compareValue = -1;
        }
        // Vergleich auf größer
        if(comparePunkt1.getY() > comparePunkt2.getY()) {
            compareValue = 1;
        }
        return compareValue;
	}
}
