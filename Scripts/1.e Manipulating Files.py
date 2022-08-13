import os

current_path = os.getcwd()
print(current_path)

print(os.listdir("."))  # We check what files are in the folder
file = "./Data/Empty File is Empty.txt"  # We select a file that is in the folder Data and attribute its name to a variable
newnamefile = file + "a"  # We decide on a new name given a file
os.rename(file, newnamefile)
os.rename(newnamefile, newnamefile[:-1])

# 5

f = open("poem.txt", encoding="latin1")
poem = f.read()
print(poem)
f.close()

with open("poem2.txt", "a", encoding="utf8") as f:
    f.write(poem)


# 7

import PyPDF2 as PDF  # It's a third-party module, so you may have to install first with "pip install pypdf2"

pdf = PDF.PdfFileReader("./Data/Example.pdf")  # We open the .pdf file found in the Data folder!
num_pages = pdf.getNumPages()
text = ""
for page in range(0, num_pages):
    text += pdf.getPage(page).extractText()  # You need to loop over the number of pages to extract the whole text

print(text)  # Printed text is not great (page number appears, words are cut, URLs are not captured)

# Exercises
