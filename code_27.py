import unittest

# Example function to be tested
def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

# Test case class derived from unittest.TestCase
class TestMathOperations(unittest.TestCase):

    # Test method to check the add function
    def test_add(self):
        self.assertEqual(add(3, 4), 7)  # This test should pass
        self.assertEqual(add(-1, 1), 0)  # This test should pass
        self.assertEqual(add(0, 0), 0)   # This test should pass

        self.assertNotEqual(add(0, 0), 10)   # This test should pass

    # Test method to check the subtract function
    def test_subtract(self):
        self.assertEqual(subtract(10, 5), 5)  # This test should pass
        self.assertEqual(subtract(-1, -1), 0)  # This test should pass
        self.assertEqual(subtract(0, 5), -5)   # This test should pass

        self.assertNotEqual(subtract(0, 5), 0)   # This test should pass

# Running the tests
if __name__ == "__main__":
    unittest.main()
