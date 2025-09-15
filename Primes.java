/**
 * The {@code Primes} class provides methods to check if a given number is a prime number.
 * It includes two methods: one using a for loop and another using a while loop.
 * 
 * @author simon
 */
public class Primes {
    /**
     * Checks if a given number is a prime number using a while loop.
     *
     * @param candidate the number to check for primality
     * @return {@code true} if the candidate is a prime number, {@code false} otherwise
     */
    public static boolean isPrimeFor(int candidate) {
        if (candidate < 2) { // there is no prime < 2
            return false;
        }
        for (int i = 2; i < candidate; i++) {
            if (candidate % i == 0) {
                return false;
            }
        }
        return true;
    }

    /**
     * Checks if a given number is a prime number using a while loop.
     *
     * @param candidate the number to check for primality
     * @return {@code true} if the candidate is a prime number, {@code false} otherwise
     */
    public static boolean isPrimeWhile(int candidate) {
        if (candidate < 2) { // there is no prime < 2
            return false;
        }

        int i = 2;
        while (i < candidate) {
            if (candidate % i == 0) {
                return false;
            }
            i++;
        }
        return true;
    }
}
