# Regexes

Earlier we devised a basic algorithm to count the number of words in a text. However, there is a 
much better, simple way to do this: It's time to introduce regular expressions,  or "regex" for short. (more info <a href='https://docs.python.org/3/library/re.html'>here</a>)

We'll spend some time on it because it is extremely important for text-heavy applications; in a course about
finance  or statistics we would not need it too much, but since we'll be analysing judgments and legal texts, regexes
    are essential. And they are great. At the end of this task, you'll be annoyed every time search engines (like 
Google) don't do regex. It's just so much better.


```python
import regex as re  # regex is typically abbreviated as re

with open("../Data/poem.txt", "r", encoding="latin1") as f:
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


Regexes are <i>patterns</i> that allow you to identify text. These patterns rely on special symbols to 
cover a range of characters in natural, written language. Because they rely on patterns, it's much more powerful 
than a search that focuses on a specific word: the word itself might be conjugated, or put in lower caps; a sentence 
could have extra words. You might be interested in a range of number and not a specific one, etc.
    
For instance, the symbol "\d" means "any number", and if you try to match this pattern with a sentence that includes a number, there will be a positive result.


```python
target_sentence = "Count: 30 frivolous cakes and 40 knifes !"
pattern = r"\d"
result = re.search(pattern, target_sentence)
print(result)
```

    <regex.Match object; span=(7, 8), match='3'>


Regex.search() will return a regex object (here, the variable `result`), which comes with a number of characteristics. For instance, that object stores the start of the matching pattern in the target sentence, as well as its end, and the exact matched pattern (method ".group()").



```python
print("Pattern was found at index ", result.start(), " of target string !")
print("String continued after pattern at index ", result.end())
print("Regex search found ", result.group(), " that matched this pattern")
```

    Pattern was found at index  7  of target string !
    String continued after pattern at index  8
    Regex search found  3  that matched this pattern



You'd note that there were several numbers in the target sentence, but the "search" function only found one - the first 
    one. To get all matches, you need another function, which is `findall`, and returns a list of result.


```python
re.findall("\d", target_sentence)
```




    ['3', '0', '4', '0']



In addition, you have `re.sub(pattern, newpattern, target_sentence)`, that substitutes a pattern for a new 
pattern. 

There is also `re.split(pattern, target_sentence)` which returns a list of strings from the original text, as 
split by the pattern. Notice that the result does not display the splitting pattern.


```python
print(re.sub("Cake", "Hake (?!)", poem[:19]))
print(re.split(" ", poem[:20]))
```

    The Frivolous Hake (?!)
    
    ['The', 'Frivolous', 'Cake\n1']


All very good, now, here are the basic patterns:
<ul><li>Any particular word or exact spelling will match itself: <code>cake</code> will match <code>cake</code> (but not 
<code>Cake</code>, unless you command regex to be case-insensitive - see below);</li>
    <li><code>.</code>, catches anything, really, so <code>c.ke</code> would get "cake" or "coke", or even "cOke"; if you need to look specifically for a period, you need to escape it with an antislash <code>\.</code> </li>
    <li><code>\s</code> matches white spaces, including line breaks, etc.; note that the upper-case version, 
<code>\S</code>,matches anything <i>but</i> a white space; and</li>
    <li><code>\w</code> matches a letter, while <code>\W</code> matches anything but a letter.</li>
    </ul>



```python
print(re.findall(".ake", poem)) # Plenty of "ake" sounds in that poem
print(re.findall("\d\.\d", poem)) # Too look for a period, you need to escape it with an antislash 
print(re.search("\W", poem))  # It will find the first space in the poem
```

    ['Cake', 'cake', 'lake', 'cake', 'hake', 'make', 'cake', 'wake', 'cake', 'hake', 'make', 'cake', 'wake', 'cake', 'hake', 'cake']
    ['1.1', '1.1', '1.2', '1.3', '1.4', '1.5', '1.6', '1.7', '2.1', '2.1', '2.2', '2.3', '3.1', '3.1', '3.2', '3.3', '3.4', '3.5', '3.6', '3.7', '4.1', '4.1', '4.2', '4.3', '5.1', '5.1', '5.2', '5.3', '5.4', '5.5', '5.6', '5.7', '6.1', '6.1', '6.2', '6.3', '6.4', '6.5', '6.6', '6.7']
    <regex.Match object; span=(3, 4), match=' '>


In addition, the following rules apply:
<ul><li>Square brackets can be used to indicate a range of characters, such as <code>[0-8a-q,]</code> will only look 
for a number between 0 and 8 OR a letter between a and q, or a comma (if you need hyphens in your range, put them at 
the end of the range);
</li>
    <li>The symbol <code>|</code> (that's Alt + 6 on your keyboard) means "or";</li>
    <li>You'd indicate the expected number of hits with braces: <code>[A-Q]{3}</code> means you are looking for three 
(consecutive) upper-case letters between A and Q, while <code>[A-Q]{3,6}</code> means you expect between 3 and 6, 
and <code>[A-Q]{3,}</code> means "at least 3" (but potentially more), on the same logic as indexing (except use 
        commas instead of colons).</li> 
    <li>Two special characters do the same job, but open-ended, "+" means that you are expected 
at least one hit, while <code>*</code> means you expect any number of hits (including none; add a <code>?</code> for 
non-greediness). A concrete example would be <code>\d{4}</code>: a date;</li>
    <li>Any pattern becomes optional if you add a <code>?</code> behind it: <code>cakey?</code> will find <code>cakey</code> or 
<code>cake</code>;</li>
    <li>You can group patterns by bracketing them with parentheses, and then build around it: for instance, <code>(
[0-8a-q])|([9r-z])</code>. You can even name the groups to retrieve them precisely from the regex object when there is a match.</li>
    <li>Characters that are usually used for patterns (such as  <code>?</code> or  <code>|</code>) can be searched for 
themselves by "escaping" them with an anti-slash  <code>\</code> (and the antislash can be escaped with another 
antislash:  <code>\\</code> will look for  <code>\</code>). Note that <code>regex</code> provides you with an 
<code>escape</code> function that returns a pattern, but escaped.</li>
    </ul>


```python
print(re.findall("[chlwm]ake", poem))
print(re.search("cake|knife", poem))
print(re.search("\d\d-\d{2}-\d+", "This is a date: 11-02-1992"))  # Note that \d\d and \d{2} are strictly equivalent
print(re.search("cakey?", "cake or cakey?")) # Here as well, if you ever need to look for an "?", you need to escape it: "\?"
```

    ['cake', 'lake', 'cake', 'hake', 'make', 'cake', 'wake', 'cake', 'hake', 'make', 'cake', 'wake', 'cake', 'hake', 'cake']
    <regex.Match object; span=(49, 53), match='cake'>
    <regex.Match object; span=(16, 26), match='11-02-1992'>
    <regex.Match object; span=(0, 4), match='cake'>


Finally, there are so-called <i>flags</i> that are typically used outside of the pattern (but can be used inside for a single sub-pattern), as a third argument, to indicate further instructions, such as:
<ul><li>Ignorecase, <code>re.I</code>;</li>
    <li>Ignore linebreaks <code>re.S</code>;</li>
    <li>Verbose (allows you to add white spaces that don't count as pattern), <code>re.X</code>; and</li>
    <li>Multilines (<code>$</code> and <code>^</code> will work for any single line, and not simply for the start 
and end of the full text), <code>re.M</code></li>
    </ul>


```python
print(re.search("cake", "The Frivolous Cake", re.I))  # This works despite the capital C since we specified re.I
```

    <regex.Match object; span=(14, 18), match='Cake'>


Regex really turns powerful in that you can add a number of conditions to you regex pattern.

<ul><li>A pattern preceded by a  <code>^</code> will be looked for only at the beginning of a line; a pattern 
followed by a <code>$</code> will only look for it if it finishes the line or text;</li>
    <li>Adding a <code>(?=2ndpattern)</code> <i>after</i> your first pattern will indicate that your first pattern 
will match <i>only if</i> the target text matches your second pattern, but the second pattern won't be caught by the regex object (this is very useful, e.g., for substitution).</li>
    <li>In the same vein, <code>(?!2ndpattern)</code>, <code>(?&lt;=2ndpattern)</code>, and <code>(?!&lt;2ndpattern)
</code> are conditions for "if it does not match after"; "if it matches before", and "if it doesn't match before", 
respectively. This can be hungry in terms of computing power, so don't overdo it.</li>    
    </ul>


```python
print(re.search("^A Freckled|throes of love.$", poem)) # Only the second alternative will be found, since the first words are not at
# the beginning of a line (the numbers 1.1 are)
print(re.search("plenty of (?=cake)", poem)) #This returns None since there are no "plenty of cake" in the poem
print(re.search("plenty of (?=.ake)", poem)) #But this returns a match, since there is "hake"
```

    <regex.Match object; span=(1667, 1682), match='throes of love.'>
    None
    <regex.Match object; span=(357, 367), match='plenty of '>


Latest versions of regex also provides for fuzzy searches - that is, with a bit of leeway to catch things despite errors in the pattern (this is exponentially greedy in resources, though, so be careful when you use it). For instance, `re.search("(coke){e<=1}", poem)`, where the braced statement means "one or less errors (e)" will find "cake", as there is only one difference (the latter o/a) between the pattern and the word. 

Finally, regex objects count as boolean: <code>if result</code> will return <code>True</code> if there was a match, while you can check for a null result by asking "if result is None". (`None` is a special Python object that means that data is empty.)

Note that there are tools to help you check if your regexes work well on the given dataset, such as <a 
href="https://www.debuggex.com/">this one</a> online.


```python
for line in poem.split("\n"): # We split the poem by lines and we loop over these lines
    if re.search("cake|knife", line, re.I):  # we check that the term "cake" is or not in the line
        print(line)  # If it is, we print the line
    else:
        print("No Cake or knife in that line...")
