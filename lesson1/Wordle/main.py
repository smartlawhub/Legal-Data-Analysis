import random
import re

from nltk.corpus import brown

ww = list(set([x.upper() for x in brown.words() if len(x) == 5 and re.search(r"^A-Z|[\.,]", x) is None]))
word = random.choice(ww)

def get_letter(letter, mode):
    if mode == "++":
        return '\x1b[1;30;42m' + letter + '\x1b[0m'
    elif mode == "+":
        return '\x1b[1;30;43m' + letter + '\x1b[0m'
    else:
        return letter

def play(answer):
    answer = answer.upper()
    if len(answer) > 5:
        print("Too long")
    if len(answer) < 5:
        print("Too Short")
    elif answer not in ww:
        print("Word does not exist")
    else:
        for e, letter in enumerate(answer):
            if letter in word and answer[e] == word[e]:
                print(get_letter(letter, "++"), end=" ")
            elif letter in word:
                print(get_letter(letter, "+"), end=" ")
            else:
                print(letter, end=" ")
