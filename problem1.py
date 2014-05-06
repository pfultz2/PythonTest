import unittest

def problem1transform(c):
    if c.upper() in ['A', 'E', 'I', 'O', 'U']: return c.upper()
    else: return c.lower()

def problem1(seq):
    return [problem1transform(c) for c in reversed(seq)]

# Routines for testing purposes
def reversed_upper(seq):
    return [c.upper() for c in reversed(seq)]

def reversed_lower(seq):
    return [c.lower() for c in reversed(seq)]

class TestProblem1(unittest.TestCase):

    def setUp(self):
        self.vowels = ['A', 'E', 'I', 'O', 'U']
        self.consonants = ['B', 'C', 'D', 'F', 'G']
        self.mixed = ['A', 'B', 'C', 'D', 'E', '1']
        self.mixed_result = ['A', 'b', 'c', 'd', 'E', '1']


    def test_reverse(self):
        self.assertEqual(self.mixed, reversed_upper(problem1(self.mixed)))

    def test_vowels(self):
        self.assertEqual(reversed_upper(self.vowels), problem1(self.vowels))

    def test_consonants(self):
        self.assertEqual(reversed_lower(self.consonants), problem1(self.consonants))

    def test_mixed(self):
        self.assertEqual(list(reversed(self.mixed_result)), problem1(self.mixed))

if __name__ == '__main__':
    unittest.main()