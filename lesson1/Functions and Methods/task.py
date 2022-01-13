# 1

def my_function(alpha, beta):
    return beta + alpha


my_function(1, 2)

# 2


def my_function(var1, var2, *var3):
    if var3:  # That is, if anything was passed as var3
        return var1 + var2
    else:
        return var2 - var1


print(my_function(1, 2))
print(my_function(1, 2, True))


# 3

print(len("How long is this sentence ?"))
print(list("this will be turned into a list of elements"))
print(round(2.3))

for x in range(0, 20, 5):  # Range takes your first number, the upper limit (not included), and (if needed) the steps to get there
    print("This is number " + str(x))

# 4 - Notice that, as long as you don't use the imported functions, they appear as grey in PyCharm

import numpy
from collections import Counter, defaultdict
import pandas as pd

# 5

numpy.mean([1, 5, 10, 15])

# 6

splitted_verse = "A freckled and frivolous cake".split(" ")
"  ".join(splitted_verse)

# 7

set1 = {1,2,3,4}
set2 = {3,4,5,6}
print(set1.difference(set2))
print(set1.intersection(set2))
print(set1.union(set2))
print(set1.symmetric_difference(set2))

# 8

fifth_para = "Around the shores of the Elegant Isles \nWhere the cat-fish bask and purr \nAnd lick their paws with adhesive smiles \nAnd wriggle their fins of fur, \nThey fly and fly ‘neath the lilac sky - \nThe frivolous cake, and the knife \nWho winketh his glamorous indigo eye \nIn the wake of his future wife."
sixth_para = "The crumbs blow free down the pointless sea \nTo the beat of a cakey heart \nAnd the sensitive steel of the knife can feel \nThat love is a race apart \nIn the speed of the lingering light are blown \nThe crumbs to the hake above, \nAnd the tropical air vibrates to the drone \nOf a cake in the throes of love."

answer = 0   # set answer to correct value after writing relevant code

list_fifth_para = fifth_para.split(" ")
list_sixth_para = sixth_para.split(" ")

intersect = set(list_fifth_para).intersection(set(list_sixth_para))
answer = len(intersect)
