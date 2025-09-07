class Ex1Solution {

    /*@ normal_behavior
      @  requires n >= 1;
      @  ensures \result == (\product int i; 1 <= i < n+1; i);
      @  measured_by n;
      @  assignable \strictly_nothing;
      @*/
    public static long factorialRec(long n) {
        if (n == 1)
            return 1;
        else
            return n * factorialRec(n-1);
    }

    /*@ normal_behavior
      @  requires n >= 1;
      @  ensures \result == (\product int i; 1 <= i < n+1; i);
      @  assignable \strictly_nothing;
      @*/
    public static long factorialIt(long n) {
        long res = 1;
        /*@ loop_invariant res == (\product int j; 1 <= j < i; j);
          @ loop_invariant 1 <= i && i <= n+1;
          @ decreases n + 1 - i;
          @ assignable \strictly_nothing;
          @*/
        for (int i = 1; i < n+1; i++) {
            res *= i;
        }
        return res;
    }
}
