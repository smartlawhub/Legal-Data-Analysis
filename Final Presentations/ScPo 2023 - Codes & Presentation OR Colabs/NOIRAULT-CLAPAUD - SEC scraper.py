import time
import re
import pandas as pd
from selenium import webdriver
from datetime import datetime 
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from selenium.common.exceptions import StaleElementReferenceException

def click_s1_links(driver):
    # Create an empty list to store the results
    results = []
    num_pages = 9  # Set the number of pages to scrape

    for page in range(num_pages):
        s1_links = driver.find_elements(By.XPATH, "//a[contains(@href, 's1.htm')]")

        # Iterate through the found links and click on each of them
        for link in s1_links:
            # Extract the href attribute from the link
            href = link.get_attribute("href")
            print(f"Opening link: {href}")

            # Click on the link using JavaScript
            driver.execute_script("arguments[0].click();", link)

            try:
                driver.execute_script("arguments[0].click();", link)
            except StaleElementReferenceException:
        # If a StaleElementReferenceException occurs, re-find the element and click it again
                link = driver.find_element(By.XPATH, "//a[contains(@href, 's1.htm')]")
                driver.execute_script("arguments[0].click();", link)

            # Wait for the modal to appear and handle it
            try:
                WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "previewer")))

                # Handle the modal by sending ESC key, assuming it's a dismissible overlay
                driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.ESCAPE)
            except Exception as e:
                print(f"Error handling modal: {e}")

            # Add a delay to give time for the page to load or handle any pop-ups
            time.sleep(6)

            # Switch to the iframe
            try:
                iframe = driver.find_element(By.ID, "ipreviewer")  # Replace "ipreviewer" with the actual iframe ID
                driver.switch_to.frame(iframe)
                print("Switched to iframe")

                # Extract the HTML content of the iframe
                iframe_html = driver.page_source

                # Use BeautifulSoup to parse the HTML content with case-insensitive search
                iframe_soup = BeautifulSoup(iframe_html, 'html.parser')

                # Define the regex pattern to find percentages based on specified phrases
                regex_pattern = re.compile(r'\b((initial\s+(?:shareholder[s]*|stockholder[s]*|Sponsors)\s*(?:\S\s*){0,70}(?:will\s+(?:collectively\s+)?(?:beneficially\s+)?own|will\s+own)\s*(\d[\d,.]*)\s*%))', flags=re.IGNORECASE)

                # Use regex to find percentages in the iframe_text
                matches = regex_pattern.findall(str(iframe_soup))

                if matches:
                    # Extract the percentage from the match
                    percentage = matches[0][2]
                    print(f"Found match: {percentage}")

                    # Locate the phrase with the units and price per unit information
                    text = iframe_soup.get_text()
                    units_pattern = re.compile(r'Securities\s+offered[^$]*?([\d,]+)\s*units[^$]*\$\s*([\d,.]+)\s*per\s*unit')
                    units_match = units_pattern.search(text)

                    if units_match:
                        units, price_per_unit = units_match.groups()
                        print(f"Units: {units}, Price per unit: {price_per_unit}")


                        #html_content = '<span class="modal-file-name">S-1 (Registration statement) of filed (2021-02-26)</span>'
                        text = iframe_soup.get_text()
                        date_pattern = re.compile(r'on (\w+\s+\d{1,2},\s+\d{4})')
                        date_match = date_pattern.search(text)

                        if date_match:
                            extracted_date = date_match.group(0)
                            print(f"Extracted Date: {extracted_date}")

                            # Append the results to the list
                            results.append({'Date': extracted_date, 'Percentage': percentage, 'Units': units, 'Price Per Unit': price_per_unit})
                        else:
                            print("Date information not found.")
                    else:
                        print("Units information not found.")
                else:
                    print("No matches found.")

                # Switch back to the default content
                driver.switch_to.default_content()
                print("Switched back to default content")
            except StaleElementReferenceException:
                print("StaleElementReferenceException: Trying to find iframe element again.")
                continue
            except Exception as e:
                print(f"Error switching to iframe: {e}")

        if page < num_pages - 1:
            try:
                next_page_link = driver.find_element(By.XPATH, "//a[@data-value='nextPage' and text()='Next page']")
                driver.execute_script("arguments[0].click();", next_page_link)
                print(f"Switching to Page {page + 2}")
                time.sleep(6)
            except Exception as e:
                print(f"Error clicking Next page link: {e}")
                break

    # Create a DataFrame from the list of results
    df = pd.DataFrame(results)

    if not df.empty:
        df['Date'] = pd.to_datetime(df['Date'])
        df = df.sort_values(by='Date')

