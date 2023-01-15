# List Comprehension

Python code is a good middle ground between very verbose code (VBA for instance), and languages that are 
perfectly opaque to the neophyte. When you look at the syntax, given a few basics, you can have a rough idea of 
what's happening.

The issue with verbosity, however, is that it take space and time. If you need to populate a list from another list 
given a condition, you have now learned that you can use a loop and a conditional statement to perform the operation.
But again, it can be cumbersome to write down all of this.

Enter list comprehensions, which is a way to create a list in a single line. The syntax is of the kind:
`[x for x in list]`

So, what you are trying to do is to invoke every element in the list, and operate over it to create a new list 
(hence the brackets around the statement).

Take for instance these three lines, which add numbers to a list after doubling then.


```python
my_list = []
for x in range(1,25):
    my_list.append(x * 3)
print(my_list)
```

    [3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36, 39, 42, 45, 48, 51, 54, 57, 60, 63, 66, 69, 72]


This can be rewritten as a list comprehension in line with the syntax above


```python
new_list = [x * 3 for x in range(1,25)]
print(new_list)
```

    [3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36, 39, 42, 45, 48, 51, 54, 57, 60, 63, 66, 69, 72]


Note that the power of this method comes from the fact that you can go much further than the bare statement I gave 
you here. in particular,  you can add conditions. For instance, let's say we are looking for every even number in a list of numbers.


```python
even_list = []
for x in my_list:
    if x % 2 == 0:  # The modulo operator, using the percent symbol, returns the remainder of a division. Every even number's 
        # remainder is always 0
        even_list.append(x)

print(even_list)
```

    [6, 12, 18, 24, 30, 36, 42, 48, 54, 60, 66, 72]


And this is the same list created with a list comprehension.


```python
new_even_list = [x for x in new_list if x % 2 == 0]
print(new_even_list)
```

    [6, 12, 18, 24, 30, 36, 42, 48, 54, 60, 66, 72]


Note that you can add conditions, and the usual `and`, `or`, and `None` commands or booleans work in this context as 
well.

Finally, the first item in the list can also be operated upon. Let's say we now want the even numbers from `my_list`,
except times three and in a string that starts with "Number: ".


```python
even_more_new_list = ["Number : " + str(x * 3) for x in new_list if x % 2 == 0]
print(even_more_new_list)
```

    ['Number : 18', 'Number : 36', 'Number : 54', 'Number : 72', 'Number : 90', 'Number : 108', 'Number : 126', 'Number : 144', 'Number : 162', 'Number : 180', 'Number : 198', 'Number : 216']

