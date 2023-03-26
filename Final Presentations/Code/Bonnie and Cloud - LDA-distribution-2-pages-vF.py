import requests
import PyPDF2
import re
import pandas as pd
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup

# Initialize all required lists
decision_page_links = []
pdf_page_links = []
sanction_list = []
date_list = []
pdf_list = []
transaction_list = []

# Loop to get all of the 124 search pages from the ADLC's website (upper bound must be 125 instead of 124)
for search_page_number in range(1, 125):
    # Reset base search page URL each time
    base_url = "https://www.autoritedelaconcurrence.fr/fr/liste-des-decisions-et-avis?search_api_fulltext=&field_precautionary_measure=0&created%5Bmin%5D=&created%5Bmax%5D=&sort_by=created&page="
    # Build search page URL based on observed syntax
    base_url = base_url + str(search_page_number)
    search_page_response = requests.get(base_url)
    # Only move forward with extraction if the first request (for each of the 124 search pages) has succeeded
    if search_page_response.status_code == 200:
        print("First level request (search page " + str(search_page_number) + ") successful")
        # Use BeautifulSoup to read the search page's HTML code
        search_page_html_content = search_page_response.text
        search_page_soup = BeautifulSoup(search_page_html_content, "html.parser")
        # Find all the links in the search page's HTML code using the 'a' tag
        unfiltered_search_page_links = search_page_soup.find_all("a")
        decision_page_links = []
        for link in unfiltered_search_page_links:
            # Exclude from the links all those whose URL do not follow the syntax used for "décisions" (e.g. "avis")
            if str(link)[:21] == '<a href="/fr/decision':
                # Extract the 'href' attribute from each link
                decision_page_links = decision_page_links + [link.get("href")]
                print("Next decision page link found on search page " + str(search_page_number) + " is " + str(link.get("href")))
        if decision_page_links == []:
            print("Could not find any decision links on search page number " + str(search_page_number))
        else:
            print("All decision page links found on search page " + str(search_page_number) + " were added to a list")
        for decision_page_link in decision_page_links:
            # Reset base decision page URL each time
            decision_page_url = "https://www.autoritedelaconcurrence.fr/" + decision_page_link
            decision_page_response = requests.get(decision_page_url)
            if decision_page_response.status_code == 200:
                print("Second level request (individual decision page " + decision_page_link + ") successful")
                decision_page_html_content = decision_page_response.text
                decision_page_soup = BeautifulSoup(decision_page_html_content, "html.parser")
                # Find all the links in the HTML using the 'a' tag
                unfiltered_decision_page_links = decision_page_soup.find_all("a")
                pdf_page_links = []
                # Note: add filter for transaction
                for link in unfiltered_decision_page_links:
                    # Exclude from the links all those whose URL do not follow the syntax used for decision PDF files
                    if str(link)[:32] == '<a aria-label="le texte intégral':
                    # Extract the 'href' attribute from each link
                        pdf_page_links = pdf_page_links + [link.get("href")]
                        print("PDF link found on this page is " + str(link.get("href")))
                if pdf_page_links == []:
                    print("Could not find any PDF link on decision page " + str(decision_page_link))
                else:
                    print("Finished listing PDF links on " + str(decision_page_link))
                for pdf_link in pdf_page_links:
                    # Missing EOF marker in the following link
                    if pdf_link != "https://www.autoritedelaconcurrence.fr/sites/default/files/commitments//93d29.doc":
                        pdf_file_response = requests.get(pdf_link)
                        if pdf_file_response.status_code == 200:
                            print("Third level request (PDF file) successful")
                            # Download the file and name it Current_Extract
                            with open("Current_Extract.pdf", "wb") as f:
                                f.write(pdf_file_response.content)
                                pdf_file = open("Current_Extract.pdf", "rb")
                                pdf_reader = PyPDF2.PdfReader(pdf_file)
                            # Reset the text for each new PDF file
                            text = ""
                            # Reading only the last 2 pages as searching on all pages would significantly decrease speed
                            for page in (len(pdf_reader.pages)-2, len(pdf_reader.pages)-1):
                                text += pdf_reader.pages[page].extract_text()
                            # Use regex to search for "distribution" in the decision's PDF file's text
                            legal_basis = re.search(r"distribution", text)
                            if legal_basis:
                                # Use regex to search for sanction patterns in the decision's PDF file's text
                                sanction_pattern_1 = re.search(r"une sanction de (\d+(?:\s+\d+)*)", text)
                                sanction_pattern_2 = re.search(r"une sanction pécuniaire de (\d+(?:\s+\d+)*)", text)
                                # For each possible sanction pattern, retrieve the fine, date and PDF link
                                if sanction_pattern_1:
                                    sanction_text = sanction_pattern_1.group().split("de")[1].strip()
                                    sanction = str(sanction_text)
                                    sanction_list = sanction_list + [sanction]
                                    print("Sanction found with value: ", sanction)
                                    date_text = str(pdf_link)[-9:][:2]
                                    date_list = date_list + [date_text]
                                    pdf_list = pdf_list + [str(pdf_link)]
                                    # Identify bargains
                                    transaction_boolean = re.search(r"Transaction", decision_page_html_content)
                                    if transaction_boolean:
                                        transaction_list = transaction_list + ["Bargain"]
                                    else:
                                        transaction_list = transaction_list + ["Other"]
                                elif sanction_pattern_2:
                                    sanction_text = sanction_pattern_2.group().split("de")[1].strip()
                                    sanction = str(sanction_text)
                                    sanction_list = sanction_list + [sanction]
                                    print("Sanction found with value: ", sanction)
                                    date_text = str(pdf_link)[-9:][:2]
                                    date_list = date_list + [date_text]
                                    pdf_list = pdf_list + [str(pdf_link)]
                                    # Identify bargains
                                    transaction_boolean = re.search(r"Transaction", decision_page_html_content)
                                    if transaction_boolean:
                                        transaction_list = transaction_list + ["Bargain"]
                                    else:
                                        transaction_list = transaction_list + ["Other"]
                                else:
                                    # If no sanction was found, register the sanction as null
                                    sanction = "0"
                                    sanction_list = sanction_list + [sanction]
                                    print("No sanction value found")
                                    date_text = str(pdf_link)[-9:][:2]
                                    date_list = date_list + [date_text]
                                    pdf_list = pdf_list + [str(pdf_link)]
                                    # Identify bargains
                                    transaction_boolean = re.search(r"Transaction", decision_page_html_content)
                                    if transaction_boolean:
                                        transaction_list = transaction_list + ["Bargain"]
                                    else:
                                        transaction_list = transaction_list + ["Other"]
                            else:
                                print("The PDF file does not contain the desired legal basis")
                            # Close this decision's PDF file now that we are done with it
                            pdf_file.close()
                    else:
                        # Warn the user that the code failed to get to the PDF file and give the file's URL
                        print("Third level request (PDF file) failed for URL " + str(pdf_link))
            else:
                # Warn the user that the code failed to get to the individual decision page and give the page's link
                print("Second level request (individual decision page) failed for page " + str(decision_page_link))   
    else:
        # Warn the user that the code failed to get to the search page and give the page's number
        print("First level request (search page) failed for search page number " + str(search_page_number))
