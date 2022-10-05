import requests  # Scraping module
from bs4 import BeautifulSoup  # HTML reading module
import regex as re

webpage = requests.get("https://www.hec.edu/fr/grande-ecole-masters/ms-et-msc/ms/llm-droit-et-management-international/programme")  # We fetch the webpage and pass it to an object
print(webpage.status_code)  # The webpage object comes with distinct methods, such as status code, which tells you if connection was successful: 404 means no
soup = BeautifulSoup(webpage.content)  # We then read the html (which is put as a string in webpage.content) with BeautifulSoup, and pass it to an object we'll call "soup"
prix_ao = soup.find(title="Prix Juridique et Fiscal Allen & Overy")  # Using that soup object, we look for an element whose title matches the one we are looking for - and we pass it to yet another element
content = prix_ao.parent.parent.text  # Next, we can use this element to get the element we are actually interested in, which here is the text of the grandparent (.parent.parent)
print(content)

# Now turning to the Conseil Constitutionnel

webpage = requests.get("https://www.conseil-constitutionnel.fr/le-bloc-de-constitutionnalite/texte-integral-de-la-constitution-du-4-octobre-1958-en-vigueur")  # Same logic, we first get the page
soup = BeautifulSoup(webpage.content)  # Then create a soup

cons_div = soup.find("div", class_="field field--name-field-reference-paragraph field--type-entity-reference-revisions field--label-hidden field__items")  # We look for the main element containing the entire constitution. Note that, by contrast with all other attributes, "class" needs to have an underscore at the end ("class_"); this is because "class" already means something in native python

for child in cons_div.findChildren("h3"):  # Looking for titles; note that all 'find' methods in Beautifulsoup work from the point of view of the element you use it on
    print(child)

dic_constitution = {}
for child in cons_div.findChildren("h3"):  # We go over every article
    text = ""  # We create an empty variable to fill with the text
    article_num = re.search(r"\d+(-\d+)?|PREMIER", child.text).group()  # We get the article number from regex; notice that some numbers are of the form \d+-\d (e.g., Article 88-2), so we provide for this; the first article is also an exception
    for sib in child.find_all_next(["h3", "p"]):  # We iterate over the next elements
        if sib.name == "h3":  # We check if we have  reached the next article, in which case we  break the loop
            break
        else:  # If we have not reached the next article, we add the text to our variable, separated  by a line-break
            text += "\n" + sib.text.strip()  # Strip because online text often has empty strings at the end and beginning of text
    dic_constitution[article_num] = text.strip()  # Once the loop over the text elements is over, we input it in our dictionary

# Exercise - Two solutions

section_with_most_arts = ""
prev_count = 0 # We initiatlise counter to keep track of what's the highest number of articles

for child in cons_div.findChildren("h2"):   # First we notice that all "Titres" are put in h2 elements
    count = 0  # We initialise a counter
    prev = ""  # We initialise an article number (see below)
    for sib in child.find_all_next(["h2", "h3"]):  # Same logic as above: we iterate over the relevant sections, and break the loop if we encounter another h2 element - which means we reached next title
        if sib.name == "h2":
            break
        else:
            article_num = re.search(r"\d+|PREMIER", child.text).group()   # Since subarticles count as one, we need to keep track of what article we are in - so same regex as above, except we don't care about second part
            if article_num != prev:  # We then check that we are in a different article; if we are not (e.g., we passed from 88-2 to 88-3, nothing happens
                count += 1  # If yes, we increase counter
                prev = article_num  # And now the previous article will become the current article, relevant for next element in loop
    if count > prev_count:  # After all children have been counted, we compare with what, so far, is the highest numnber - if it beats it, it replaces it
        section_with_most_arts = child.text
        prev_count = count


print(section_with_most_arts)

# Second solution: There is a trick, you can use the summary on the left pane, which puts all articles in parent elements "li"
section_with_most_arts = ""
prev_count = 0  # We initialise counter to keep track of what's the highest number of articles
for el in soup.find_all("a", class_="h2"):  # We notice that, in the summary, all titles are put in "a" elements with class "h2"
    parent = el.parent  # We look for the parent element that contains a list of all articles
    count = len(parent.findAll("a"))  # We count these articles (they are all in "a" elements)
    if len(parent.findAll("a")) > prev_count:  # We compare with the highest number so far
        section_with_most_arts = el.text
        prev_count = count
