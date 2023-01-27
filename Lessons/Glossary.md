# Glossary

## General Terms

You will be coding 

<ul><li><b>The Console</b> is where you input commands for Python to do something: create variables, operate over data, etc.;</li>
<li><b>.py Files</b> is where you store your code ("scripts") for later use;</li>
<li><b>Errors</b> are what happens when your code cannot compute:</li>
    <ul><i>Syntax Errors</i> when you made a typo, forget to close a bracket, or to properly indent your code; or</ul>
    <ul><i>Type Errors</i> is when you try to do something over a data that is not of the proper type, or combine types of data in ways that are impossible: e.g., add a number to a text;</ul>
    <ul><i></i></ul>
<li><b>Modules or Packages</b> are ways to access more functions than are available in native python. There is a package for everyhing you need to do, and more. Typically, you need to:</li>
        <ul><i>Install</i> the package at least once, if it is not native to Python, py typing "pip install package-name"; and</ul>
    <ul><i>Import</i> the package every time you restart the console, with <code>import package</code>.</ul>
<li><b>Functions</b> are ways to operate on the data, usually to get an output from an input. For instance, <code>len()</code> returns the length of a list or of a string. What goes within the brackets of a function are called "arguments";</li>
<li><b>Indexing</b> means trying to get a slice of a data (for example, the content of a list, or the column of a dataframe. You usually index using brackets: <code>ll[0]</code> returns the first element of list ll;</li></ul>

## Data Types

Data takes many forms, and comes with distinct ways to operate on it.

<ul><li><b>Most common Types</b>:</li>
    <ul><i>Integers</i> known as <code>int</code> refer to numbers without decimals;</ul>
    <ul><i>String</i> known as <code>str</code> means text; can be indexed like a list, since it is a list of characters/letters;</ul>
    <ul><i>Dictionaries</i> known as <code>dict</code>, associate a key to a value.</ul>
    <ul><i>Lists</i> are lists of other data types, including lists.</ul>
<li><b>Attached to Data:</b>
    <ul><i>Methods</i> are functions that operate directly on an variable; they always take the form <code>var.method()</code>. For instance, <code>ll.append(x)</code> will add x to the list ll;</ul>
    <ul><i>Attributes</i> are data attached to a variable, for instance the text of an html or xml element can be extracted with <code>el.text</code> (no brackets);</ul>
    <ul><i></i></ul></li></ul>
    
## Syntax

Two key elements of coding are loops and conditions - everything else is built on that.

<ul><li><b>Loops</b> allows you to work on the individual data, one by one, is a list or iterable. The syntax always takes the form <code>for x in l:</code>, with l being a list; what happens within the list is then indented after the ':'. A few things to note:
    <ul><i>the last x in the loop </i> remains assigned to the last data in the list even after you escape the loop;</ul>
    <ul>The keyword <i>break </i> allows you to stop the loop before its term, for instance when a condition is met.</ul>
    <ul>You can have more than one variable assigned in the loop. For instance, the function <code>enumerate</code> allows you to loop with the data points and their index in the list; <code>for e, x in enumerate(l):</code> with e the index, and x the data point, for each data in list l.</ul></li>
    <li><b>Conditions</b> will fork your code depending on if the condition is met. They take the form <code>if x: [then do]</code> with the condition being met if x is <code>True</code> (for instance, <code>len("Cake") == 4</code>).
    <ul>The keyword <i>else:</i>, put at the same indentation level as your if, allows to specify what happens if the condition is not met;</ul>
    <ul>The keyword <i>elif:</i> allows you to create subconditions;</ul>
        <ul>Conditions can be stacked or put as alternatives with the keywords <i>and</i> and <i>if</i>: for instance, if "x" is the number 4, the following condition will not be met: <code>if x == 5 and x / 2 == 4 or type(x) == str:</code>.</ul></li>
</ul>

    
## Common Packages

<ul><li><b>OS</b> allows you to navigate through files and manipulate them. Typical functions are:
    <ul><i>os.getcwd()</i> returns the current directory/folder Pythin is 'in';</ul>
    <ul><i>os.chdir(x)</i> allows Python to move to a subdirectory named 'x'. Note that you can use '..' to return to the parent folder;</ul>
    <ul><i>os.listdir(x)</i> returns the content of folder x. Inputing '.' for x means returning the content of the current folder.</ul></li>
    <li><b>pandas</b> typically abbreviated as <code>pd</code>, allows you to work with dataframes. Typical functions are:
    <ul><i>pd.read_csv("name.csv", header="infer", encoding="ut8")</i> creates the dataframe (usually called <code>df</code> from a csv file;</ul>
    <ul><i>pd.DataFrame(L, columns=lc)</i> creates a dataframe from a list of lists <code>L</code>, with columns name from a list lc. All sublists in L must be the same size;</ul>
    <ul><i>pd.read_html(x)</i> creates a dataframe from a webpage x, or for any variable that contains html in a string format.</ul></li>
    <li><b>etree</b> is a module found in the <code>lxml</code> package ( "from lxml import etree"), allows you to load and operate over xml files. <code>etree.parse(f)</code> will open the .xml file f and pass it to a variable.</li>
</ul>

## Scraping Packages

<ul><li><b>requests</b> allows you to scrap static websites. <code>requests.get(url)</code> returns a <i>webpage</i> variable (from the url), which comes with the following attributes:
    <ul><i>webpage.status_code</i> tells you if the connection was successful (200) or not (404);</ul>
    <ul><i>webpage.content</i> returns the webpage's full .html code.</ul></li>
    <li><b>Beautifulsoup</b>, a module found in the <code>bs4</code> package allows you to work with .html, converting it from pure string to an .html objects (often named soup) with dedicated methods and attributes, such as:
    <ul><i>soup.find()</i> returns the first element that matches your search criteria. For instance, <code>soup.find("a", href=re.compile("/site/"))</code> will return an element "a" (a link), whose attribute "href" contains the string "/site";</ul>
    <ul><i>soup.find_all()</i> returns all elements that matches your search criteria, as a list;</ul></li>
    <li><b>Selenium</b> is a module allowing you to manipulate a webbrowser through Python, and scrap dynamic website. You typically create a variable "driver" that represents your browser. In turn:
        <ul><i>driver.find_element(By, "X")</i> returns the first element that matches your search criteria. The keyword "By" (which needs to be imported) contains a number of categories, such as class or text, the second argument is the value you are looking for for that search methods;</ul>
    <ul><i>soup.find_elements()</i> returns all elements that matches your search criteria, as a list;</ul>
    </li>
</ul>

## NLP Packages

TDD
