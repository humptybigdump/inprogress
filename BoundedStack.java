
class BoundedStack {

    private final int stack[];
    private int pos;

    BoundedStack(int capacity) {
        this.stack = new int[capacity];
    }

    int pop() {
        return stack[pos--];
    }

    void push(int value) {
        stack[pos++] = value;
    }

    int size() {
        return pos;
    }

    int capacity() {
        return stack.length;
    }
}

class StackClient {

    /*@ public normal_behaviour
      @   requires \invariant_for(bs);
      @   ensures true;
      @*/
    void test(BoundedStack bs, int v, int w) {
        if(bs.capacity() >= bs.size() + 2) {
            bs.push(v);
            bs.push(w);
            int p1 = bs.pop();
            assert p1 == w;
            int p2 = bs.pop();
            assert p2 == v;
        } else {
            try {
                bs.push(v);
                bs.push(w);
                assert false;
            } catch(IndexOutOfBoundsException ex) {
                // expected!
            }
        }
    }
}
