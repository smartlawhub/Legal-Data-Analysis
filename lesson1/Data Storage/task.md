## Storing Data

<b>1. </b> Anyhow, back to storing data. The canonical way to do it in Python is by opening a file, storing it in a 
variable with methods such as `.write()`, and then closing it. The two methods that follow are equivalent, one is 
self-contained (the file closes itself once the indented code is executed), the other more open-ended (code will 
compute until you manually close the file).

```python
with open("poem.txt", "ab") as f:
    f.write(poem)

f = open("poem.txt")
text = f.read()
print(text)
f.close()
```

*** Talk a bit about encoding ***

<b>2. </b> This is text data, arguably the most straightforward type of data to handle. As we'll see in the next 
task, however, a lot of what you'll be handling is structured data: either in marked-up format (XML, HTML), or in 
some kind of spreadsheet. You probably know Excel's native `.xls` format for spreadsheet, but there are plenty 
others, and a good deal of data analysis relies on a simple format called `.csv` - which stands for comma-separated 
value.

Python has a built-in module to handle the opening and writing of csv files, as follows:

```python
import csv

with open("first_csv.csv", "w") as csv_file:
    writer = csv.writer(csv_file, delimiter=",")

    writer.writerow(["Cake", "Beautiful", "Sensitive"])
    writer.writerow(["Knife", "Gliterring", "Murderous"])
```

And you would read it in the same manner, but with the `reader` function.

*** Maybe talk about .zips et al. ***

<b>8. </b> Depending on what you do, you might not need to rely on these methods much: we'll see in the next lesson 
how to handle data with pandas, which has its own, more straightforward methods to save and load data. Likewise, XML 
tools in Python typically have their own methods.

<u>Exercise 6</u> Without looking at it in your navigator (in any case it won't work), find in the "Gibberish" 
folder the name of the file that has the answer to the exercise. The answer is somewhere in the file, and will be 
preceded by the (exact) terms `answer=`.
