import regex as re

# 1

my_list = []
for x in range(1,25,1):
    my_list.append(x)

even_list = []
for x in my_list:
    if x % 2 == 0:  # The modulo operator, using the percent symbol, returns the remainder of a division.
        even_list.append(x)

print(even_list)


# 2

new_my_list = [x for x in range(1,25,1)]

new_even_list = [x for x in new_my_list if x % 2 == 0]

even_more_new_list = ["Number : " + str(x * 3) for x in new_my_list if x % 2 == 0]

# Exercise 8

with open("poem.txt", "r") as f:
    poem = f.read()

longest_line = ""
for line in re.split(r"\n", poem):
    if re.search("ake", line) and re.search("[A-Z]", re.sub(r"^[\d \.]+", "", line[6:])) is None:
        len_line = len(re.findall(r"\w+", line[3:]))
        if len_line in [3, 5, 7] and len_line > len(re.findall(r"\w+", longest_line[3:])):
            longest_line = line
print(longest_line[:3])

print(sorted([line for line in re.split(r"\n", poem)[1:] if re.search("ake", line) and re.search("[A-Z]", re.sub(r"^[\d \.]+", "", line[6:])) is None and len(re.findall(r"\w+", line.strip()[3:])) in [3,5,7]], key=len, reverse=True)[0][:3])
