<h1>1. Introduction to Python</h1>

<p>This is the first lesson in the context of Course HEC <i>Law Project Legal Data Analytics</i></p>

<p><i>*** First a bit of Semantics: Code, Console, Comments, Etc. . Need to talk about os at some point as 
well***</i></p>

<h2>Basic operations in Python</h2>

<p>Computer code, at its most basic, calculates stuff. You can think of this course and everything that follows as expanding the uses of a calculator. For instance:</p>

```python
2+2
=> 4
```

Typically, in Python you'd use the command `print` to have stuff appear on your screen. It is also more precise, as 
it gives your computer the exact command to process. 

For instance, if you add a line of computations above and try to run everything in the Console, it will only render 
the last line - but if you insert two `print` statement, one after the other, both will render.
`print` is a <em>command</em>. Like most commands, it requires some <em>parameters</em>, that are indicated within brackets. Eg.  

```python
print(2+2)
print(2*3)
```

We will come back to functions a bit later. Before that, we need to discuss <em>variables</em>, which you can think 
of as recipients in which you store information.
Variables are typically written in lower caps; the way  you assign data to a variable is with a `=` sign, as follows.
You can then use variables directly in functions (such as print), or do operations between them.
What do you think will print if we press Enter ?

```python
my_var = 1
my_var2 = 2
my_var3 = 2*3
print(my_var + my_var2 + my_var3)
```
There are different types of numbers in Python, but we'll see that later. Now, variables need not be numbers. They can also be text, which in Python is typically known as a string. Likewise, you can make operations with them, such as collating two strings.

```python
text_var = "Hello World"
text_var2 = "Hello Cake"
print(text_var + text_var2)
```
Do note that the print command does exactly what you ask it to do: it did not insert a space between the two strings here, it's for you to think of this kind of details.

In what follows, we'll use text and strings taken from Mervyn Peake's poem <a href ="https://gormenghasts.tumblr.com/post/80656474535/the-frivolous-cake-a-freckled-and-frivolous-cake"><i>The Frivolous Cake</i></a>. I have numeroted every verse; we'll store it in a variable for now and come back to it later.

```python
poem = "The Frivolous Cake\n1.1  A freckled and frivolous cake there was\n1.1  That sailed upon a pointless sea, \n1.2  Or any lugubrious lake there was\n1.3  In a manner emphatic and free.\n1.4  How jointlessly, and how jointlessly\n1.5  The frivolous cake sailed by\n1.6  On the waves of the ocean that pointlessly\n1.7  Threw fish to the lilac sky.\n\n2.1  Oh, plenty and plenty of hake there was\n2.1  Of a glory beyond compare, \n2.2  And every conceivable make there was\n2.3  Was tossed through the lilac air.\n\n3.1  Up the smooth billows and over the crests\n3.1  Of the cumbersome combers flew\n3.2  The frivolous cake with a knife in the wake\n3.3  Of herself and her curranty crew.\n3.4  Like a swordfish grim it would bounce and skim\n3.5  (This dinner knife fierce and blue) , \n3.6  And the frivolous cake was filled to the brim\n3.7  With the fun of her curranty crew.\n\n4.1  Oh, plenty and plenty of hake there was\n4.1  Of a glory beyond compare -\n4.2  And every conceivable make there was\n4.3  Was tossed through the lilac air.\n\n5.1  Around the shores of the Elegant Isles\n5.1  Where the cat-fish bask and purr\n5.2  And lick their paws with adhesive smiles\n5.3  And wriggle their fins of fur, \n5.4  They fly and fly ‘neath the lilac sky -\n5.5  The frivolous cake, and the knife\n5.6  Who winketh his glamorous indigo eye\n5.7  In the wake of his future wife.\n\n6.1  The crumbs blow free down the pointless sea\n6.1  To the beat of a cakey heart\n6.2  And the sensitive steel of the knife can feel\n6.3  That love is a race apart\n6.4  In the speed of the lingering light are blown\n6.5  The crumbs to the hake above, \n6.6  And the tropical air vibrates to the drone\n6.7  Of a cake in the throes of love."
print(poem)
```
