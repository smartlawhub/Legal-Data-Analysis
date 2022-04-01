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
