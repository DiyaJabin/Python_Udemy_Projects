#--------IMPORTS-------
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv
import os

load_dotenv()

#---------CONSTANTS-------
GFORM_LINK =os.getenv("GFORM_LINK")

#--------SCRAPE NECESSARY DATA-----------
response = requests.get("https://appbrewery.github.io/Zillow-Clone/?")
code = response.text
soup = BeautifulSoup(code,'html.parser')
# print(soup.prettify())
all_listings = soup.find_all(name = "a",class_ = "property-card-link")
listings = []
for listing in all_listings:
    listings.append(listing.get("href"))
all_prices = soup.find_all(name = "span", class_ ="PropertyCardWrapper__StyledPriceLine")
prices = []
for price in all_prices:
    if '+' in price.text:
        prices.append(price.text.split('+')[0])
    elif '/' in price.text:
        prices.append(price.text.split('/')[0])
all_addresses = soup.find_all(name = "address")
addresses = []
for address in all_addresses:
    if '|' in address.text:
        formatted_address = address.text.replace('|','')
        addresses.append(formatted_address.strip())
    else:
        addresses.append(address.text.strip())


#---------AUTOMATE FILLING THE GOOGLE FORM-------
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach",True)
driver = webdriver.Chrome(options = chrome_options)
driver.maximize_window()
wait = WebDriverWait(driver,10)

count = len(listings)
index = 0

driver.get(GFORM_LINK)

while count>0:
    address_input = wait.until(EC.element_to_be_clickable((By.XPATH,"//input[@aria-labelledby = 'i1 i4']")))
    address_input.send_keys(addresses[index])

    prices_input = wait.until(EC.element_to_be_clickable((By.XPATH,"//input[@aria-labelledby = 'i6 i9']")))
    prices_input.send_keys(prices[index])

    link_input = wait.until(EC.element_to_be_clickable((By.XPATH,"//input[@aria-labelledby = 'i11 i14']")))
    link_input.send_keys(listings[index])

    submit_button = wait.until(EC.element_to_be_clickable((By.XPATH,"//div[@role = 'button']")))
    submit_button.click()

    submit_another_response = wait.until(EC.element_to_be_clickable((By.XPATH,"//a[contains(@href,'form_confirm')]")))
    submit_another_response.click()


    index+=1
    count-=1


