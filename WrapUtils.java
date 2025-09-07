public class WrapUtils {

    /**
     * This method replaces every space character by a linefeed character ('\n').
     *
     * It requires that s is not null.
     *
     * 1. It never crashes.
     * 2. It always terminates.
     * 3. The only changes made to the heap are to the entries in s.
     * 4. The only changes in s are turning all occurrences of ' ' into '\n'.
     * 5. All other characters of the array are left unchanged.
     */
    public static void replaceSpaces(char[] s) {
        // TODO
    }

    /**
     * This method is a simple line wrapping method.
     *
     * It requires that s is not null, and lineLength must be positive.
     *
     * 1. It never crashes.
     * 2. It always terminates.
     * 3. The only changes made to the heap are to the entries in s.
     * 4. The only changes in s are turning ' ' into '\n'.
     * 5. (Extra) Every line (but the last) has at least lineLength characters.
     */
    public static void wrapLines(char[] s, int lineLength) {

        int lastBreak = -1;
        int lastSpace = indexOf(s, ' ', 0);

        while(lastSpace != -1) {
            if(lastSpace - lastBreak > lineLength) {
                s[lastSpace] = '\n';
                lastBreak = lastSpace;
            }
            lastSpace = indexOf(s, ' ', lastSpace+1);
        }
    }

    /**
     * This method looks for a character in a character array.
     *
     * It requires that s is not null, from must be a valid index into s.
     *
     * 1. It never crashes.
     * 2. It always terminates.
     * 3. It returns -1 if c is not in s at any index >= from.
     * 4. It returns the smallest index into s that has value c 
     *    and is not before index from (if it exists).
     * 5. No heap is changed, no object is created.
     */
    private static int indexOf(char[] s, char c, int from) {

        for(int k = from; k < s.length; k++) {
            if(s[k] == c) {
                return k;
            }
        }
        
        return -1;
    }
}
