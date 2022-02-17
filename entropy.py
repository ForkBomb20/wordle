"""
Nathan Kawamoto
Wordle Bot Helpers
Inspired by 3Blue1Brown's wordle bot. This bot utilizes the official list of 2,315
possible Wordle words and the concepts of entropy and information theory to produce optimal
words for play.
"""

from math import log2
import itertools

# A list of all 243 possible combinations of greens, yellows and grays
# a word could have when played for use in entropy function
PATTERNS = list(itertools.product("gyn", repeat=5))


# entropy function that takes in a word to be played and returns the
# average bits of information likely to result from it
def entropy(word: str, allowed: list) -> float:
    e_sum = 0
    for pattern in PATTERNS:
        greens = []
        yellows = []
        grays = []

        for i in range(len(pattern)):
            if pattern[i] == "g":
                greens.append((word[i], i))
            elif pattern[i] == "y":
                yellows.append((word[i], i))
            else:
                grays.append(word[i])

        p = probability(greens, yellows, grays, allowed)
        if p != 0:
            i = information(p)
            e_sum += p * i

    return e_sum


# Information function that return the expected information for a given probability
def information(p: float) -> float:
    return -log2(p)


# Probability function supplementing information function that takes a list of
# green, yellow, and gray letters for a Wordle play and computes all possible
# remaining words using possible function and return the probability by
# dividing the new length of possible words by the old
def probability(greens: list, yellows: list, grays: list, allowed: list) -> float:
    po = possible(greens, yellows, grays, allowed)
    prob = len(po) / len(allowed)
    return prob


# Possible function supplementing probability function that return all the
# words from the wordle list that could match the greens, yellows, and grays
# given as input
def possible(greens: list, yellows: list, grays: list, allowed: list) -> list:
    def hasDuplicates(letters):
        letters = [letter for (letter, ind) in letters]
        return len(letters) != len(set(letters))

    def getDuplicates(letters):
        duplicates = []
        letters = [letter for (letter, ind) in letters]
        for letter in letters:
            if letters.count(letter) > 1:
                duplicates.append(letter)

        return set(duplicates)

    possible_words = []

    for (letter, ind) in greens:
        if letter in grays: grays = [l for l in grays if l != letter]

    for (letter, ind) in yellows:
        if letter in grays: grays = [l for l in grays if l != letter]

    for word in allowed:
        # Boolean for whether the current word has all green letters in the proper positions
        right_greens = all([(word[ind] == letter) or (word[ind] == letter and letter in word) for (letter, ind) in greens])
        # Boolean for whether the current word does not have yellow letters in the same place
        no_yellows = all([word[ind] != letter for (letter, ind) in yellows])
        # Boolean for whether the current word has yellows in it
        if hasDuplicates(yellows):
            yellow_letters = [letter for (letter, ind) in yellows]
            duplicates = getDuplicates(yellows)
            has_yellows = all([yellow_letters.count(letter) == word.count(letter) for letter in duplicates])

        else:
            has_yellows = all([letter in word and word.count(letter) == 1 for (letter, ind) in yellows])
        # Boolean for whether the current word does not have any gray letters
        no_grays = all([(not (letter in word)) for letter in grays])

        if right_greens and no_yellows and has_yellows and no_grays:
            possible_words.append(word)

    return possible_words
