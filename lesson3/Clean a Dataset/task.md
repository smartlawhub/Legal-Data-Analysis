# Organise a Dataset

<b>1. </b> Before working on the data you collected, let's turn to an existing dataset, which you can find on data.
gouv.fr. <a href="https://www.data.gouv.fr/fr/datasets/avis-et-conseils-de-la-cada/">here</a>.

This is a heavy file - we'll downsize it a bit later -, which collects all decisions by the CADA since its creation 
until November 2011, nearly 50,000 in total. We'll clean and perform basic analyses of this file, so as to answer a 
very simple and distinctive question: is the rate of positive/negative decisions by the CADA influenced by elections ?

<b>2. </b> CSV cells have a character limit (exactly 32,767 for a single cell, the same as in Excel, although the 
latter also have row and columns limits), and it's quite frequent that this is exceeded when dealing with 
texts. 

Sure enough, this one has an error at some point, which is clearly visible when you open the file on Excel, but can 
also be guessed due to higher-than-expected number of columns in the pandas df (all those "Unnamed" columns).

Although we could clean this quickly by opening the .csv file in Excel, we can also do it with `pandas`. Notice that 
overflowing text will often be stored on a new row, and then use columns that are not meant to receive text. For instance, the first column of 
the dataframe here is `Numéro de dossier`, and it's always a number following a specific format.

Once we know this, it's easy enough to locate rows that are corrupted. Here is one way:

This will identify the rows that are corrupted. Although we did that by focusing on the `.len` of some entries, there 
are plenty of other ways to go about it. You could for instance check which cells in the first column can't be expressed as a number, which row 
does not have all columns correctly filled (assuming they all should), etc.

<b>2. </b> Once it's cleaned, we can start investigating it. One question you migh ask is: what are the types of 
decisions in the dataset. In other words,  what's the distribution ? `value_counts` is particularly helpful here, 
especially when you normalise the data to have percentages.

Another question, since we have the Years, is to check the chronological evolution of the number of decisions. Here 
as well, we could use `value_counts`, but it's sometimes easier to group the dataframe by a data point (here, years) 
and then find out the size of every group.

<b>3. </b> You can also be interested in locating specific items in the dataset. Here, `pandas` offers you plenty of 
ways to pinpoint a specific row, or colums, or cell - though it's not always intuitive. Once again, having an idea 
of the type of output will really help you understand how to manipulate all these. For instance, `.iloc` returns a 
row, while `.loc` returns another, smaller dataframe. `.at` returns a cell, because you need to specify both an 
index (row) and a column.

<u>Exercise 1</u> TBD
