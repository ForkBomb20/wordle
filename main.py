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

    greens = []
    yellows = []
    grays = []

    while playing:
        word = input("Please enter the word you played").strip()
        letters = [char for char in word]

        for i in range(len(letters)):
            color = input(f"What color is {letters[i]}? g (green), y (yellow), n (gray)").strip()
            if color == "g" and not (letters[i], i) in greens:
                greens.append((letters[i], i))
            elif color == "y" and not (letters[i], i) in yellows:
                yellows.append((letters[i], i))
            elif color == "n" and (not ((letters[i], i) in grays)):
                grays.append(letters[i])

        global allowed
        allowed = possible(greens, yellows, grays, allowed)
        es = [entropy(word, allowed) for word in allowed]
        max_e = max(es)
        ind = es.index(max_e)

        print(f"Play {allowed[ind]}\nEntropy: {max_e}\n")
        print(f"Allowed words: {allowed}")
        playing = input("Would you like to stop (s)?").strip().lower() != "s"

        grays.clear()
        yellows.clear()
        greens.clear()


if __name__ == "__main__":
    main()
