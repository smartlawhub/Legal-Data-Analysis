# 1
import regex as re  # regex is typically abbreviated as re

with open("../../poem.txt", "r") as f:
    poem = f.read()


# 2

target_sentence = "Count: 3 frivolous cakes and 4 knifes !"
pattern = r"\d"
result = re.search(pattern, target_sentence)
print(result)

# 3

pattern = "cake|knife"
all_words = re.findall(pattern, poem)
print(len(all_words))

# 4

print(re.sub("Cake", "Hake (?!)", poem[:20]))
print(re.split(" ", poem[:20]))

# 5

sear = re.search(r"""(?<=the\s)   # A look-before condition
                    (?P<first>[A-Z]\w*?)  # first capitalised term we are looking for; note the ? after *
                    \s?  # Then we look for a white space
                    (?P<second>[A-Z]\w*?$)  # and finally the second capitalised word""", poem, re.M | re.X)
print(sear.group("first"))
print(sear.group("second"))


#TODO : Revise Exercise (too hard)
