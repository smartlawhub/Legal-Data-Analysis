# Dates and xPath

Before turning to scraping, two important points that fit nowhere else. For both, we will use a decision from the Conseil d'Etat (see previous lesson on .xml).

## xPath

We saw how to locate an element by filtering all children from the root with the <code>.iter()</code> method. Yet, this is not the easiest way to locate an element when you really need it. Instead, you need to use yet another syntax, called xpath. You can read more about xPath 
<a href="https://www.w3schools.com/xml/xpath_syntax.asp">here</a>. It works like this:

<ul><li>You first identify where to find the required element. You typically start from the source element 
(represented by a dot <code>.</code>), then use one slash if you want to search in the immediate children, or two slashes 
(<code>//</code>) if you need to search in the entire tree;</li>
    <li>Then you specify the name of the element, or <code>*</code> if any would do;</li>
    <li>And then you add conditions, in brackets, such as the value of an attribute (introduced by a <code>@</code>),
or based on other functions (such as whether the element contains a certain text);</li>
<li>You can also directly looked for all "x" elements (will return a list of those);</li>
    <li>Finally, xpath comes with a number of functions, such as <code>contains()</code> (allows you to check that 
the object contains a certain text);</li>
    </ul>

For instance, if we needed to find the element `Date_Lecture` in the xml_file, this is what the xPath expression 
would look like: `root.xpath(".//Date_Lecture") `.

Xpath method Returns a list, be careful about this ! If you expect only one element, you can immediately index it, as below.


```python
import os
from lxml import etree

os.chdir("../Data/CE")  # We move to the relevant folder, if needed
file = os.listdir(".")[0] # We take the first file from the CE folder

xml_file = etree.parse(file)  # We first open the .xml file with the "parse" method
root = xml_file.getroot()  # We then look for the "root" of the XML tree, and pass it to a variable root

numero_dossier = root.xpath(".//Numero_Dossier")[0]  # We search for the element Numero Dossier starting from the root
# (which is the "." here)
print("Le numéro de dossier est: ", numero_dossier.text)

paras = root.xpath(".//*[contains(text(), 'Article')]")  # Looking for all elements whose text contains the term "Article"
for para in paras:  # We can loop since xPath always returns a list!
    print(para.text)
```

    Le numéro de dossier est:  461328
    Article 1er : Le pourvoi de Erreur ! Aucune variable de document fournie. n'est pas admis.
    Article 2 : La présente décision sera notifiée à  et à la Chambre De Commerce Et D'industrie Lyon Métropole Saint-etienne RoanneCopie en sera adressée à la chambre de commerce et d'industrie Lyon Métropole Saint-Etienne Roanne.


## Dates

Python has a data format called datetime, which deals with dates. Dates can be text; in some cases, they can be 
numbers (e.g., a year); but they are most useful when they are of the type "datetime", since they then come with useful methods.

To transform a text into a datetime object, you need to parse it. The datetime module has a function <code>strptime</code> that detects time according to a pattern. You can look for days, months, quarters, minutes, etc. For instance, the symbol "%Y" means the full year written as four consecutive digits (e.g., in regex, \d\d\d\d). The full syntax is available <a href="https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes">here</a>.

Once you have that datetime object, you can act on it, for instance extract the month in the attributes.


```python
from datetime import datetime # The relevant module in the package datetime is also called datetime ... 

print(datetime.today())  # datetime knows what date it is today

date = root.xpath(".//Date_Lecture")[0] # We get the date of our decision
print(date.text)

parsed_date = datetime.strptime(date.text, "%Y-%m-%d")  # The function strptime allows you to read a text (first argument), 
# and if it matches the pattern in second argument, you will create a datetime object (parsed_date here).
print(parsed_date.day)  # The day attribute knows the day number (in the week); today is Friday so 5
```

    2023-01-20 19:14:07.280923
    2022-12-05
    5


But more importantly, datetime objects allow you to reformat a date according to your needs - again, using a pattern.


```python
full_date = parsed_date.strftime("%A %d %B %Y")  # Your datetime object can then be transforme (strftime) into a more 
# pleasant date format, again using a pattern. Note that datetime know what day of the week that date was !
print(full_date)

date.set("date", full_date)  # Let's add the full date as an attribute to our date element

new_date_el = root.xpath(".//Date_Lecture[@date='" + full_date + "']")[0]  # And now we can use xPath to find this element 
# with the attribute (which we just added)
print("The element's attribute date: ", new_date_el.get("date"))
```

    Monday 05 December 2022
    The element's attribute date:  Monday 05 December 2022

