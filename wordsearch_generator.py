"""Generate wordsearches

Wordsearches are represented as two-dimensional lists e.g.
    [['a', 'b', 'c', 'd'],
     ['e', 'f', 'g', 'h']]

To create a wordsearch, create an empty grid using the create_empty_grid() function, then use the
insert_words_randomly() or insert_words() functions to populate the grid. Finally, use fill_blanks_randomly() to fill in
the blank spaces with random characters.

All the functions that modify the grid do so in-place unless otherwise stated.
"""
from copy import deepcopy
from random import randint, shuffle


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


def insert_word_horizontally(grid, word, x, y):
    """Insert a word horizontally into a grid

    If the word would overwrite any characters that are already in the grid, then the word doesn't fit into this space.
    The function returns True if the word was successfully inserted.

    A word will still be inserted if it overlaps another word without overwriting any letters i.e the words can cross at
    a common letter.

    This function does not check if a word is out of the bounds of the grid.

    :param grid: The grid to insert the word into
    :type grid: list
    :param word: The word to insert
    :type word: str
    :param x: The x coordinate of the first letter (the first column has x coordinate 0)
    :type x: int
    :param y: The y coordinate of the first letter (the first row has y coordinate 0)
    :type y: int
    :return: True if the word was successfully inserted, else False
    :rtype: bool
    """
    # check if the word fits in this space
    for i in range(len(word)):
        grid_char = grid[y][x + i]
        if grid_char is not None and grid_char != word[i]:
            return False  # the word doesn't fit into this space

    # insert the word
    for i in range(len(word)):
        grid[y][x + i] = word[i]

    return True


def insert_word_vertically(grid, word, x, y):
    """Insert a word vertically into a grid

    If the word would overwrite any characters that are already in the grid, then the word doesn't fit into this space.
    The function returns True if the word was successfully inserted.

    A word will still be inserted if it overlaps another word without overwriting any letters i.e the words can cross at
    a common letter.

    This function does not check if a word is out of the bounds of the grid.

    :param grid: The grid to insert the word into
    :type grid: list
    :param word: The word to insert
    :type word: str
    :param x: The x coordinate of the first letter (the first column has x coordinate 0)
    :type x: int
    :param y: The y coordinate of the first letter (the first row has y coordinate 0)
    :type y: int
    :return: True if the word was successfully inserted, else False
    :rtype: bool
    """
    # check if the word fits in this space
    for i in range(len(word)):
        grid_char = grid[y + i][x]
        if grid_char is not None and grid_char != word[i]:
            return False

    # insert the word
    for i in range(len(word)):
        grid[y + i][x] = word[i]

    return True


def iterate_word_spaces(grid, word):
    """Iterate over the possible ways to insert a word

    This generator yields the grid corresponding to every possible way of inserting the word horizontally or vertically.
    It doesn't yield any grid where characters are overwritten i.e. the word doesn't fit.

    :param grid: The grid that the word is being inserted into
    :type grid: list
    :param word: The word that is being inserted
    :type word: str
    """
    height = len(grid)
    width = len(grid[0]) if height > 0 else 0

    temp_grid = deepcopy(grid)

    # horizontal spaces
    for x in range(width - len(word) + 1):
        for y in range(height):
            word_fits = insert_word_horizontally(temp_grid, word, x, y)
            if word_fits:
                yield temp_grid
                temp_grid = deepcopy(grid)  # reset temp_grid so the next word location can be generated

    # vertical spaces
    for y in range(height - len(word) + 1):
        for x in range(width):
            word_fits = insert_word_vertically(temp_grid, word, x, y)
            if word_fits:
                yield temp_grid
                temp_grid = deepcopy(grid)


def iterate_word_spaces_randomly(grid, word):
    """Iterate randomly over the possible ways to insert a word

    This generator yields the grid corresponding to every possible way of inserting the word horizontally or vertically.
    It doesn't yield any grid where characters are overwritten i.e. the word doesn't fit.

    :param grid: The grid that the word is being inserted into
    :type grid: list
    :param word: The word that is being inserted
    :type word: str
    """
    # This function works by generating possible locations for the word, shuffling them, then yielding the corresponding
    # grids with the word inserted.

    height = len(grid)
    width = len(grid[0]) if height > 0 else 0

    # ************** generate spaces ****************

    # horizontal spaces
    spaces = []
    for x in range(width - len(word) + 1):
        for y in range(height):
            spaces.append((x, y, True))

    # vertical spaces
    for y in range(height - len(word) + 1):
        for x in range(width):
            spaces.append((x, y, False))

    # ************** shuffle spaces ****************
    shuffle(spaces)

    # **************** yield grids *********************
    temp_grid = deepcopy(grid)
    for x, y, horizontal in spaces:
        if horizontal:
            word_fits = insert_word_horizontally(temp_grid, word, x, y)
        else:
            word_fits = insert_word_vertically(temp_grid, word, x, y)

        if word_fits:
            yield temp_grid
            temp_grid = deepcopy(grid)  # reset temp_grid so the next word location can be generated


def insert_words_randomly(grid, words):
    """Insert words randomly into a grid

    The words from the list are inserted in random locations and orientations. The words may intersect, but they will
    not overwrite each other. However, anything that is already in the grid may be overwritten, so the grid should be
    empty.

    This function does not work in-place. It returns the new grid with the words inserted, or returns None is there is
    no solution.

    :param grid: An empty grid to insert the words into
    :type grid: list
    :param words: The words to insert
    :type words: list
    :return: The new grid with the words inserted
    :rtype: list
    """
    # This function works the same as insert_words, but it uses iterate_word_spaces_randomly instead of
    # iterate_word_spaces.

    if len(words) == 0:
        return grid

    for temp_grid in iterate_word_spaces_randomly(grid, words[0]):
        temp_grid = insert_words_randomly(temp_grid, words[1:])
        if temp_grid is not None:
            return temp_grid

    return None  # There are no possible ways to insert this word, so we backtrack.


def insert_words(grid, words):
    """Insert words randomly into a grid

    The words from the list are inserted in the first available configuration found. The words may intersect, but they
    will not overwrite each other. However, anything that is already in the grid may be overwritten, so the grid should
    be empty.

    This function does not work in-place. It returns the new grid with the words inserted, or returns None is there is
    no solution.

    :param grid: An empty grid to insert the words into
    :type grid: list
    :param words: The words to insert
    :type words: list
    :return: The new grid with the words inserted
    :rtype: list
    """
    # This function uses a recursive backtracking method. The base case is when there are no more words to insert. It
    # backtracks when it has gone through all of possible ways to insert the next word.

    if len(words) == 0:
        return grid

    for temp_grid in iterate_word_spaces(grid, words[0]):
        temp_grid = insert_words(temp_grid, words[1:])
        if temp_grid is not None:
            return temp_grid

    return None  # There are no possible ways to insert this word, so we backtrack.


def main():
    pass


if __name__ == "__main__":
    main()
