from bs4 import BeautifulSoup
import requests
import smtplib
import os
from dotenv import load_dotenv

#-------CONSTANTS-------#
load_dotenv()
TARGET_PRICE = 100
MESSAGE = "Price of item is now below target price.Buy Now!!!"
SMTP_ADDRESS = os.getenv("SMTP_ADDRESS")
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
HEADER = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36",
    "Accept-Encoding":"gzip, deflate, br, zstd",
    "Accept-Language":"en-AU,en-GB;q=0.9,en-US;q=0.8,en;q=0.7,ml;q=0.6",
}
    # ----MAIN CODE---#

response = requests.get("https://appbrewery.github.io/instant_pot/",headers=HEADER)
content = response.text
soup = BeautifulSoup(content,"html.parser")
block = soup.find("span",class_ = "a-price aok-align-center reinventPricePriceToPayMargin priceToPay")
price = float(block.text.split("$")[1])
print(price)


if price<=TARGET_PRICE:
    with smtplib.SMTP(SMTP_ADDRESS,587) as server:
        server.starttls()
        server.login(EMAIL_ADDRESS,EMAIL_PASSWORD)
        server.sendmail(EMAIL_ADDRESS,EMAIL_ADDRESS,MESSAGE)
        print("Email Sent!")