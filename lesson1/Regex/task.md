<html>

<h2>Regex</h2>

<b>1. </b>It's time to introduce regular expressions, or "regex" for short. (more info <a
        href='https://docs.python.org/3/library/re.html'>here</a>)

We'll spend some time on it because it is extremely important for text-heavy applications; in a course about
finance  or statistics we would not need it too much, but since we'll be analysing judgments and legal texts, regexes
    are essential.

<b>2. </b>Regexes are patterns that allow you to identify text. These patterns rely on special symbols to cover a 
range of characters in natural, written language.
    For instance, the symbol "\d" means "any number", and if you try to match this pattern with a sentence that includes a number, there will be a positive result.

 ```python
import regex as re # regex is typically abbreviated as re

target_sentence = "Count: 3 frivolous cakes and 4 knifes !"
pattern = "\d"
sear = re.search(pattern, target_sentence)
print(sear)
=> <regex.Match object; span=(7, 8), match='3'>
```

<b>3. </b>Regex will return a regex object, which comes with a number of characteristics. For instance, the "sear" 
object stores the start of the matching pattern in the target sentence, as well as its end, and the exact matched pattern. 

You'd note that there were two numbers in the target sentence, but the "search" function only found one - the first one. To get all matches, you need another function, which is "findall", and returns a list.
 ```python
print(re.findall(pattern, target_sentence))
=> ['3', '4']
```

<b>4. </b>In addition, you have re.sub(pattern, newpattern, target_sentence), that substitutes a pattern for a new 
pattern, as well as re.split(pattern, target_sentence) which returns a list of strings from the original text, as split by the pattern. Notice that the result does not display the splitting pattern

 ```python
print(re.sub("Cake", "Hake (?!)", poem[:20]))
=> The Frivolous Hake (?!)
print(re.split(" ", poem[:20]))
=> ['The', 'Frivolous', 'Cake\n\n']
```

<b>5. </b>All very good, now, here are the basic patterns:
<ul><li>Any particular word or exact spelling will match itself: "cake" will match "cake" (but not "Cake", unless you command regex to be case-insensitive);</li>
    <li>".", catches anything, really, except a newline;</li>
    <li>\s matches white spaces, including line breaks, etc.; note that the upper-case version, \S, matches anything <i>but</i> a white space; and</li>
    <li>\w matches a letter, while \W matches anything but a letter.</li>
    </ul>
In addition, the following rules apply
<ul><li>Square brackets can be used to indicate a range of characters, such as "[0-8a-q]" will only look for a number between 0 and 8 OR a letter between a and q;</li>
    <li>The symbol "|" (that's Alt + 6 on your keyboard) means "or";</li>
    <li>You'd indicate the expected number of hits with braces: [A-Z]{3} means you are looking for three (consecutive) upper-case letters between A and Z, while [A-Z]{3,6} means you expect between 3 and 6, and [A-Z]{3,} means "at least 3" (but potentially more). Two special characters do the same job, but open-ended, "+" means that you are expected at least one hit, while "*" means you expect any number of hits (including none);</li>
    <li>Any pattern becomes optional if you add a "?" behind it: "cakey?" will find "cakey" or "cake"; and</li>
    <li>You can group patterns by bracketing them with parentheses, and then build around it: for instance, "([0-8a-q])|([9r-z])". You can even name the groups to retrieve them precisely from the regex object when there is a match.</li>
    <li>Characters that are usually used for patterns (such as "?" or "|") can be searched for themselves by "escaping" them with an anti-slash "\" (and the antislash can be escaped with another antislash: "\\" will look for "\")</li>
    </ul>

Regex really turns powerful in that you can add a number of conditions to you regex pattern.

<ul><li>A pattern preceded by a "^" will be looked for unly at the beginning of a line; a pattern followed by a $ will only look for it if it finishes the line;</i>
    <li>Adding a "(?=2ndpattern)" <i>after</i> your first pattern will indicate that your first pattern will match <i>only if</i> the target text matches your second pattern, but the second pattern won't be caught by the regex object (this is very useful, e.g., for substitution).</li>
    <li>In the same vein, "(?!2ndpattern)", "(?&lt;=2ndpattern)", and "(?!&lt;2ndpattern)" are conditions for "if it does not match after"; "if it matches before", and "if it doesn't match before", respectively.</li>    
    </ul>

Latest versions of regex also provides for fuzzy searches - that is, with a bit of leeway to catch things despite errors in the pattern (this is exponentially greedy in resources, though, so be careful when you use it). For instance, re.search("(coke){e<=1}", poem), where the braced statement means "one or less errors (e)" will find "cake", as there is only one difference (the latter o/a) between the pattern and the word. 

Finally, there are so-called <i>flags</i> that are typically used outside of the pattern (but can be used inside for a single sub-pattern), as a third argument, to indicate further instructions, such as:
<ul><li>Ignorecase, "re.I"</li>
    <li>Ignore linebreaks "re.S"</li>
    <li>Verbose (allows you to add white spaces that don't count as pattern), "re.X"</li>
    <li>Multilines ($ and ^ will work for any single line, and not simply for the start and end of the full text), "re.M"</li>
    </ul>

Regex count as boolean: "if sear" will return "True" if there was a match, while you check for a null result by asking "if sear is None".

Here is a full-on example:

 ```python
sear = re.search(r"""(?<=the\s)   # A look-before condition
                    (?P<first>[A-Z]\w*?)  # first capitalised term we are looking for; note the ? after *
                    \s?  # Then we look for a white space
                    (?P<second>[A-Z]\w*?$)  # and finally the second capitalised word""", poem, re.M|re.X)
print(sear.group("first"))
print(sear.group("second"))
 ```

<u>Exercise 4</u> Write some code that will identify the number of the line that meets the following conditions: 
<ul><li>An odd number of words, but fewer than 8 in total (<u>not</u> counting the numbers at the beginning of the line)</li>
    <li>At least one "ake" sound in it;</li>
    <li>No capitalised letter except for the first one; and</li>
    <li>The most "e"s;</li>
    </ul>

There is only one line that meets all these conditions. You can do it multiple ways, using all the methods you have learned so far.

<div class="hint"> Look at the raw poem above (remove the "print" statement), and find the relevant pattern to split 
the poem in lines. Then identify the relevant pattern for each line !</div>

<div class="hint">Think analytically: what's the first step of your algorithm, what's the condition to proceed to 
the second step, etc.</div>
<div class="hint">Be careful of the numbers at the beginning of a line: they count as two words, and you should 
account for it in one way or another !</div>
