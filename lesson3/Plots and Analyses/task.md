# Plots and Analyses

<b>1. </b>Now, once we have done all this, we can check one of the first questions we had: does the CADA slows down 
before elections take place ? 

This is where the module `pyplot` becomes useful and relevant. Shortly put, while `pandas` allows you to make basic 
plots, you often need other modules to fine-tune those plots. Pyplot provides the basics for this: the logic is that 
your plot is located in a `plt` element, which comes with a number of methods to act upon, e.g., the axes, the grid, 
colors, etc.

Another popular module in this context is `seaborn`, often abbreviated `sns`, which provides a number of 
ready-to-use graphs functions. This can also be used in parallel with pyplot and the basic plot tools of `pandas`. 

<b>2. </b> Back to the analysis. One way to look at it is simply to plot the number of decisions, and indicate the relevant 
election (Presidentielle for the Central administration, etc.) with a line. Doing this, it's hard to detect a role 
for elections in the rate of favourable opinions from the cada, although it seems that the number of decisions 
decreases.
