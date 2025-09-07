package tests;

import java.io.File;
import java.util.List;
import org.checkerframework.checker.optionaldemo.OptionalDemoChecker;
import org.checkerframework.framework.test.CheckerFrameworkPerDirectoryTest;
import org.junit.runners.Parameterized.Parameters;

/**
 * Test runner for tests of the OptionalDemo Checker.
 *
 * <p>Tests appear as Java files in the {@code tests/optionaldemo} folder. To add a new test case,
 * create a Java file in that directory. The file contains "// ::" comments to indicate expected
 * errors and warnings; see
 * https://github.com/typetools/checker-framework/blob/master/checker/tests/README .
 */
public class OptionalDemoTest extends CheckerFrameworkPerDirectoryTest {
    public OptionalDemoTest(List<File> testFiles) {
        super(
                testFiles,
                OptionalDemoChecker.class,
                "optionaldemo",
                "-Anomsgtext",
                "-AstubWarnIfNotFound",
                "-nowarn");
    }

    @Parameters
    public static String[] getTestDirs() {
        return new String[] {"optionaldemo"};
    }
}
