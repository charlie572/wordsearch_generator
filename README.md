# Wordsearch Generator

This project generates wordsearches using a recursive backtracking method.

## Usage

`wordsearch_generator.py [-h] [--words [WORDS [WORDS ...]]] [--words-file WORDS_FILE] width height`


Run wordsearch_generator.py, specifying either a list of words, or a text file.
If a text file is used, it must contain the words on separate lines.

E.g. `python wordsearch_generator.py 10 10 --words "wander" "meringue" "lemon"`

Run `python wordsearch_generator.py -h` for more help.

## Technologies

Language: python 3.8.1