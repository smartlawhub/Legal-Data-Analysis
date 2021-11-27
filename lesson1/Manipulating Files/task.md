## Manipulating Files

<b>1.</b> This course is about data analysis, not software creating. You'll mostly use the Console, and won't 
particularly need to write `.py` scripts, invent new classes, etc. Scripts can record methods and functions you 
invented, but most analyses are transient: you use it on the go, sometimes for a single task, and get to something 
else.

And yet, the data to be analysed needs to be stored. We'll now see the basics of this.

<b>2. </b>But first a word about how computers work. You've got memory: your hard drive. You've got RAM: Random 
Access Memory, which is what your computer use to perform its basic tasks. There is a constant <i>va et vient</i> 
between the two. When you create a new variable, it's stored in RAM; if you want to use it next time, you need to 
store it in the secondary memory.

<b>3. </b>You can do that through Python, but you need an interface between the code and your computer 
environment. Fortunately, Python relies on the same kind of methods that are at the basis of most computers (since 
they get their roots in the UNIX system. If you open the Command Prompt (`cmd` on Windows, or the Terminal on a Mac),
you 
can navigate between folders with the command `cd` (for "Change directory"), or create a new folder with `mkdir`.

<b>4. </b>By default, the Console is virtually located in the folder that hosts your Python Script. But you can move 
as if you were in the command prompt. Notably, `cd` works as well. Use it with a double period, `cd ..` to go back 
one folder.

<b>5. </b>We can do more than that, and here it's helpful to use `os`, a module that lets you navigate through, and 
manipulate files with Python. For instance, the command `os.listdir(".")` returns the list of files and folders 
in a given directory. (Note that the argument we gave it was ".", which usually means "this current folder".)

`os` is also very helpful to manipulate files from Python, for instance renaming them. Instead of spending an hour 
renaming hundreds of files, you can do it in a few lines, for instance:

```python
import os 

print(os.listdir("."))  # We check what files are in the folder
file = "text.txt"  # We select a file that is in the folder and attribute it to a variable
newnamefile = file + "a"  # We decide on a new name given a file
os.rename(file, newnamefile) # We provide os's rename function with the required variables
```

Note that the resulting file is now corrupted: you changed the extension from `txt` to `.txta`, which is unknown - 
and so you can't read it anymore. There are ways to control for this, but this is the subject of the exercise.

<u>Exercise 5</u> Go to the `Gibberish` folder in Lesson 1 > Storing Data, and rename all files that do not finish 
by a `_\d` format (for instance, `Damien Charlotin_10786`, but not `Damien Charlotin_10786_1`). Rename these files 
by adding `_main` to their name. How many files have you renamed ?

<div class="hint">Remember how to deal with lists, and relative indexing.</div>
