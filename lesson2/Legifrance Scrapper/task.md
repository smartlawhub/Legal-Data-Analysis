# Legifrance Scraper   

This is a scraper I designed in a project to get every historical version of an article from the codes available on 
Legifrance. Everything is commented; remember that we use Inspecting tools in Google to know where to look for 
special data (e.g., what is the "class" of the element that has relevant data). 

There are several exception handlers of the form `try: except:`, because experience taught me these were frequent 
errors (and that makes your script stop if you don't have an handler). It's entirely possible there are easier ways 
to scrap that data, it's just the one I came up with.

Result is a dataframe with one row per version of an article. Can take time to collect all the data, because you 
need to load a lot of pages with Selenium.

(Note that it might be easier and quicker to use Legifrance's API, but I've never tried so far.)
