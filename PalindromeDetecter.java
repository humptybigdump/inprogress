package task1;

public final class PalindromeDetecter {
    private PalindromeDetecter() {
        // Utility class cannot be instantiated.
    }

    public static boolean isPalindrome(String word) {
        if (word.length() <= 1) {
            return true;
        }

        if (word.charAt(0) == word.charAt(word.length() - 1)) {
            return istPalindrom(word.substring(1, word.length() - 1));
        } else {
            return false;
        }
    }
}