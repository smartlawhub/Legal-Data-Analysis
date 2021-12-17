## Selenium

<b>1. </b>Now turning to dynamic websites : much harder ! Let's try with one to see what's wrong. 

The Conseil d'Etat has a database of decisions, available at : https://www.conseil-etat.fr/ressources/decisions-contentieuses/arianeweb2

However, you can't click on the decision before inputting research terms. And once you do input these terms, the URL 
does not budge - this is not a new page loading, but a truly dynamic webpage reacting to your input by producing 
(server-side) a new output, incorporated in the original website's framework. If we try to get it with requests, you 
can't get the`table` element from the webpage

<b>2. </b>To bypass this issue, you'll need to have someone, or something, click on the right buttons and filling 
the expected input, which`requests` cannot do (or with difficulty). The most straightforward strategy here is to imitate 
what a human would do with a browser, except that it should be done by a robot.

Enters `Selenium`, a package made for this: Selenium will take control of your browser, and allow 
your script to perform just as much as you do.

More accurately, Selenium takes control of a version of your browser: you need to link it with a "webdriver" file. 
This course comes pre-loaded with versions of Chrome for Windows and Mac, but it should also work with Firefox or 
Safari (I understand Mac users can find it at /usr/bin/safaridriver).

<b>3.</b> The main steps are however the same as for scraping with `requests`: you'll need to know how to get to your 
results, and tell the robot/webdriver as much, before collecting the page source and parsing it with BeautifulSoup.

This might require a lot of trial and error, especially when you are required to search something by xPath: what you 
see, even in the robot browser, might be different from what Selenium might see (a good way to make sure the element 
you are looking for is simply to print `driver.page_source` in the Console).