# Reordering columns and creating 'Date SPAC' column
        df = df[['Date', 'Percentage', 'Units', 'Price Per Unit']]
        df['Date SPAC'] = df['Date'].dt.strftime('%d/%m/%Y')

# Converting 'Units' and 'Price Per Unit' to numeric
        df['Units'] = pd.to_numeric(df['Units'].str.replace(',', ''), errors='coerce')
        df['Price Per Unit'] = pd.to_numeric(df['Price Per Unit'].str.replace(',', ''), errors='coerce')

# Calculating 'SPAC size' and cumulative 'Total SPAC amount' in millions
        df['SPAC size'] = (df['Units'] * df['Price Per Unit']) / 1000000
        df['Total SPAC amount'] = df['SPAC size'].cumsum()

# Adding an 'ID' column and calculating 'Nombre de SPAC'
        df['ID'] = 1

        for test_nbr, row in df.iterrows():
          SPAC = row["SPAC size"]

          if SPAC > 0:
              df.at[test_nbr, 'ID'] = 1

          else:
              df.at[test_nbr, 'ID'] = 0
        
        df['Nombre de SPAC'] = df['ID'].cumsum()

        df['Mean SPAC size'] = df['Total SPAC amount'] / df['Nombre de SPAC']
        df['Mean SPAC size'] = df['Mean SPAC size'].round(1)

# Dropping the original 'Date' column
        df.drop(columns=['Date'], inplace=True)

# Reordering columns for the final output
        df = df[['Date SPAC', 'Percentage', 'SPAC size', 'Mean SPAC size']]

# Displaying the resulting DataFrame
        print(df)
        df.head(25)

        import matplotlib.pyplot as plt



        # Displaying the resulting DataFrame
        print(df)

        # Print mean, median, and standard deviation of SPAC size
        mean_spac_size = df['Mean SPAC size'].mean()
        median_spac_size = df['Mean SPAC size'].median()
        std_dev_spac_size = df['Mean SPAC size'].std()

        print(f"Mean SPAC size: {mean_spac_size}")
        print(f"Median SPAC size: {median_spac_size}")
        print(f"Standard Deviation of SPAC size: {std_dev_spac_size}")

        # Convert 'Date SPAC' to datetime type
        df['Date SPAC'] = pd.to_datetime(df['Date SPAC'], format='%d/%m/%Y')

        # Compute the number of SPACs per year
        spacs_per_year = df.groupby(df['Date SPAC'].dt.year)['Date SPAC'].count()

        # ... (previous code)

        # Plotting Figure 1: Evolution of Mean SPAC size
        plt.figure(figsize=(10, 6))
        plt.plot(df['Date SPAC'], df['Mean SPAC size'], marker='o')
        plt.title('Evolution of Mean SPAC Size Over Time')
        plt.xlabel('Date')
        plt.ylabel('Mean SPAC Size')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show(block=False)

        # Plotting Figure 2: Number of SPACs per Year
        plt.figure(figsize=(10, 6))
        plt.plot(spacs_per_year.index, spacs_per_year.values, marker='o')
        plt.title('Number of SPACs per Year')
        plt.xlabel('Year')
        plt.ylabel('Number of SPACs')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show(block=False)

        # Plotting Figure 3: Mean SPAC size per Year
        plt.figure(figsize=(10, 6))
        plt.plot(df['Date SPAC'], df['Mean SPAC size'], marker='o')
        plt.title('Mean SPAC Size per Year')
        plt.xlabel('Date')
        plt.ylabel('Mean SPAC Size')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

# Create a new instance of the Chrome driver
driver = webdriver.Chrome()

# URL of the SEC page
url = 'https://www.sec.gov/edgar/search/#/q=%2522special%2520purpose%2520acquisition%2520company%2522&category=form-cat5&filter_forms=S-1'
driver.get(url)

# Add a delay after opening the SEC website
time.sleep(7)

# Call the function to click on links with "s1.htm" in the href attribute
click_s1_links(driver)





