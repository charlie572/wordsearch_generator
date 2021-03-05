import unittest
import wordsearch_generator as wg
from random import seed


class CreateEmptyGridTestCase(unittest.TestCase):
    def test_zero_dimensions(self):
        self.assertEqual([], wg.create_empty_grid(0, 0))

    def test_zero_height(self):
        self.assertEqual([], wg.create_empty_grid(4, 0))

    def test_zero_width(self):
        self.assertEqual([[] for _ in range(4)], wg.create_empty_grid(0, 4))

    def test_unit_dimensions(self):
        self.assertEqual([[None]], wg.create_empty_grid(1, 1))

    def test_square(self):
        self.assertEqual([[None] * 4] * 4, wg.create_empty_grid(4, 4))

    def test_wide_rectangle(self):
        self.assertEqual([[None] * 5] * 4, wg.create_empty_grid(5, 4))

    def test_tall_rectangle(self):
        self.assertEqual([[None] * 4] * 5, wg.create_empty_grid(4, 5))


class GridToStrTestCase(unittest.TestCase):
    def test_zero_dimensions(self):
        self.assertEqual("", wg.grid_to_str([]))

    def test_zero_width(self):
        grid = [[] for _ in range(4)]
        self.assertEqual("", wg.grid_to_str(grid))

    def test_zero_height(self):
        self.assertEqual("", wg.grid_to_str([]))

    def test_square(self):
        grid = [['a', 'b', 'c'],
                ['d', 'e', 'f'],
                ['g', 'h', 'i']]
        expected = "a b c\nd e f\ng h i"
        self.assertEqual(expected, wg.grid_to_str(grid))

    def test_wide_rect(self):
        grid = [['a', 'b', 'c'],
                ['d', 'e', 'f']]
        expected = "a b c\nd e f"
        self.assertEqual(expected, wg.grid_to_str(grid))

    def test_tall_rect(self):
        grid = [['a', 'b'],
                ['c', 'd'],
                ['e', 'f']]
        expected = "a b\nc d\ne f"
        self.assertEqual(expected, wg.grid_to_str(grid))


class FillBlanksRandomlyTestCase(unittest.TestCase):
    def test_get_random_char(self):
        seed(112342)
        char = wg.get_random_char()
        self.assertTrue(97 <= ord(char) <= 122)

    def test_fill_blanks_randomly(self):
        grid = [[None, 'b', None],
                ['d', None, 'f'],
                [None, None, 'i']]

        wg.fill_blanks_randomly(grid)
        for r, row in enumerate(grid):
            for c, element in enumerate(row):
                with self.subTest(msg=f"element at (c, r) is None"):
                    self.assertTrue(element is not None)


if __name__ == '__main__':
    unittest.main()
