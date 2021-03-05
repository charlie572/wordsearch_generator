"""Generate wordsearches

Wordsearches are represented as two-dimensional lists e.g.
    [['a', 'b', 'c', 'd'],
     ['e', 'f', 'g', 'h']]

To create a wordsearch, create an empty grid using the create_empty_grid() function, then use the
insert_words_randomly() or insert_words() functions to populate the grid. Finally, use fill_blanks_randomly() to fill in
the blank spaces with random characters.

All the functions that modify the grid do so in-place.
"""
from random import randint


def create_empty_grid(width, height):
    """Create an empty grid

    :param width: The width of the grid
    :type width: int
    :param height: The height of the grid
    :type height: int
    :return: The empty grid
    :rtype: list
    """
    return [[None] * width for _ in range(height)]


def grid_to_str(grid):
    """Convert a grid to a string

    :param grid: The grid to convert
    :type grid: list
    :return: The string representation
    :rtype: str
    """
    result = ""

    if len(grid) > 0 and len(grid[0]) > 0:
        for row in grid:
            row = [str(c) for c in row]
            result += " ".join(row) + "\n"

    result = result[:-1]
    return result


def get_random_char():
    """Get a random character

    Only lower case characters are returned.

    :return: A single character
    :rtype: str
    """
    return chr(randint(97, 122))


def fill_blanks_randomly(grid):
    """Fill blank spaces with random characters

    Every element of the grid that is None will be replaced by a random lowercase character.

    :param grid: The grid to fill in the blanks of
    :type grid: list
    """
    for row in grid:
        for i in range(len(row)):
            if row[i] is None:
                row[i] = get_random_char()


def insert_words_randomly(grid, words):
    """Insert words randomly into a grid

    The words from the list are inserted in random locations and orientations. The words may intersect, but they will
    not overwrite each other. However, anything that is already in the grid may be overwritten, so the grid should be
    empty.

    This function words in-place.

    :param grid: An empty grid to insert the words into
    :type grid: list
    :param words: The words to insert
    :type words: list
    """
    pass


def insert_words(grid, words):
    """Insert words randomly into a grid

    The words from the list are inserted in the first available configuration found. The words may intersect, but they
    will not overwrite each other. However, anything that is already in the grid may be overwritten, so the grid should
    be empty.

    This function words in-place.

    :param grid: An empty grid to insert the words into
    :type grid: list
    :param words: The words to insert
    :type words: list
    """
    pass


def main():
    pass


if __name__ == "__main__":
    main()
