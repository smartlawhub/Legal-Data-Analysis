# 3

pip install pypdf2  # First you'll have to install it since it's a third-party module
import PyPDF2 as PDF

pdf = PDF.PdfFileReader("181-20211207-PRE-01-00-EN.pdf")  # Be sure to be in the right folder !
num_pages = pdf.getNumPages()
text = ""
for page in range(0, num_pages):
    text += pdf.getPage(page).extractText()  # You need to loop over the number of pages to extract the whole text

print(text)  # Printed text is not great (page number appears, words are cut, URLs are not captured)
