import pandas as pd
from lxml import etree  # This is one of the main .xml reader module in Python, the etree method from the lxml package. You need to : pip install lxml
import os
from datetime import datetime
from collections import defaultdict, Counter

os.chdir("../Data/CE")  # We go to the main folder that stores all files
files = os.listdir(".")  # We create a list of all files

for file in files:
    xml_file = etree.parse(file)  # We first open the .xml file with the "parse" method
    root = xml_file.getroot()  # We then look for the "root" of the XML tree, and pass it to a variable root

    print(root.attrib)  # You can check the attributes of every element this way
    print(root.text)  # Likewise, the "text" attribute gives you the text inside an element; root has no text, as you can see everything is in the elements instead

    tree = etree.ElementTree(root)  # This is a snippet of code I found online to print the structure of the tree; you first recreate a tree from the root
    for el in root.iter():  # Then you iterate all elements/descendants starting from the root with the "iter" method (more about it below)
        path = tree.getpath(el)  # You obtain the full path to that element, which is something that starts with the root ("Document") and ends with the element
        path = path.replace('/', '    ')  # Replacing slashes by a space
        spaces = Counter(path)  # Counting the number of spaces, to know how deep in the structure the element is
        tag_name = el.tag  # Obtain the element's name (called tag in xml, but name in html)
        result = ' ' * (spaces[' '] ) + tag_name  # We then use the number of spaces we got up to add spaces before the tag name - recreating a tree
        print(result)

    for child in root:  # The parent element also works as a list of its children element, so you can easily iterate over it immediately like this
        print(child.tag)

    for paragraph in root.iter("p"):  # Though a better way to do it is with iter(); this command takes arguments that allow you to filter the descendants
        print(etree.tostring(paragraph, encoding="unicode"))  # You can also turn any element into a string and see as normal text

    for el in root.iter(["Numero_Dossier", "Date_Lecture"]):  # The filter can also be a list of relevant element namess
        print(el.text)

    prev_el = el.getprevious() # These methods (and others) allow you to jump from one element to another; sometimes if you can't find one element or are not sure of its name, you can rely on another element and make the necessary jumps
    next_el = el.getnext()

    for el in root.iter("Date_Lecture"):  # We next look for the Date element, which is called Date_Lecture; easiest way in XML is to filter all descendants to get only the one we are interesting in, here
        date = el

    parsed_date = datetime.strptime(date.text, "%Y-%m-%d")  # Introducing datetime elements ! The function strptime allows you to read a text (first argument), and if it matches the pattern in second argument, you will create a datetime object (parsed_date here).
    full_date = parsed_date.strftime("%A %d %B %Y")  # Your datetime object can then be transforme (strftime) into a more pleasant date format, again using a pattern
    date.set("date", full_date)  # And this is how you set new attributes into an element

    el_to_remove = root.xpath(".//Numero_Role")[0]  # Looking for an element to remove, we'll explain xPath below
    el_to_remove.getparent().remove(el_to_remove) # Finally, let's say you want to remove an element, you can do it by finding the parent element and using "remove", passing the element to remove as argument

    xml_file.write(file)   # And finally you can save it like this

    new_date_el = root.xpath(".//Date_Lecture[@date='" + full_date + "']")  # Notice that this works here only because we set the "full_date" attribute at an earlier stage

details = ["Numero_Dossier", "Date_Lecture", "Date_Audience", "Avocat_Requerant", "Type_Decision", "Type_Recours",
"Formation_Jugement"]
lists_details = []  # Easiest way to create a dataframe is first to have a list of lists, and then pass it to pd.Dataframe(lists, columns=details)

for file in files:
    newlist = []  # We create a new, empty list, every time we switch to a new file; that list will be filled with relevant data and added to main list
    XML = etree.parse(file)
    root = XML.getroot()

    for detail in details:  # For each file, we iterate over each type of detail, using a loop
        result = ""
        for el in root.iter(detail):  # and we use this detail to filter from all descendants in root
            result = el.text
        newlist.append(result)  # we then pass the result to the list created above

    lists_details.append(newlist)  # Before the loop concludes with one file and passes on to the next, we append the (filled) newlist to main list

df = pd.DataFrame(lists_details, columns = details)  # Out of the loop, we create a dataframe based on that list of lists
df.to_clipboard(index=False) # Finally, we copy the DataFrame so as to paste it (CTRL+V) in Excel
