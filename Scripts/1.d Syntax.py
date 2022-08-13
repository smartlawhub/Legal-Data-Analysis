f = open("poem.txt", "r")   # We open and load the poem file with the built-in function "open", which takes as arguments a path (here, the name of the file), and a method ("r" for "read")
poem = f.read()  # The function "open" created an object that comes with its own methods, of which "read()" renders a string

# 1

words = ["A", "Freckled", "and", "Frivolous", "Cake", "There", "Was"]

for el in words:
    print(el)

recreated_text = ""  # We start by creating an empty text variable
for letter in "Swordfish":   # We loop over the string Swordfish (strings can be used as lists of characters, so loops work there)
    print(letter)  # We first print the letters, one by one
    recreated_text += letter  # Then we add the letter to the existing recreated text
    print(recreated_text)  # And we print the recreated text to see where we are at

# 2

for word in words:
    if "e" in word:
        print(word)
    else:
        print(word, " : No 'e' in that word")

# 3

sentence = " ".join(words)
print(sentence)
my_bol = False

if "frivolous" in sentence:
    print("First Condition Met")
elif my_bol:
    print("Second Condition Met")
elif len(sentence) == 50:   # len() is a built-in function rendering the length of a list or string
    print("Third Condition Met")
elif len(sentence) >= 30 and "e" in sentence or "Cake" in sentence:
    print("Fourth Condition Met")
else:
    pass

# Exercise 3

print(poem)  # This is the full poem, but try printing it without using print to find a hint about the exercise
