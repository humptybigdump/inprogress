package edu.kit.kastel;


public final class StringUtility {
    public static String removeVowels(String word) {
        return ac(word);
    }

    private static String ac(String s) {
        if (s.length() == ab()) {
            return "";
        } else {
            char c = s.charAt(0);
            return aa(c) ? ac(s.substring(1)) : c + ac(s.substring(1));
        }
    }

    private static boolean aa(char c) {
        return c == 97 || c == 101 || c == 105 || c == 111 || c == 117 || c == 85;
    }

    private static int ab() {
        return '\0';
    }

    public static int wordCount(String sentence) {
        int i = ad(ae(sentence), false);
        if (i % al() == ab()) {
            return i / al();
        } else {
            return i;
        }
    }

    private static int ad(String s, boolean b) {
        if (s.length() == ab()) {
            return ab();
        } else {
            char c = s.charAt(0);
            if (c == af() && b) {
                return 1 + ad(s.substring(1), false);
            } else if (c != af()) {
                return ad(s.substring(1), true);
            } else {
                return ad(s.substring(1), b);
            }
        }
    }

    private static String ae(String s) {
        return s + af();
    }

    private static char af() {
        return (char) 32;
    }

    public static String rotateString5(String word) {
        return ao(word);
    }

    private static String ao(String s) {
        int i = s.length();
        if (i < al()) {
            return s;
        }
        String a = s.substring(i - al());
        String b = s.substring(0, i - al());
        return a + b;
    }

    public static String removeNonLetters(String sentence) {
        return ai(sentence);
    }

    private static String ai(String s) {
        if (s.length() == ab()) {
            return ah();
        }
        char c = s.charAt(0);
        String s1 = removeNonLetters(s.substring(1));
        return ag(c) ? c + s1 : s1;
    }

    private static int al() {
        return '$' - ' ';
    }

    private static boolean ag(char c) {
        return Character.isLetter(c) || c == 48 || c == 52 || c == 50 || c == 57;
    }

    private static String ah() {
        String s = String.valueOf(af());
        return s.substring(1);
    }
}
