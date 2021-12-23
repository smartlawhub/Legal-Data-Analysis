## Syntax

<b>1.</b> Finally, some basics notions of syntaxes. You write code as you would write anything: sequentially. This means you first define your variables or your functions before using it, or Python won't be able to know what you mean.

An important first concept is the `loop`, which tells Python to do something as long as a condition is not fulfilled. The typical use is to go over (the term is "iterate") a number of elements, for instance in a list.

<b>2.</b> You will note that for your loop to work, the second level of instructions needs to be shifted to the right. That's 
called identation, and this is crucial in Python. It's also one of the main reasons why people don't like this 
language. Other languages are more explicit as to when a section of your code is actually contained in another 
section: for example, in C++ you would put stuff within brackets, or indicate the end of a statement with a semi-colon 

<b>3.</b> The second important syntax element, and really the basic building block of so much code that runs your 
daily life, is the `if/else` statement. It simply asks if a condition is met, and then accomplish the resulting code. 
In the example below, we will check that the letter "e" (i.e., a string corresponding to the lower case "e") is present in a list of words.

<b>4.</b> They are several ways to syntax `if` statements:
<ul><li>With an <code>is in</code> if need to check that an item is part of a list or a set (or the inverse 
<code>is not in</code>)</li>
    <li>By itself if you are checking a boolean (<code>if my_bol:</code> will return <code>True</code> or 
<code>False</code> depending on the value of <code>my_bol</code>)</li>
    <li>With the double equal sign <code>==</code> for identity between two variables, or <code>!=</code> for lack of 
identity</li>
    <li>With a combination of the signs <code>></code>, <code><</code> and <code>=</code> when comparing two quantities.
</li>
    <li>You can also complicate the conditions with <code>and</code> or <code>or</code>.</li></ul>
<p>Finally, a middle point between if and else is <code>elif</code>, which gives you another chance to check if a 
condition is met.</p>

<b>5.</b> Note that an issue of adding too many conditions to a line, as above, is that you don't know which one was 
true or false.

This leads us to discuss a number of "best practices" when coding. Type `import this`. Note the point about 
namespaces: you can get the list of `namespaces` with dir(__builtins__). Understand that variables have different 
scopes (LEGB Rule).

This is all, or nearly. On the basis of the very basic concepts I just introduced to you run most of the rest of the Python scripts you can see out there. 

<b>6.</b> <u>Exercise 3</u>On the basis of what you learned in the past hour, please iterate over the lines of the 
poem (not the individual words), in order to find the number of terms "cake" and "knife" (not counting the one in 
the title). Print that number.
