import unittest


def problem1(seq):
    return list(reversed(seq))

class TestProblem1(unittest.TestCase):

    def setUp(self):
        self.mixed = ['A', 'B', 'C', 'D', 'E']

    def test_reverse(self):
        result = [c.upper() for c in reversed(problem1(self.mixed))]
        self.assertEqual(self.mixed, result)


if __name__ == '__main__':
    unittest.main()