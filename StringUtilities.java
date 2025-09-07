package task4;

public class StringUtilities {
    public static int firstIndexOf(char character, String word) {
        for (int i = 0; i < word.length(); i++) {
            if (word.charAt(i) == character) {
                return i;
            }
        }
        return -1;
    }
}
