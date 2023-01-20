# Syntax

Finally, some notions of syntaxes. You write code as you would write anything: sequentially. This means 
you first define your variables or your functions before using it, or Python won't be able to know what you mean. 
This being said, there are two basic syntaxic ideas that are crucial to any coding script - or indeed, to any software you are currently using. These are loops, and conditions.

## Loops

A `loop`,  tells Python to go over (the term is "iterate") a number of elements, most often from a list. 
The syntax is always the same: `for x in list: y`, where "x" represents the temporary name of element in the "list" in 
turn, and "y" what happens to that "x". In other words, start with the first element (called "x" in the context of 
the loop), do stuff ("y") with that element, then go over the 
next element (which will also be called "x"), and so on. 


```python
words = ["A", "Freckled", "and", "Frivolous", "Cake", "There", "Was"]

for x in words:  # This loop will print each word from the list one by one
    print(x)
```

    A
    Freckled
    and
    Frivolous
    Cake
    There
    Was


After the loop has been completed, the variable `x` is still available: it represents whatever was the last item iterated over.


```python
print(x)
```

    Was


You will note that for your loop to work, the second level of instructions needs to be shifted to the right (and you 
have a colon at the end of your `for` statement). That's 
called identation, and this is crucial in Python. It's also one of the main reasons why people don't like this 
language. Other languages are more explicit as to when a section of your code is actually contained in another 
section: for example, in C++ you would put stuff within brackets, or indicate the end of a statement with a semi-colon.

You can loop over lists, strings, and other objects we will discover later.


```python
recreated_text = ""  # We start by creating an empty text variable
for letter in "Swordfish":   # We loop over the string Swordfish (strings can be used as lists of letters)
    print(letter)  # We first print the letters, one by one
    recreated_text += letter  # Then we add the letter to the existing recreated text; remember that x += 1 increment x by 1
    print(recreated_text)
```

    S
    S
    w
    Sw
    o
    Swo
    r
    Swor
    d
    Sword
    f
    Swordf
    i
    Swordfi
    s
    Swordfis
    h
    Swordfish


As everywhere else in Python, the order of things is very important, including in the context of a loop.


```python
for x in words: # We loop over the words
    y = x  # We assign a new variable y that's the same as every x, one by one
    print(x + " - " + y)
    
for x in words: # In this second loop, y has not been assigned yet, so it is still the last-assigned y
    print(x + " - " + y)
    y = x
```

    A - A
    Freckled - Freckled
    and - and
    Frivolous - Frivolous
    Cake - Cake
    There - There
    Was - Was
    A - Was
    Freckled - A
    and - Freckled
    Frivolous - and
    Cake - Frivolous
    There - Cake
    Was - There


A key thing to understand about loops, and why they are so powerful and important in data science, is that loops 
allow you to be agnostic about the data you are working on. In other words, you can operate over tons of data 
without knowing (or needing to know) what is exactly is that data, since the loop does it for you when you 
define the name of each data point one by one. 

To give you an example, if you loop through the content of a file, you can operate over each file, one by one, even 
if you have no idea how many files they are or what are the file names: in <code>for x in my_filelist:</code>, each 
file will be named <code>x</code> for the purpose of what you want to do with that file (e.g., load it or rename it),
even if the real file name is not x. This is the power of a loop.

## Conditions

The second important syntax element, and really the basic building block of so much code that runs your 
daily life, is the `if/else` statement. It simply asks if a condition is met, and then accomplish the resulting code.
The syntax is of the form `if x:` , where "x" need to be <code>True</code> (in the boolean sense) for the (indented) code coming after the colon to output. 2 + 2 = 4, so a statement `if 2+2 == 4: print("Correct")` would print correct. (Note that 
we use "==" to check an identity, since the single "=" sign is used to assign variables.)

In the example below, we will check that the letter "e" (i.e., a string corresponding to the lower case "e") is present in a list of words.

Note that the `else` will compute only if the `if` condition has not been met. 


```python
for word in words:
    if "e" in word:
        print(word)
    else:
        print(word, " : No 'e' in that word")
```

    A  : No 'e' in that word
    Freckled
    and  : No 'e' in that word
    Frivolous  : No 'e' in that word
    Cake
    There
    Was  : No 'e' in that word


They are several ways to syntax `if` statements:
<ul><li>With an <code>is in</code> if need to check that an item is part of a list or a set (or the inverse 
<code>is not in</code>);</li>
    <li>By itself if you are checking a boolean (<code>if my_bol:</code> will return <code>True</code> or 
<code>False</code> depending on the value of <code>my_bol</code>);</li>
    <li>With the double equal sign <code>==</code> for identity between two variables, or <code>!=</code> for lack of 
identity; and</li>
    <li>With a combination of the signs <code>></code>, <code><</code> and <code>=</code> when comparing two 
quantities.</li></ul>

Finally, you can add conditions with the keywords `and` and `or`. 

In case you want to try a second condition after a first one is not met, you can use the keyword `elif` ("else if"), which works exactly like if.


```python
sentence = " ".join(words)  # We recreate the sentence from the list of words with the method join
print(sentence)
my_bol = False  # We set a boolean that's False

if "frivolous" in sentence:
    print("First Condition Met")
elif my_bol:
    print("Second Condition Met")
elif len(sentence) == 50:   # len() is a built-in function rendering the length of a list or string
    print("Third Condition Met")
elif len(sentence) >= 30 and "e" in sentence or "Cake" in sentence:
    print("Fourth Condition Met")
else:
    pass
```

    A Freckled and Frivolous Cake There Was
    Fourth Condition Met


This is all, or nearly. On the basis of these very basic concepts run most of the rest of the Python scripts you can see out there. 
