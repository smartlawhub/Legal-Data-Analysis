# List Comprehension

<b>1. </b> Python code is a good middle ground between very verbose code (VBA for instance), and languages that are 
perfectly opaque to the neophythe. When you look at the syntax, given a few basics, you can have a rough idea of 
what's happening.

The issue with verbosity, however, is that it take space and time. If you need to populate a list from another list 
given a condition, you have now learned that you can use a loop and a conditional statement to perform the operation.
But again, it can be cumbersome to write down all of this.

<b>2. </b> Enter list comprehensions, which is a way to create a list in a single line. The syntax is of the kind:
`[x for x in list]`

So, what you are trying to do is to invoke every element in the list, and operate over it to create a new list 
(hence the brackets around the statement).

Note that the power of this method comes from the fact that you can go much further than the bare statement I gave 
you here. For instance, you can vary with is the original list. 

More importantly,  you can add conditions. Here is the previous operation to create `even_list`, done as a list 
comprehension.

Note that you can add conditions, and the usual `and`, `or`, and `None` commands or booleans work in this context as 
well.

Finally, the first item in the list can also be operated upon. Let's say we now want the even numbers from `my_list`,
except times three and in a string that starts with "Number: ".

<u>Exercise 8</u> Take the solution to Exercise 4, and rewrite it in a single line.

<div class="hint"> You can sorted a list with the function sorted, of the form <code>sorted(list, key=XX, reverse=True)
</code>, with key the criteria to sort (such as "len") and reverse to start in descending order.</div>
