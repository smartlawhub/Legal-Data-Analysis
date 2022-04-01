# 1

def my_function(alpha, beta):  # An example of a function that just returns the sum of the two arguments you pass to it (which will be known as beta and alpha in the sole context of the function)
    return beta + alpha


print(my_function(1, 2))  # We call the function with brackets to include the expected arguments


# 2

print(len("How long is this sentence ?"))
print(list("this will be turned into a list of elements"))
print(round(2.3))

for x in range(0, 20, 5):  # Range takes your first number, the upper limit (not included), and (if needed) the steps to get there
    print("This is number " + str(x))


# 3- Notice that, as long as you don't use the imported functions, they appear as grey in PyCharm

import numpy
from collections import Counter
import pandas as pd

# 4

numpy.mean([1, 5, 10, 15])

# 5

splitted_verse = "A freckled and frivolous cake".split(" ")

print("  ".join(splitted_verse))

# 6

set1 = {1,2,3,4}
set2 = {3,4,5,6}
print(set1.difference(set2))
print(set1.intersection(set2))
print(set1.union(set2))
print(set1.symmetric_difference(set2))

# 7

fifth_para = "Around the shores of the Elegant Isles \nWhere the cat-fish bask and purr \nAnd lick their paws with adhesive smiles \nAnd wriggle their fins of fur, \nThey fly and fly ‘neath the lilac sky - \nThe frivolous cake, and the knife \nWho winketh his glamorous indigo eye \nIn the wake of his future wife."
sixth_para = "The crumbs blow free down the pointless sea \nTo the beat of a cakey heart \nAnd the sensitive steel of the knife can feel \nThat love is a race apart \nIn the speed of the lingering light are blown \nThe crumbs to the hake above, \nAnd the tropical air vibrates to the drone \nOf a cake in the throes of love."
