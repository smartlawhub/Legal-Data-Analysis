<h1>1. Introduction to Python</h1>

<p>This is the first lesson in the context of Course HEC <i>Law Project Legal Data Analytics</i></p>

<p><i>*** First a bit of Semantics: Code, Console, Comments, Etc., Console shortcuts as well .***</i></p>

<b>1. </b>Computer code, at its most basic, calculates stuff. You can think of this course and everything that 
follows as expanding the uses of a calculator. For instance:

Typically, in Python you'd use the command `print` to have stuff appear on your screen. It is also more precise, as 
it gives your computer the exact command to process. 

For instance, if you add a line of computations above and try to run everything in the Console, it will only render 
the last line - but if you insert two `print` statement, one after the other, both will render.
`print` is a <em>command</em>. Like most commands, it requires some <em>parameters</em>, that are indicated within brackets. Eg.  

<b>2. </b>We will come back to functions a bit later. Before that, we need to discuss <em>variables</em>, which you can 
think of as recipients in which you store information.

Variables are typically written in lower caps; the way  you assign data to a variable is with a `=` sign, as follows.
You can then use variables directly in functions (such as print), or do operations between them.
What do you think will print if we press Enter ?

You can assign and re-assign variables at will: you can even assign a variable to another variable. Variables that 
contain numbers can also be added or subtracted to with a specific syntax:

```python
gamma = gamma + alpha
print(gamma)
gamma += 1 
print(gamma)
gamma -= 2
print(gamma)
```

There are different types of numbers in Python. Now, variables need not be numbers. They can also be text, which in Python is known as a `string`. Likewise, you can make operations with them, such as collating two strings.

```python
alpha = "Hello World"
beta = "Hello Cake"
print(alpha + beta)
```
Do note that the print command does exactly what you ask it to do: it did not insert a space between the two strings here, it's for you to think of this kind of details.

In what follows, we'll use text and strings taken from Mervyn Peake's poem <a href ="https://gormenghasts.tumblr.com/post/80656474535/the-frivolous-cake-a-freckled-and-frivolous-cake"><i>The Frivolous Cake</i></a>. I have numeroted every verse; we'll store it in a variable for now and come back to it later.
