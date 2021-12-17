# Synthetise Data

<b.>1. </b>Your analyses will be more powerful if you are able to synthetise the data in the dataset.

For instance, when you look at the different results recorded in 
the `Sens et motivation` column, you can see that the categories are not super helpful. It'd be better to group them 
in two categories: favourable, and unfavourable (counting instances of "Incompétent", "Inexistant", etc. as 
unfavourable).

We might also want to group the different sorts of administrations, but this is harder, as they are many more 
categories. We can do a process of iterating through these until most have been tagged one way or another, and be 
happy with leaving the "Other" on the side.

<u>Exercise 2</u> Improve the `dict` until the category "Other" in the column `Admin` has fewer than 90 entries. You 
well need to use regex in particular to get there.
