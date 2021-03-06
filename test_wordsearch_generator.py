import unittest
from copy import deepcopy

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
                with self.subTest(msg=f"Check that element at ({c}, {r}) is not None"):
                    self.assertTrue(element is not None)


class InsertSingleWordsTestCase(unittest.TestCase):
    def test_horizontal_normal(self):
        grid = [[None] * 4 for _ in range(4)]
        expected = [['b', 'a', 'c', 'k'],
                    [None] * 4,
                    [None] * 4,
                    [None] * 4]

        inserted_correctly = wg.insert_word_horizontally(grid, "back", 0, 0)

        self.assertTrue(inserted_correctly)
        self.assertEqual(expected, grid)

    def test_vertical_normal(self):
        grid = [[None] * 4 for _ in range(4)]
        expected = [['b', None, None, None],
                    ['a', None, None, None],
                    ['c', None, None, None],
                    ['k', None, None, None]]

        inserted_correctly = wg.insert_word_vertically(grid, "back", 0, 0)

        self.assertTrue(inserted_correctly)
        self.assertEqual(expected, grid)

    def test_horizontal_overlap(self):
        grid = [['b', None, None, None],
                ['a', None, None, None],
                ['c', None, None, None],
                ['k', None, None, None]]
        expected = [['b', 'a', 'c', 'k'],
                    ['a', None, None, None],
                    ['c', None, None, None],
                    ['k', None, None, None]]

        inserted_correctly = wg.insert_word_horizontally(grid, "back", 0, 0)

        self.assertTrue(inserted_correctly)
        self.assertEqual(expected, grid)

    def test_vertical_overlap(self):
        grid = [['b', 'a', 'c', 'k'],
                [None] * 4,
                [None] * 4,
                [None] * 4]
        expected = [['b', 'a', 'c', 'k'],
                    ['a', None, None, None],
                    ['c', None, None, None],
                    ['k', None, None, None]]

        inserted_correctly = wg.insert_word_vertically(grid, "back", 0, 0)

        self.assertTrue(inserted_correctly)
        self.assertEqual(expected, grid)

    def test_horizontal_overwrite(self):
        grid = [['q', None, None, None],
                ['a', None, None, None],
                ['c', None, None, None],
                ['k', None, None, None]]
        expected = deepcopy(grid)

        inserted_correctly = wg.insert_word_horizontally(grid, "back", 0, 0)

        self.assertFalse(inserted_correctly)
        self.assertEqual(expected, grid)

    def test_vertical_overwrite(self):
        grid = [['q', 'a', 'c', 'k'],
                [None] * 4,
                [None] * 4,
                [None] * 4]
        expected = deepcopy(grid)

        inserted_correctly = wg.insert_word_vertically(grid, "back", 0, 0)

        self.assertFalse(inserted_correctly)
        self.assertEqual(expected, grid)


class IterateWordSpacesTestCase(unittest.TestCase):
    def test_normal(self):
        grid = [[None] * 4 for _ in range(4)]
        expected_grids = [
            [['c', 'a', 't', None],
             [None] * 4,
             [None] * 4,
             [None] * 4],
            [[None, 'c', 'a', 't'],
             [None] * 4,
             [None] * 4,
             [None] * 4],
            [[None] * 4,
             [None] * 4,
             [None] * 4,
             ['c', 'a', 't', None]],
            [[None] * 4,
             [None] * 4,
             [None] * 4,
             [None, 'c', 'a', 't']],
            [[None, None, None, 'c'],
             [None, None, None, 'a'],
             [None, None, None, 't'],
             [None] * 4],
            [[None] * 4,
             [None, None, None, 'c'],
             [None, None, None, 'a'],
             [None, None, None, 't']]
        ]

        actual_grids = list(wg.iterate_word_spaces(grid, "cat"))

        for i, expected_grid in enumerate(expected_grids):
            with self.subTest(msg=f"Check that grid {i} is yielded"):
                self.assertIn(expected_grid, actual_grids)

    def test_zero_width(self):
        grid = [[] for _ in range(4)]
        grids_generated = list(wg.iterate_word_spaces(grid, "cat"))
        self.assertEqual(0, len(grids_generated))

    def test_zero_height(self):
        grid = []
        grids_generated = list(wg.iterate_word_spaces(grid, "cat"))
        self.assertEqual(0, len(grids_generated))

    def test_iterate_word_spaces_randomly(self):
        """Test that iterate_word_spaces_randomly produces the same output as iterate_word_spaces (not necessarily in
        the same order)"""
        grid = [[None] * 4 for _ in range(4)]

        non_random_grids = wg.iterate_word_spaces(grid, "cat")
        random_grids = list(wg.iterate_word_spaces_randomly(grid, "cat"))

        for i, grid in enumerate(non_random_grids):
            with self.subTest(msg=f"Test grid {i} is present"):
                self.assertIn(grid, random_grids)


class InsertAllWordsTestCase(unittest.TestCase):
    def test_insert_words_succeeds(self):
        grid = [[None] * 4 for _ in range(4)]
        words = ["cat", "mad", "stun", "put", "ban"]
        generated_grid = wg.insert_words(grid, words)
        self.assertTrue(generated_grid is not None)

    def test_insert_words_randomly_succeeds(self):
        grid = [[None] * 4 for _ in range(4)]
        words = ["cat", "mad", "stun", "put", "ban"]
        generated_grid = wg.insert_words_randomly(grid, words)
        self.assertTrue(generated_grid is not None)


if __name__ == '__main__':
    unittest.main()
