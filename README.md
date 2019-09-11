# IMDb Web Scraper
IMDb Web Scraper - as the name suggests - is a web scraper that goes through the IMDb website and creates a CSV spreadsheet with movies and television shows and all of their relevant information.

# How does it work?
Through a series of inputs, the program creates filters that are found in the URL of the IMDb website. Once all the filters have been determined, the program downloads a copy of the HTML code of that specific URL and searches through it for every movie and/or television show on the page and adds the title and all of its relevant information into a CSV spreadsheet. It continues to do this until all the results for the filters have been exhausted on the website or until the spreadsheet contains 10,000 items.

# Why should I use this?
This program is designed with data scientists and machine learning in mind as the spreadsheet that is generated can be used for analysis and to discover common trends among various types of programming as well as for creating powerful machine learning models that can extend beyond the use of just this one spreadsheet.

# Installation
1. Download and install the latest version of <a href='https://www.python.org/downloads/'>Python</a> if you do not already have it installed
2. Open up your Command Terminal (as Administrator on Windows) and enter <code>pip install bs4</code>
3. Clone the project repository
4. <code>cd</code> into the project directory
5. Enter <code>python imdb_web_scraper.py</code> to initialize the program

# Dependencies
<a href='https://pypi.org/project/bs4/'>Beautiful Soup</a>
