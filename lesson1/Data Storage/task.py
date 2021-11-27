import os
import regex as re

f = open("text.txt", encoding="utf8")
poem = f.read()
print(poem)
f.close()

with open("poem.txt", "ab", encoding="utf8") as f:
    f.write(poem)

f = open("poem.txt")
text = f.read()
print(text)
f.close()

answer = ""

for file in os.listdir("."):
    with open(file, "r", encoding="utf8") as f:
        text = f.read()
        sea = re.search('(?<=answer=\").*?(?=\")', text)
        if sea:
            answer = sea.group()
            break

print(answer)
