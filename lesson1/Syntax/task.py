# 1

words = ["A", "Freckled", "and", "Frivolous", "Cake", "There", "Was"]

for el in words:
    print(el)

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
elif len(sentence) == 50:
    print("Third Condition Met")
elif len(sentence) >= 30 and "e" in sentence or "Cake" in sentence:
    print("Fourth Condition Met")
else:
    pass

# 4

print(True)

# 5

num_words = 0
for line in poem.split("\n"):
    if "cake" in line:
        num_words += 1
        if "knife" in line:
            num_words += 1
    elif "knife" in line:
        num_words += 1
print(num_words)
