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
def entropy(word: str) -> float:
    e_sum = 0
    for pattern in PATTERNS:
        greens = {}
        yellows = {}
        grays = []

        for i in range(len(pattern)):
            if pattern[i] == "g":
                greens[word[i]] = i
            elif pattern[i] == "y":
                yellows[word[i]] = i
            else:
                grays.append(word[i])

        p = probability(greens, yellows, grays)
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
def probability(greens: dict, yellows: dict, grays: list) -> float:
    po = possible(greens, yellows, grays)
    prob = len(po) / len(allowed)
    return prob


# Possible function supplementing probability function that return all the
# words from the wordle list that could match the greens, yellows, and grays
# given as input
def possible(greens: dict, yellows: dict, grays: list) -> list:
    possible_words = []

    for word in allowed:
        # Boolean for whether the current word has all green letters in the proper positions
        right_greens = all([word[greens[letter]] == letter for letter in greens])
        # Boolean for whether the current word does not have yellow letters in the same place
        no_yellows = all([word[yellows[letter]] != letter for letter in yellows])
        # Boolean for whether the current word has yellows in it
        has_yellows = all([letter in word for letter in yellows])
        # Boolean for whether the current word does not have any gray letters
        no_grays = all([(not (letter in word)) for letter in grays])

        if right_greens and no_yellows and has_yellows and no_grays:
            possible_words.append(word)


    return possible_words


def main():
    playing = True

    greens = {}
    yellows = {}
    grays = []

    while playing:
        word = input("Please enter the word you played").strip()
        letters = [char for char in word]

        for i in range(len(letters)):
            color = input(f"What color is {letters[i]}? g (green), y (yellow), n (gray)").strip()
            if color == "g" and not letters[i] in greens:
                greens[letters[i]] = i
            elif color == "y" and not letters[i] in yellows:
                yellows[letters[i]] = i
            elif color == "n" and (not (letters[i] in grays)):
                grays.append(letters[i])

        for letter in greens:
            if letter in grays: grays = [l for l in grays if l != letter]

        for letter in yellows:
            if letter in grays: grays = [l for l in grays if l != letter]

        allowed = possible(greens, yellows, grays)
        es = [entropy(word) for word in allowed]
        max_e = max(es)
        ind = es.index(max_e)

        print(f"Play {allowed[ind]}\nEntropy: {max_e}")


if __name__ == "__main__":
    main()
