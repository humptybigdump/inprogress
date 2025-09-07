import org.checkerframework.checker.optionaldemo.qual.*;
import java.util.Optional;

class IsPresentFlowTest {
    void foo(@MaybePresent Optional<Object> x) {
        // :: error: method.invocation.invalid
        x.get().toString();

        if (x.isPresent()) {
            x.get().toString();
        }

        // :: error: method.invocation.invalid
        x.get().toString();
    }
}
