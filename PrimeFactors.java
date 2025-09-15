/**
 * The PrimeFactors class provides a method to print the prime factors of a given integer.
 * It includes a main method that serves as the entry point for the program and a helper method
 * to print the prime factors.
 *
 * @author simon
 */
public class PrimeFactors {

    /**
     * The main method that serves as the entry point for the program.
     * It takes a single command-line argument, parses it as an integer,
     * and prints the prime factors of the given number.
     *
     * @param args Command-line arguments where the first argument should be an integer.
     */
    public static void main(String... args) {
        if (args.length < 1) {
            return;
        }

        int prime = Integer.parseInt(args[0]);

        // prime factors
        System.out.printf("Prime Factors for %d:%n", prime);
        printPrimeFactors(prime);
    }


    /**
     * Prints the prime factors of a given number.
     *
     * This method takes an integer as input and prints its prime factors to the standard output.
     * It starts with the smallest prime number (2) and checks if it is a factor of the given number.
     * If it is, it prints the prime number and divides the given number by this prime factor.
     * It continues this process until the given number is reduced to 1.
     *
     * @param number the integer whose prime factors are to be printed
     */
    private static void printPrimeFactors(int number) {
        int i = 2;
        while (number > 1) {
            if (number % i == 0 && Primes.isPrimeFor(i)) {
                System.out.println(i);
                number = number / i;
            } else {
                i++;
            }
        }
    }

}
