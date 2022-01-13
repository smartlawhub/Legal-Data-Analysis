# Lists

<b>1.</b> Another type of variable is a <em>list</em>, which is exactly what you think it is: it lists things, such 
as data, or even other variables, or even other lists ! Lists are denoted by using brackets and commas. You update a 
list by using the function `.append()` directly from the list, as follows: see that the item you added with append 
now appears at the end of the list.

<b>2.</b> A very important feature of lists is that they are ordered. This means if you know the (numerical) index of 
an item in a list, you can access it immediately.

Learn it once and for all: indexes start at 0; the first element in a list can be found at index 0. This will lead 
you to such difficulties if you do not get that 0, not 1, marks the beginning of a list. For instance, the length of 
a list starts at 1, by definition, but there is a logic here, as we'll see with ranges.

You can also select an element of a list by reference to its relative position. Finally, if you can select the item in a list of list by collating indexes.

<b>3.</b> You can also select several elements in a list, by using the `:` operator. The operator is not inclusive of the outer limit, meaning that the item on the right-hand-side of the  `:` operator won't be included in the list that is rendered. For instance, if you look for indexes `[0:2]`, you'll get items at index 0 and index 1, but not 2 (because it's excluded).

You can leave the selection open-ended, according to the same principles: the right-hand-side index won't be included, but the left-hand-side one is.

<b>4.</b> Another data type is what's called a boolean. It is simply a statement True or False, but it is often very 
useful when you have to check conditions. It's based on the logic invented by George Boole in the mid-1800s, which 
is basically what powers computers now (see <a href="https://computer.howstuffworks.com/boolean.htm">here</a>)

<b>5.</b> Finally, there are two other types of data worth knowing at this stage: `sets` and `dictionaries`. 

Sets are like lists (they can take any sort of variable, but not a list), except they are unordered, and they can't have duplicates. They are very useful to check if two sets of data overlap, or what they have or don't have in common. Since they are not ordered, you cannot select an element from a set. If you create a set with a duplicate element, it will ignore it and returns a set without the duplicate.

<b>6.</b> A Dictionary is a type of data that links a `key` to a `value`. The key becomes the index of your dictionary; if you give a key to the dictionary, it will return the value. It is useful to track down relations between different data points. Here as well, you can use any type of data you want. You use brackets, and indicate the relationship with a ":" operator.

<u>Exercice 1</u> Before switching to the next section, complete the placeholder such that you can print "Mervyn 
Peake" using both the list `my_list` and the dictionary `my_dict`.

<div class="hint">Check out the previous code to identify the correct index and key; don't forget the middle space !
</div>
