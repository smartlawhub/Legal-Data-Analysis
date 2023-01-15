# Functions and Methods

Now, coming back to functions, they are what allows you to do operations over data and variables in Python 
(more info <a href='https://www.w3schools.com/python/python_functions.asp'>here</a>). For this, you need to pass it 
the expected arguments. 

The first few lines of code in the .py file show you what a function looks like, and how you 
create it. You declare it with the specific term `def`, then give it a name, and specify expected arguments within 
brackets.  

Then, and <u>this is crucial</u>, you input a new line, and a tab - the inside of your function should 
<b>not</b> be on the same line as the declaration, everything should be shifted by one tab. (This is a type of 
syntax we'll see again and again.)

The example given is a very simple function returning a sum, and while you'd get 
the same result merely by doing  the sum immediately (without passing it to a function), it's sometimes useful to 
write down things formally in this fashion.


```python
def my_function(alpha, beta):  # An example of a function that just returns the sum of the two arguments you pass to it 
    # (which will be known as beta and alpha in the sole context of the function)
    return beta + alpha

print(my_function(1, 2))  # We call the function with brackets to include the expected arguments
print(my_function("E", "H")) # Notice that the order of the arguments is important
```

    3
    HE


If you are not sure what a function does, you can always type  `help(function)`, and the console shall return an answer.


```python
help(print)
```

    Help on built-in function print in module builtins:
    
    print(...)
        print(value, ..., sep=' ', end='\n', file=sys.stdout, flush=False)
        
        Prints the values to a stream, or to sys.stdout by default.
        Optional keyword arguments:
        file:  a file-like object (stream); defaults to the current sys.stdout.
        sep:   string inserted between values, default a space.
        end:   string appended after the last value, default a newline.
        flush: whether to forcibly flush the stream.
    


You can create, and you will create your own functions. However, Python has already plenty of built-in 
functions, so that you don't have to invent the wheel everytime you need to do something. As you already saw, you 
don't need a function to calculate the sum of two variables, so `my_function` is redundant.

Other important functions are those that allow you to play with the types of variables. For instance, `str` 
transform your variable into a string, `int` into a number, `list` into a list, etc. The function `set` takes a list and returns a set. Check also the function `range`, that allows you to iterate over a definite number of numbers.


```python
print(len("How long is this sentence ?"))
print(list("this will be turned into a list of letters"))
print(round(2.3))
print(set([1, 1, 1, 3]))

for x in range(0, 20, 5):  # Range takes your first number, the upper limit (not included), and (if needed) the steps to get there
    print("This is number " + str(x))
```

    27
    ['t', 'h', 'i', 's', ' ', 'w', 'i', 'l', 'l', ' ', 'b', 'e', ' ', 't', 'u', 'r', 'n', 'e', 'd', ' ', 'i', 'n', 't', 'o', ' ', 'a', ' ', 'l', 'i', 's', 't', ' ', 'o', 'f', ' ', 'l', 'e', 't', 't', 'e', 'r', 's']
    2
    {1, 3}
    This is number 0
    This is number 5
    This is number 10
    This is number 15


Python is a shared resources, and for most uses someone has already created a function for you, such that 
you just need to import it. This is the system of packages and librairies that power Python. 

When you find a package or module that intests you, you should first install it (from the internet) in your local 
Python environment. The way to do this is with the command `pip install X`, with X being the name of your package ; 
you type this command in the Terminal (not the Console), unless you have downloaded the iPython package (which 
boosts the console and allows direct installations). Once a package it's installed, you don't have to do it again.

However, in order to use that package, you need to import it every time you restart the console. Every script 
file starts with "import statements" which indicates which packages you will be using in the context of this 
script. You need the keyword <code>import</code>, and you can give aliases to the modules with the keyword <code>as</code>.

If you get an error when trying to import a package, usually it's because you have not installed it (with 
"pip install" as described above).

You can either import a full package (such as `numpy` here), or dedicated functions or "modules" in a package (using 
the "from X import Y" syntax. The difference is in terms of performance (some packages are heavy). You then call the functions in accordance with 
their name as imported, a name that you can set yourself (some are conventional: `pandas` is nearly always `pd`, 
`numpy` is  `np`, etc.)


```python
import numpy as np  # We import numpy, but it's typically aliased 'np'
from collections import Counter  # we can also import only a selected functions from a package
import pandas as pd


```




    7.75



The first package here, `numpy`  is specialised in numbers and mathematical operations; it typically goes 
further than the basic Python functions. For instance, if you want to compute a mean: you could just use `sum` and 
divide by `len`; but it's easier to just use `np.mean()` on a list of numbers. 

The syntax is always the same: you go from a module to a function by adding a period (`.`), and then add the required 
parameters to your function. If you don't know what is the required parameters, you can usually use CTRL+P to learn 
more about the inside of a function.


```python
np.mean([1, 5, 10, 15])  # Instead of creating a function to calculate a mean, we can just leverage the existing package numpy
```

All of the data and variables you will manipulate in this course will have built-in functions (called 
"methods") already attached to them. They also have what's called attributes, which are data points. Methods take an 
argument (within brackets), 
while attributes have no brackets (and only output the data point). 
(We won't learn it, but it's related to `classes` in Python, about which you can learn more <a href='https://docs.python.org/3/tutorial/classes.html'>here</a>). 

We saw it earlier when we used `append` to add an item to a list. The equivalent method for sets is `add`.

We will be working on legal data, which means, for a large part, text data. Fortunately, strings are quite easy to 
work with, as they have built-in functions in Python. For instance, the function `split` can be used to obtain a 
list of items in that string depending on a splitting criterion. The opposite of that function would be `join`, 
whereby you join items in a list with a common character.

These two functions are also a good example of how Python works between different data types: lists become strings, and the reverse.


```python
splitted_words = "A freckled and frivolous cake there was".split(" ")  # The variable splitted_verse will take the result of the right-hand side expression, which splits a string according to a criterion
splitted_cake = "A freckled and frivolous cake there was".split("cake")

print(splitted_words)
print(splitted_cake)

print("  ".join(splitted_words))
```

    ['A', 'freckled', 'and', 'frivolous', 'cake', 'there', 'was']
    ['A freckled and frivolous ', ' there was']
    A  freckled  and  frivolous  cake  there  was


Sets have a number a functions attached to them as well, allowing for comparisons between sets: 
<ul><li><code>difference</code> will return the difference between set1 and 2;</li>
    <li><code>intersection</code>, for items that are in both sets;</li>
    <li><code>union</code> returns a set with both sets' content; and</li>
    <li><code>symmetric_difference</code> returns the items that are only in one set</li>
    </ul>


```python
set1 = {1,2,3,4}
set2 = {3,4,5,6}
print(set1.difference(set2))
print(set1.intersection(set2))
print(set1.union(set2))
print(set1.symmetric_difference(set2))
```

    {1, 2}
    {3, 4}
    {1, 2, 3, 4, 5, 6}
    {1, 2, 5, 6}

