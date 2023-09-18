import requests
from bs4 import BeautifulSoup
import smtplib
import os

EMAIL = os.getenv('SMTP_EMAIL')
PASSWORD = os.getenv('SMTP_PASSWORD')
RECEIVER_EMAIL = os.getenv('TEST_EMAIL')
URL = ("https://www.clarosa.fr/collections/clarosa-talons/products/sandales-en-suedine-vert-pastel"
       "-avec-bride-croisee-a-la-cheville-a-talons")
NORMAL_PRICE = 39.99
response = requests.get(URL)

soup = BeautifulSoup(response.content, "lxml")
title = soup.find(class_="product-single__title").get_text().strip()
print(title)
price = soup.find(class_="price-item").getText()
price = price.strip()
x = price.split("€")[0]
new_x = x.replace(',', '.')
new_price = float(new_x)
print(new_price)

# send an email when the price of the sandales is less than 15
if new_price < NORMAL_PRICE:
    message = f"{title} is now {price}"
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        # server.starttls()
        server.login(user=EMAIL, password=PASSWORD)
        server.sendmail(
            from_addr=EMAIL,
            to_addrs=RECEIVER_EMAIL,
            msg=f"Subject:Clarosa Price Alert!\n\n{message}\n{URL}".encode("utf-8")
        )
