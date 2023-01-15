# Lists

Another type of variable is a list, which is exactly what you think it is: it lists things, such as data, or even other variables, or even other lists ! Lists are denoted by using brackets and commas. You update a list by using the function .append() directly from the list, as follows: see that the item you added with append now appears at the end of the list.


```python
beta = "Cake"
my_list = ["Frivolous", 42, beta, ["This is a second list, with a number: ", 142], "Peake"]
print(my_list)
my_list.append("Swordfish")
print(my_list)
```

    ['Frivolous', 42, 'Cake', ['This is a second list, with a number: ', 142], 'Peake']
    ['Frivolous', 42, 'Cake', ['This is a second list, with a number: ', 142], 'Peake', 'Swordfish']


A very important feature of lists is that they are ordered. This means if you know the (numerical) index of an item in a list, you can access it immediately. This is called "indexing".
Learn it once and for all: <b>in Python, indexes start at 0</b>; the first element in a list can be found at index 0. This is not intuitive, but you need to get used to it: 0, not 1, marks the beginning of a list.


```python
print(my_list[0])
print(my_list[1])
print(my_list[3])
```

    Frivolous
    42
    ['This is a second list, with a number: ', 142]


Note that the last indexing returns the second list that was in my_list. As such, it can also itself be indexed.


```python
print(my_list[3][1])
```

    142


Indexing also works using the relative position of an item in a list: [-1] gives you the last item, [-2] the penultimate, etc.


```python
print(my_list[-2])   # Will return 'Peake', the penultimate term since we added 'Swordfish' as last term
```

    Peake


More importantly, you can select what's called a range by using the <code>:</code> operator. The operator is not inclusive of the outer limit, meaning that the item on the right-hand-side of the  <code>:</code> operator won't be included in the list that is rendered. For instance, if you look for indexes  <code>[0:2]</code>, you'll get items at index 0 and index 1, but not 2 (because it's excluded).


```python
print(my_list[0:2])
```

    ['Frivolous', 42]


You can leave the selection open-ended, according to the same principles: the right-hand-side index won't be included, but the left-hand-side one is. So <code>[:5]</code> means "any element until the 6th (not included)", while <code>[2:]</code> means "every element after the third element (included)".


```python
print(my_list[:2])
print(my_list[2:])
print(my_list[-2:])
print(my_list[0::3]) # This last type of range gives you every 3 items starting from 0 
```

    ['Frivolous', 42]
    ['Cake', ['This is a second list, with a number: ', 142], 'Peake', 'Swordfish']
    ['Peake', 'Swordfish']
    ['Frivolous', ['This is a second list, with a number: ', 142]]


Another data type is what's called a boolean. It is simply a statement True or False, but it is often very useful when you have to check conditions. It's based on the logic invented by George Boole in the mid-1800s, which is basically what powers computers now (see <a href="https://computer.howstuffworks.com/boolean.htm">here</a>).


```python
var_bol = True
var_bol2 = False
print(bool(var_bol))
print(bool(var_bol2))
```

    True
    False


Boolean logic works by manipulating <code>True</code> and <code>False</code> statements. In Python, you often need to check if something is <code>True</code> or not, for instance in the context of conditions (next module). The most basic way to do this is with the <code>==</code> (double equal - not to be confused with single equal, which is used to assign a variable. Its opposite is <code>!=</code>.


```python
gamma = 5
print(gamma == 5) # Since gamma is indeed 5, this prints True
print(gamma != 5) # Since gamma is not different from 5, this prints False
```

    True
    False


Finally, there are two other types of data worth knowing at this stage: `sets` and `dictionaries`. 

Sets are like lists (they can take any sort of variable, but not a list), except they are unordered, and they can't have duplicates. They are very useful to check if two sets of data overlap, or what they have or don't have in common. Since they are not ordered, you cannot select an element from a set. If you create a set with a duplicate element, it will ignore it and returns a set without the duplicate.


```python
my_set = {1, 2, 2, 3, 3, 4, "Cake", "Cake"}
print(my_set)
```

    {1, 2, 3, 4, 'Cake'}


A Dictionary is a type of data that links a `key` to a `value`. The key becomes the index of your dictionary; if you give a key to the dictionary, it will return the value. It is useful to track down relations between different data points. Here as well, you can use any type of data you want. You use brackets, and indicate the relationship with a ":" operator.


```python
my_dict = {42: "Mervyn", "Peake": 2, "My List" : my_list}
print(my_dict[42])
print(my_dict["My List"])
```

    Mervyn
    ['Frivolous', 42, 'Cake', ['This is a second list, with a number: ', 142], 'Peake', 'Swordfish']


Before switching to the next section, find a way to print "Mervyn Peake" indexing both the list 
`my_list` and the dictionary `my_dict`. Don't forget the middle space !
