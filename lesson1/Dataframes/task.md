## Dataframes

<b>1. </b>A lot of the analyses you'll be asked to perform will be based on a dataframe, i.e., a spreadsheet where 
data is structured in rows and columns. 

There are other ways to store, access, and exploit data (we'll discuss Structured Data in the next Lesson), but 
usually even that data is at one point converted into a dataframe, over which you'll perform (and record) your analyses.

<b>2. </b>The main and most popular module in Python for dataframes is called `pandas`, and frequently abbreviated 
as `pd`. Think of pandas in this context as an equivalent of Microsoft Excel - except 
infinitely more flexible (though you can do much more with Excel if you learn VBA, the language powering it).

We'll introduce you very softly to pandas today, keeping most of the heavy work for another lesson - but you'll need 
the basics to properly follow through the lessons on Scraping, for instance.

<b>3. </b>This course comes pre-loaded with a `.csv` file about cheeses. We'll perform a number of operations over 
it to showcase `pandas`'s abilities. It's a very simple dataframe with names and types of cheese.

You first load the file with pandas, which makes it easy for you for a dedicated `read_csv` function (no need to use 
a reader/writer as we just saw before).

```python
import pandas as pd

df = pd.read_csv("fromages.csv", header="infer", encoding="utf8")
```

Then we can do a bit of data investigation, see what's the most interesting column or data, etc.

<b>3. </b> In particular, it would be helpful to match the Départements with their region. Fortunately, we have a 
second dataset that does just that, so let's try to match them in a single dataset. In Excel, you would do a VLookup,
or something like this; here, it's simpler to create a dictionary from the first dataset, and map it to our 
dataframe `df`.

<b>4. </b>Finally, let's do something more ambitious. I searched for a way to make maps of France online, and just 
copied and pasted the relevant code.  This is will be the topic of the exercise.

<u>Exercise</u> Based on the two datasets, create a dictionary that you will be able to inputted in the French map 
renderer: it should take department numbers (not names) as keys, and the number of entries as values.
