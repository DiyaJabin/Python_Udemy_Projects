\# Day 53 – Data Entry Job Automation



Course project from a Udemy Python course.



This script:

\- Scrapes property listings (address, price, link) from a Zillow-style demo page using `requests` + `BeautifulSoup`

\- Automatically enters the scraped data into a Google Form using Selenium



The Google Form link is stored in a `.env` file for easy configuration.



\## Requirements

\- Python

\- selenium

\- beautifulsoup4

\- requests

\- python-dotenv

\- Google Chrome



\## Setup

Create a `.env` file in the project folder with:



GFORM\_LINK=your\_google\_form\_link\_here



\## Run

pip install selenium beautifulsoup4 requests python-dotenv  

python main.py