```

    The Frivolous Cake
    1.1  A freckled and frivolous cake there was
    No Cake or knife in that line...
    No Cake or knife in that line...
    No Cake or knife in that line...
    No Cake or knife in that line...
    1.5  The frivolous cake sailed by
    No Cake or knife in that line...
    No Cake or knife in that line...
    No Cake or knife in that line...
    No Cake or knife in that line...
    No Cake or knife in that line...
    No Cake or knife in that line...
    No Cake or knife in that line...
    No Cake or knife in that line...
    No Cake or knife in that line...
    No Cake or knife in that line...
    3.2  The frivolous cake with a knife in the wake
    No Cake or knife in that line...
    No Cake or knife in that line...
    3.5  (This dinner knife fierce and blue) , 
    3.6  And the frivolous cake was filled to the brim
    No Cake or knife in that line...
    No Cake or knife in that line...
    No Cake or knife in that line...
    No Cake or knife in that line...
    No Cake or knife in that line...
    No Cake or knife in that line...
    No Cake or knife in that line...
    No Cake or knife in that line...
    No Cake or knife in that line...
    No Cake or knife in that line...
    No Cake or knife in that line...
    No Cake or knife in that line...
    5.5  The frivolous cake, and the knife
    No Cake or knife in that line...
    No Cake or knife in that line...
    No Cake or knife in that line...
    No Cake or knife in that line...
    6.1  To the beat of a cakey heart
    6.2  And the sensitive steel of the knife can feel
    No Cake or knife in that line...
    No Cake or knife in that line...
    No Cake or knife in that line...
    No Cake or knife in that line...
    6.7  Of a cake in the throes of love.

