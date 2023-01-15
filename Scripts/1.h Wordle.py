import random
import re
from nltk.corpus import brown

ww = list(set([x.upper() for x in brown.words() if len(x) == 5 and re.search(r"^A-Z|[\.,]", x) is None]))  # We don't know the original list of words in Wordle, so we'll just take all 5 letters words in the Brown corpus; we convert all of them to upper caps version for harmonisation puporses
word = random.choice(ww)  # We pick a random word

def play(answer):  # We create a function that returns all words in a given format depending on how close we are from the right answer
    answer = answer.upper()  # Get the all caps version of the word to compare with dataset of words
    if len(answer) > 5:  # We first check that the input word in answer fits the requirement: be 5 in len, and in the dataset
        print("Too long")
    elif len(answer) < 5:
        print("Too Short")
    elif answer not in ww:
        print("Word does not exist")
    else:  # If this is a proper guess, we proceed to the main part of the function
        for e, letter in enumerate(answer):  # The function enumerate allows you to iterate cver a list together with the index
            if letter in word and answer[e] == word[e]:  # If the letter is in the word and at the exact same place, we return a green square
                print('\x1b[1;30;42m' + letter + '\x1b[0m', end=" ")
            elif letter in word:  # If it is in the word, but at a different place, we return a yellow square
                print('\x1b[1;30;43m' + letter + '\x1b[0m', end=" ")
            else:  # Otherwise we just return the letter
                print(letter, end=" ")
