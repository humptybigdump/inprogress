package kit.edu.aifb.proksy.lambdaFilmrolle;

import java.util.Arrays;
import java.util.List;

/**
 * @author ProkSy-Team
 * @version 1.0
 *
 */
public class LambdaAdvanced {

	public static void main(String[] args) {
		Filmrolle hodor = s -> System.out.print("Hodor!");
		Filmrolle plapper = System.out::print;
		Filmrolle yoda = s -> {
			String[] array = s.split("\\s");
			List<String> liste = Arrays.asList(array);
			liste.sort(String::compareToIgnoreCase);
			liste.forEach(e -> System.out.print(e + " "));
		};
		
		System.out.println("Hodor:");
		hodor.sagWas("Hallo, wie geht's?");
		System.out.println("");
		System.out.println("");
		System.out.println("Yoda:");
		yoda.sagWas("Der Himmel ist blau");
		System.out.println("");
		System.out.println("");
		System.out.println("Plapper:");
		plapper.sagWas("Was guckst du?");
	}
}
