"""
Nathan Kawamoto
Wordle Bot Main
Inspired by 3Blue1Brown's wordle bot. This bot utilizes the official list of 2,315
possible Wordle words and the concepts of entropy and information theory to produce optimal
words for play.
"""

from entropy import entropy, possible
import json

# Opening and formatting json of words into a list
file = open("words.json")
data = json.load(file)
allowed = data["allowed"]


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

        print(f"Play {allowed[ind]}\nEntropy: {max_e}\n")
        playing = input("Would you like to stop (s)?").strip().lower() == "s"


if __name__ == "__main__":
    main()
