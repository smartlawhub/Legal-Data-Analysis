# Functions


<b>1.</b> Now, coming back to functions, they are what allows you to do operations over data and variables in Python 
(more info <a href='https://www.w3schools.com/python/python_functions.asp'>here</a>). For this, you need to pass it the expected arguments. Here is what a function looks like, and how you create it:

<b>2.</b> The above is a very simple function returning a sum, and while you'd get the same result merely by doing the sum immediately (without passing it to a function), it's sometimes useful to write down things formally in this fashion.

If you are not sure what a function does, you can always type  `help(function)`, and the console shall return an answer.

Functions can be much more complicated. Notably, while you need to pass all expected arguments (also called parameters), you can also specify "bonus" arguments that are not necessarily required.

<b>3.</b> You can create, and you will create your own functions. However, Python has already plenty of built-in 
functions, so that you don't have to invent the wheel everytime you need to do something. As you already saw, you 
don't need a function to calculate the sum of two variables, so `my_function` is redundant.

Other important functions are those that allow you to play with the types of variables. For instance, `str` 
transform your variable into a string, `int` into a number, `list` into a list, etc. Check also the function range, 
that allows you to iterate over a definite number of numbers.

<b>4.</b> In addition, Python is a shared resources, and for most uses someone has already created a function for you, such that you just need to import it. This is the system of packages and librairies that power Python. 

You can either import a full package (such as `numpy` here), or dedicated functions or "modules" in a package. The 
difference is in terms of performance (some packages are heavy). You then call the functions in accordance with 
their name as imported, a name that you can set yourself (some are conventional: `pandas` is nearly always `pd`, 
`numpy` is  `np`, etc.)

<b>5.</b> The first package here, `numpy`  is specialised in numbers and mathematical operations; it typically goes 
further than the basic Python functions. For instance, if you want to compute a mean: you could just use `sum` and 
divide by `len`; but it's easier to just use `np.mean()` on a list of numbers. 

The syntax is always the same: you go from a module to a function by adding a period, and then add the required 
parameters to your function. If you don't know what is the required parameters, you can usually use CTRL+P to learn 
more about the inside of a function.

<b>6.</b> Frequently, the data and variables you will manipulate have functions (called "methods") already attached to them.
(We won't discuss it, but it's related to `classes` in Python, about which you can learn more <a href='https://docs.python.org/3/tutorial/classes.html'>here</a>). 

We saw it earlier when we used `append` to add an item to a list. The equivalent method for sets is `add`.

We will be working on legal data, which means, for a large part, text data. Fortunately, strings are quite easy to 
work with, as they have built-in functions in Python. For instance, the function `split` can be used to obtain a 
list of items in that string depending on a splitting criterion. The opposite of that function would be `join`, 
whereby you join items in a list with a common character.

These two functions are also a good example of how Python works between different data types: lists become strings, 
and the reverse. (Actually, evey string can be thought of as a list of single characters, and you can index it.)

<b>7.</b> Sets have a number a functions attached to them as well, allowing for comparisons between sets: 
<ul><li><code>difference</code> will return the difference between set1 and 2;</li>
    <li><code>intersection</code>, for items that are in both sets;</li>
    <li><code>union</code> returns a set with both sets' content; and</li>
    <li><code>symmetric_difference</code> returns the items that are only in one set</li>
    </ul>

<b>8.</b> <u>Exercise 2</u> Using the methods you just learned, find the number of words that are common to both the 
fifth and sixth paragraphs of the poem, which I have put in variables.