print("Main loop has finished running")
# Put the data in a dataframe
sanction_dataframe = pd.DataFrame({'Sanction': sanction_list, 'Date': date_list, 'Link': pdf_list, 'Type': transaction_list})
# Export the final dataframe to CSV format
sanction_dataframe.to_csv('ADLC_Sanctions.csv')
# Read the final dataframe
sanction_reading = pd.read_csv('ADLC_Sanctions.csv')
# Prepare the decisions by year bar chart
# Use a pattern to drop all abnormal years
pattern = r"([0-2][0-9])"
sanction_reading = sanction_reading[sanction_reading['date'].str.contains(pattern, na=False)]
# Group the rows by year and count the number of occurrences
year_counts = sanction_reading.groupby('date').size()
# Plot the counts as a bar chart
year_counts.plot(kind='bar')
# Add axis labels and a title
plt.xlabel('Year')
plt.ylabel('Number of decisions')
plt.title('Decisions in each year')
plt.show()
# Prepare the decision type pie chart
type_counts = sanction_reading['type'].value_counts()
# Create a pie chart showing the proportion of "Bargain" and "Other" values
type_counts.plot(kind='pie', labels=type_counts.index, autopct='%1.1f%%')
# Add a title to the chart
plt.title('Bargains as a proportion of total decisions')
# Show the chart
plt.show()
# Prepare the fine status pie chart
# Count the number of occurrences of each value in the column of interest
sanction_counts = sanction_reading['sanction'].value_counts()
# Create a new column with a binary indicator for each category
sanction_reading['category'] = sanction_reading['sanction'].apply(lambda x: 'No fine' if x == "0" else 'Fine')
# Count the number of occurrences of each category
category_counts = sanction_reading['category'].value_counts()
# Create a pie chart with two categories
category_counts.plot(kind='pie', labels=category_counts.index, autopct='%1.1f%%')
# Add a title to the chart
plt.title('Proportion of fined and not fined parties')
# Show the chart
plt.show()
