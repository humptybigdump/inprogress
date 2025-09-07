package test;

import edu.kit.kastel.StringUtility;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class StringActionTest {
    @Test
    void testVowel() {
        assertEquals("Hll, Wrld!", StringUtility.removeVowels("Hello, World!"));
    }
}