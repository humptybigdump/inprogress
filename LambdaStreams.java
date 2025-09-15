package edu.kit.aifb.proksy.lambdastreams;

import java.util.Arrays;
import java.util.List;

/**
 * Klasse enthält alle Lösungsbestandteile der Aufgabe.
 * 
 * @author ProkSy-Team
 * @version 1.0
 *
 */
public class LambdaStreams {
	public static void main(String[] args) {
		List<String> list = Arrays.asList("Alfons", "Rocko", "Willhelm", "Henrietta", "Heidrun", "Leonie");

		// a)
		list.stream().filter(s -> s.startsWith("H")).sorted().forEach(System.out::println);

		// b)
		list.stream().filter(z -> z.length() > 5).sorted((a, b) -> a.length() - b.length())
				.forEach(a -> System.out.println(a)); // System.out::println wäre auch möglich

		// c)
		list.stream().map(s -> {
			String reverse = "";
			for (int i = s.length() - 1; i >= 0; i--)
				reverse += s.charAt(i);
			return reverse;
		}).limit(4).forEach(System.out::println);

		// d)
		long counter = list.stream().map(s -> s.length()).distinct().mapToInt(s -> Integer.valueOf(s)).sum();
		System.out.println(counter);
	}
}