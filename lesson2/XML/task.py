# 3
import pandas as pd
from lxml import etree  # This is one of the main .xml reader module in Python
import os
from datetime import datetime
from collections import defaultdict, Counter

os.chdir("./lesson2/XML/Not so gibberish")  # We go to the main folder

for file in os.listdir("."):
    xml_file = etree.parse(file)  # We first open
    root = xml_file.getroot()

    print(root.attrib)  # You can check the attributes of every element

    tree = etree.ElementTree(root)  # This is a snippet of code I found on the internet to print the structure of the treee
    for tag in root.iter():
        path = tree.getpath(tag)
        path = path.replace('/', '    ')
        spaces = Counter(path)
        tag_name = path.split()[-1].split('[')[0]
        tag_name = ' ' * (spaces[' '] - 4) + tag_name
        print(tag_name)

    for child in root:  # The parent element also works as a list of its children element, so you can easily iterate over it
        print(child.tag)


    for paragraph in root.iter("p"):
        print(etree.tostring(paragraph, encoding="unicode"))  # You can also turn any element into a string and see as normal text

    paragraph.getprevious()
    paragraph.getnext()

    for el in root.iter("Date_Lecture"):  # We next look for the Date element, which is called Date_Lecture; we iterate over all elements that match that term, and assign it
        date = el

    parsed_date = datetime.strptime(date.text, "%Y-%m-%d")  # Introducing datetime elements !
    full_date = parsed_date.strftime("%A %d %B %Y")  # Transforming into a more pleasant date format
    date.set("date", full_date)  # And this is how you set new attributes into an element

    el_to_remove = root.xpath(".//Numero_Role")[0]
    el_to_remove.getparent().remove(el_to_remove) # Finally, let's say you want to remove an element, you can do it by finding the parent element and using "remove"

    xml_file.write(file)   # And finally you can save it like this

    new_date_el = root.xpath(".//Date_Lecture[@date='" + full_date + "']")  #  xpath method Returns a list, be careful about this ! If you are sure there is an element that matches you search, you can just use xPath expressions in .find()

details = ["Numero_Dossier", "Date_Lecture", "Date_Audience", "Avocat_Requerant", "Type_Decision", "Type_Recours",
"Formation_Jugement"]
lists = []  # Easiest way to create a dataframe is first to have a list of lists, and then pass it to pd.Dataframe(lists, columns=details)

for file in os.listdir("."):
    sub_list = []
    xml_file = etree.parse(file)  # We first open
    root = xml_file.getroot()
    for el in details:
        el_in_doc = root.xpath(".//" + el)
        if len(el_in_doc):
            sub_list.append(el_in_doc[0].text)
        else:
            sub_list.append("")
    lists.append(sub_list)

df = pd.DataFrame(lists, columns=details)

days = []
for date in df["Date_Audience"].values.tolist():
    if date != "":
        parsed_date = datetime.strptime(date, "%Y-%m-%d")
        days.append(parsed_date.strftime("%A"))

Counter(days).most_common()
