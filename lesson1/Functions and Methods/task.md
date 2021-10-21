## Functions


<b>1.</b> Now, coming back to functions, they are what allows you to do operations over data and variables in Python 
(more info <a href='https://www.w3schools.com/python/python_functions.asp'>here</a>). For this, you need to pass it the expected arguments. Here is what a function looks like, and how you create it:

```python
def my_function(var1, var2):
    return var1 + var2
my_function(1,2)
```
<b>2.</b> The above is a very simple function returning a sum, and while you'd get the same result merely by doing the sum immediately (without passing it to a function), it's sometimes useful to write down things formally in this fashion.

Functions can be much more complicated. Notably, while you need to pass all expected arguments (also called parameters), you can also specify "bonus" arguments that are not necessarily required.

<b>3.</b> You can create, and you will create your own functions. However, Python has already plenty of built-in functions, so that you don't have to invent the wheel everytime you need to do something.


<b>4.</b> In addition, Python is a shared resources, and for most uses someone has already created a function for you, such that you just need to import it. This is the system of packages and librairies that power Python. 

You can either import a full package (such as `numpy` here), or dedicated functions or "modules" in a package. The difference is in terms of performance (some packages are heavy). You then call the functions in accordance with their name as imported, a name that you can set yourself (some are conventional: `pandas` is nearly always `pd`)

<b>5.</b> The first package here is specialised in numbers and mathematical operations; it typically goes further than the basic Python functions. For instance, if you want to compute a mean.

<b>6.</b> Frequently, the data and variables you will manipulate have functions (called "methods") already attached to them.
(We won't discuss it, but it's related to `classes` in Python, which you can learn more about <a href='https://docs.python.org/3/tutorial/classes.html'>here</a>). 

We saw it earlier when we used `append` to add an item to a list. The equivalent method for sets is `add`.

Strings have a function `split` that can be used to obtain a list of items in that string depending on a splitting criterion. 

<b>7.</b> Sets have a number a functions attached to them as well, allowing for comparisons between sets: 
<ul><li>`difference` will return the difference between set1 and 2</li>
    <li>`intersection`, for items that are in both sets</li>
    <li>`union` returns a set with both sets' content</li>
    <li>`symmetric_difference` returns the items that are only in one set</li>
    </ul>

<b>8.</b> <u>Exercise 2</u> Using the methods you just learned, find the number of words that are common to both the 
first and third verse of the poem. 
