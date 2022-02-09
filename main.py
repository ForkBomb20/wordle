from math import log2
import json
import itertools

file = open("words.json")
data = json.load(file)
allowed = data["allowed"]

PATTERNS = list(itertools.product("gyn", repeat=5))

def entropy(word):
    sum = 0
    for pattern in PATTERNS:
        greens = {}
        yellows = {}
        grays = []

        for i in range(len(pattern)):
            if pattern[i] == "g": greens[word[i]] = i
            elif pattern[i] == "y": yellows[word[i]] = i
            else: grays.append(word[i])

        p = probability(greens, yellows, grays)
        if p != 0:
            i = informaton(p)
            sum += p * i

    return sum

def informaton(p):
    return -log2(p)

def probability(greens: dict, yellows: list, grays: list) -> (int, list):
    po = possible(greens, yellows, grays)
    prob = len(po) / len(allowed)
    return prob

def possible(greens, yellows, grays):
    possible = []

    for word in allowed:
        right_greens = all([word[greens[letter]] == letter for letter in greens])
        # has_yellows = all((([word[yellows[letter]] != letter and (letter in word) for letter in yellows]))
        # has_yellows = all([(((word[yellows[letter]] != letter) and (letter in word)) for letter in yellows)])
        no_yellows = all([word[yellows[letter]] != letter for letter in yellows])
        has_yellows = all([letter in word for letter in yellows])
        no_grays = all([(not (letter in word)) for letter in grays])

        if right_greens and no_yellows and has_yellows and no_grays:
            possible.append(word)

    return possible

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
            if color == "g" and not letters[i] in greens: greens[letters[i]] = i
            elif color == "y" and not letters[i] in yellows: yellows[letters[i]] = i
            elif (color == "n" and (not (letters[i] in grays))): grays.append(letters[i])

        for letter in greens:
            if letter in grays: grays = [l for l in grays if l != letter]

        for letter in yellows:
            if letter in grays: grays = [l for l in grays if l != letter]

        print(greens, yellows, grays)
        allowed = possible(greens, yellows, grays)
        print(allowed)
        es = [entropy(word) for word in allowed]
        max_e = max(es)
        ind = es.index(max_e)

        print(f"Play {allowed[ind]}\nEntropy: {max_e}")


if __name__ == "__main__":
    main()





