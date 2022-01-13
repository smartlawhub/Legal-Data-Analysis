import os
import regex as re

# 1

f = open("../../poem.txt", encoding="latin1")
poem = f.read()
print(poem)
f.close()

with open("poem2.txt", "a", encoding="utf8") as f:
    f.write(poem)

f = open("poem2.txt")
text = f.read()
print(text)
f.close()

# 2

import csv

with open("first_csv.csv", "w") as csv_file:
    writer = csv.writer(csv_file, delimiter=",")

    writer.writerow(["Cake", "Beautiful", "Sensitive"])
    writer.writerow(["Knife", "Gliterring", "Murderous"])


# Exercise

answer = ""

os.chdir("./Gibberish")

for file in os.listdir("."):
    with open(file, "r", encoding="utf8") as f:
        text = f.read()
        sea = re.search('(?<=answer=\").*?(?=\")', text)
        if sea:
            answer = file
            break
