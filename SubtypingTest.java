import org.checkerframework.checker.optionaldemo.qual.*;

// Test subtyping relationships for the OptionalDemo Checker.
class SubtypeTest {
  void allSubtypingRelationships(@MaybePresent int x, @Present int y) {
    @MaybePresent int a = x;
    @MaybePresent int b = y;
    // :: error: (assignment.type.incompatible)
    @Present int c = x; // expected error on this line
    @Present int d = y;
  }
}
