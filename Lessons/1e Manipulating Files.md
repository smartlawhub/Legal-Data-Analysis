# Manipulating Files

This course is about data analysis, not software creating. You'll mostly use the Console, and won't 
particularly need to write `.py` scripts, invent new classes, etc. Scripts can record methods and functions you 
invented, but most analyses are transient: you use it on the go, sometimes for a single task, and get to something 
else.

And yet, the data to be analysed needs to be stored. We'll now see the basics of this.

## Navigating Files

But first a word about how computers work. You've got memory: your hard drive. You've got RAM: Random 
Access Memory, which is what your computer use to perform its basic tasks. There is a constant <i>va et vient</i> 
between the two. When you create a new variable in the Console, it's stored in RAM; if you want to use it next time, 
you need to store it in the secondary, hard memory.

You can do that through Python, but you need an interface between the code and your computer 
environment. Fortunately, Python relies on the same kind of methods that are at the basis of most computers (since 
they get their roots in the UNIX system). If you open the Command Prompt (`cmd` on Windows, or the Terminal on a Mac),
you can navigate between folders with the command `cd` (for "Change directory"), or create a new folder with `mkdir`.

Three commands in particular will be useful during this course:
<ul><li><b>os.getcwd()</b>, which means "Get Current Working Directory", outputs the current position of Python 
within your files</li>
<li><b>os.chdir("x")</b>, which "changes dir" to the directory x you specify in argument (x needs to be a subfolder 
of the current folder: you cannot directly change dir to a sub-sub-folder, for instance).</li>
<li><b>os.listdir(".")</b>, which returns a list of files in a directory (using the "." argument means: in the 
current directory.)</li></ul>

(Note that the argument we gave to the listdir() method was ".", which usually means "this current folder", whereas 
".." always means "parent folder".)


```python
import os

current_path = os.getcwd()
print(current_path)

os.chdir("..")
new_path = os.getcwd() 
print(new_path)

print(os.listdir("."))  # We check what files and subfolders are in the folder
os.chdir("Lessons") 
print(os.listdir("."))
```

    /home/DamienCh/LDA/Lessons
    /home/DamienCh/LDA
    ['bin', '.gitignore', 'Lessons', 'pyvenv.cfg', 'lib', 'Data', 'Scripts']
    ['.ipynb_checkpoints', '1e Manipulating Files.ipynb', '1b Lists.ipynb', '1c Functions and Methods.ipynb', '1d Syntax.ipynb', '1.a Variables.md']


`os` is also very helpful to manipulate files from Python, for instance renaming them. Instead of spending hours 
renaming hundreds of files (a common thing for junior lawyers), you can do it with the `os.rename(x, y)` method, which changes file x into y.

Note that the resulting file is now corrupted: you changed the extension from `txt` to `.txta`, which is unknown - 
and so you can't read it anymore. There are ways to control for this, but this is the subject of the exercise.


```python
file = "../Data/Empty File is Empty.txt"  # We select a file that is in the folder Data and attribute its name to a variable
newnamefile = file + "a"  # We decide on a new name to give that file
os.rename(file, newnamefile)
print("The new file list is: ", os.listdir("../Data"))
os.rename(newnamefile, newnamefile[:-1])  # We do it a second time to revert to original name
print(os.listdir("../Data"))
```

    The new file list is:  ['Empty File is also Empty (or is it)1.txt', 'Empty File is Empty.txta', 'poem.txt']
    ['Empty File is Empty.txt', 'Empty File is also Empty (or is it)1.txt', 'poem.txt']


## Load and Store data

Anyhow, back to storing data. The canonical way to do it in Python is by opening a file and storing it in a 
variable. This variable (or object) comes with distinct methods, such as "read()" which returns the data inside the 
file. Another method is "write()", which allows you to add to the existing data.

To create a new file, you'd use the with syntax `with open("your_file_name.txt", "a") as f:`; and then, in the 
indented part of the code, you use the "write()" method of the "f" object to add your text to the data.
Note the "a"argument, which means that you want to both read and write in the file (you could input "r" only for reading, or "w" only for writing). 

*** You may want to learn a bit about encoding, and the <a href="https://nedbatchelder.com/text/unipain/unipain. html#1">Unipain</a>***


```python
f = open("../Data/poem.txt", encoding="latin1")
poem = f.read()
print(poem)
f.close()

with open("../Data/poem2.txt", "a", encoding="utf8") as f:
    f.write(poem)
    
os.listdir("../Data")  # We check that we indeed saved a new "poem2" file in the Data folder
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





    ['Empty File is Empty.txt',
     'Empty File is also Empty (or is it)1.txt',
     'poem2.txt',
     'poem.txt']



This is text data, arguably the most straightforward type of data to handle. As we'll see in the next 
task, however, a lot of what you'll be handling is structured data: either in marked-up format (XML, HTML), or in 
some kind of spreadsheet. You probably know Excel's native `.xls` format for spreadsheet, but there are plenty 
others, and a good deal of data analysis relies on a simple format called `.csv` - which stands for comma-separated 
value.

Depending on what you do, you might not need to rely on these methods much: we'll see at some point 
how to handle data with pandas, which has its own, more straightforward methods to save and load data. Likewise, XML 
tools in Python typically have their own methods.

# PDFs

Beyond text, .csv, and structured content, data is sometimes enclosed in .pdfs. Now, this is an issue: .
pdfs are not meant for data analysis, their (main) interest, and the reason why they have been invented, is to be a 
format that preserves a maximum the appearance of a file, on all platforms. But this is not a data-friendly format.

Unfortunately, a lot of data out here is found in .pdfs, so you'll have to wrestle with them to extract their data. 
For this, you'll need to use a third-party library dedicated to .pdfs files, such as `pyPDF2` or `pdfminer`. But the 
principle is the same: you open your .pdf and store it in an object, and then you use methods from this object (they 
would differ depending on the package used) to obtain the data you are interested in.


```python
import PyPDF2 as PDF  # It's a third-party module, so you may have to install first with "pip install pypdf2"

pdf = PDF.PdfFileReader("../Data/Example.pdf")  # We open the .pdf file found in the Data folder
num_pages = pdf.getNumPages()
text = ""
for page in range(0, num_pages):
    text += pdf.getPage(page).extractText()  # You need to loop over the number of pages to extract the whole text

print(text[:500])  # Printed text (the first 500 charac) is not great (page number appears, words are cut, URLs are not captured)
```

     
     
    INTERNATIONAL COURT OF JUSTICE
     
    Peace Palace, 
    Car negieplein 2, 
    2517 KJ 
     
    The Hague, Netherlands
     
    Te
    l
    .
    :
     
    +31 (0)
    70
     
    302 2323
       
    Fax: +31 (0)
    70 364 9928
     
    Website
       
    Twitter
       
    YouTube
       
    LinkedIn 
     
     
     
    Press R elease
     
    Un official
     
     
     
     
     
    No.
     
    20
    2
    1
    /
    35
     
     
    7
     
    December
     
    20
    2
    1
     
     
     
     
    Application of the International Convention on the Elimination of All Forms 
     
    of Racial Discrimination (Azerbaijan
     
    v. 
    Armenia)
     
     
    The Court  indicat es provisional measures t o prot

