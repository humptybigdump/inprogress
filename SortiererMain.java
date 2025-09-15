package edu.kit.aifb.proksy.Sortierer;

import java.util.*;

/**
 * @version 1.0
 * @author ProkSy-Team
 *
 */
public class SortiererMain {

	public static void main(String[] args) {
		TreeSet<Punkt> tree1 = new TreeSet<Punkt>();
		TreeSet<Punkt> tree2 = new TreeSet<Punkt>(new PunktComparator());
		
		tree1.add(new Punkt(1,2));
		tree1.add(new Punkt(12,4));
		tree1.add(new Punkt(3,6));
		tree1.add(new Punkt(7,5));
		tree1.add(new Punkt(9,10));
		
		tree2.addAll(tree1);
		
		Iterator<Punkt> it = tree1.iterator();
		int i = 1;
		System.out.println("Sortierung nach X-Wert mit Comparable:");
		while(it.hasNext()) {
			Punkt p = (Punkt) it.next();
			System.out.println("Punkt " + i + ": "+p);
			i++;
		}
		
		it = tree2.iterator();
		i = 1;
		System.out.println("Sortierung nach Y-Wert mit Comparator:");
		while(it.hasNext()) {
			Punkt p = (Punkt) it.next();
			System.out.println("Punkt " + i + ": "+p);
			i++;
		}
		
	}

}
