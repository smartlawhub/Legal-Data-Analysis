<h1>1. Introduction to Python</h1>

<p>This is the first lesson in the context of the <i>Legal Data Analytics</i> course.</p>

First a bit of Semantics:

<ul><li><b>The Code</b> is what you'll be writing as input in the Console. The .py files found in the Script folder 
contain some code snippets ready to be deployed in the Console, but you'll also be writing your own code and store 
it in these files for later use.
</li>
    <li><b>The Console</b> is the environment where you'll be inputting code to generate outputs. As long as you 
do not restart the console, your variables and data will remain active, in memory; but all this disappears whenever 
you shut 
down PyCharm, so you'll need to make sure to store and save your data.</li>
    <li><b>Comments</b> are greyed out bits of non-code, natural language, to describe and explain the code. 
Comment start with the hashtag <code>#</code>.    
<li><b>Errors</b> are what happens when you try to execute invalid code. The most frequent types of 
errors are:<ol><i>Syntax Error</i>, when you just made a mistake in the syntax, which is paramount in Python; and</ol>
<ol><i>Type Error</i>, when you are trying to work with two incompatible types of data.</ol></li>
    <li><b>Pycharm</b> is an IDE, or Integrated Development Environment. It's just an easier way to code, as 
all your files are there together with the console. You code is also automatically colored according to the nature 
of the different objects and variables types you are using. Amongst the main shortcuts, you should know:
<ol><i>Up Arrow</i>, when in the console, input the previous inputs in ante-chronological order;</ol>
<ol><i>The Tab key</i> autofills your code, or offers a menu of option to choose from; and</ol>
<ol><i>Alt+Shift+E</i> (on Windows - may be different on Macs), automatically input and execute a line of code 
highlighted from a .py script.
</ol></li></ul>

<b>1. </b>Computer code, at its most basic, calculates stuff. You can think of this course and everything that 
follows as expanding the uses of a calculator. For instance, if you input 2+2 in the Console, press "Enter", output will be 4.

Typically, in Python you'd use the command `print` to have stuff appear on your screen. It is also more precise, as 
it gives your computer the exact command to process: if you type two lines of computation before pressing enter, 
only the last will render; however, both will render an output if you specify that both need to be printed.


```python
2+2
3+3
```




    6



`print` is a <em>command</em>. Like most commands (or functions), it requires some <em>arguments</em>, that are 
indicated 
within 
brackets - as here 2+2.


```python
print(2+2)
print(2*3)
```

    4
    6


<b>2. </b>We will come back to functions a bit later. Before that, we need to discuss <em>variables</em>, which you can think of as recipients in which you store information.

Variables are typically written in lower caps; the way  you create/assign data to a variable is with a `=` sign, according 
to the syntax `variable = value`.
You can then use variables directly in functions (such as print), or do operations between them.

You can assign and re-assign variables at will: you can even assign a variable to 
another variable. 


```python
alpha = 1
beta = 2
gamma = 2 * 3
print(alpha + beta + gamma)
```

    9


Variables that contain numbers can also be added or subtracted to with a specific syntax: `var += 2` means that 2 
will be added to my variable, and this every time you input this particular command. Think of it as an update of the 
original 
variable.


```python
gamma = gamma + alpha
print(gamma)
gamma += 1
print(gamma)
gamma -= 2
print(gamma)
```

    7
    8
    6


<b>3. </b>Variables need not be numbers. They can also be text, which in Python is known as a `string`. Likewise, you can make operations with them, such as collating two strings.

Do note that the print command does exactly what you ask it to do: it did not insert a space between the two strings 
here, it's for you to think of this kind of details. Programming is deterministic: output follows input with, most 
of the time, no role for randomness. On the plus side, this means you should be assured that you'll get an output if 
we type proper input; on the minus side, this therefore requires utmost precision on your part. 


```python
alpha = "Hello World"
beta = "Hello Cake"
print(alpha + beta)
```

Also important to keep into account is that strings are different from number. And you cannot, for instance, add 
strings to number: this would throw a TypeError.


```python
print(alpha + gamma)  # gamma has been defined above and is still known to the console's environment
```

In what follows, we'll use text and strings taken from Mervyn Peake's poem <a href ="https://gormenghasts.tumblr.com/post/80656474535/the-frivolous-cake-a-freckled-and-frivolous-cake"><i>The Frivolous Cake</i></a>. I have numeroted every verse; we'll store it in a variable for now and come back to it later.


```python
f = open("../Data/poem.txt", "r", encoding="latin1")
poem = f.read()
print(poem)
```

    The Frivolous Cake
    1.1  A freckled and frivolous cake there was
    1.1  That sailed upon a pointless sea, 
    1.2  Or any lugubrious lake there was
    1.3  In a manner emphatic and free.
    1.4  How jointlessly, and how jointlessly
    1.5  The frivolous cake sailed by
    1.6  On the waves of the ocean that pointlessly
    1.7  Threw fish to the lilac sky.
    
    2.1  Oh, plenty and plenty of hake there was
    2.1  Of a glory beyond compare, 
    2.2  And every conceivable make there was
    2.3  Was tossed through the lilac air.
    
    3.1  Up the smooth billows and over the crests
    3.1  Of the cumbersome combers flew
    3.2  The frivolous cake with a knife in the wake
    3.3  Of herself and her curranty crew.
    3.4  Like a swordfish grim it would bounce and skim
    3.5  (This dinner knife fierce and blue) , 
    3.6  And the frivolous cake was filled to the brim
    3.7  With the fun of her curranty crew.
    
    4.1  Oh, plenty and plenty of hake there was
    4.1  Of a glory beyond compare -
    4.2  And every conceivable make there was
    4.3  Was tossed through the lilac air.
    
    5.1  Around the shores of the Elegant Isles
    5.1  Where the cat-fish bask and purr
    5.2  And lick their paws with adhesive smiles
    5.3  And wriggle their fins of fur, 
    5.4  They fly and fly neath the lilac sky -
    5.5  The frivolous cake, and the knife
    5.6  Who winketh his glamorous indigo eye
    5.7  In the wake of his future wife.
    
    6.1  The crumbs blow free down the pointless sea
    6.1  To the beat of a cakey heart
    6.2  And the sensitive steel of the knife can feel
    6.3  That love is a race apart
    6.4  In the speed of the lingering light are blown
    6.5  The crumbs to the hake above, 
    6.6  And the tropical air vibrates to the drone
    6.7  Of a cake in the throes of love.

