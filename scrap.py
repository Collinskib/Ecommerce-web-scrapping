import requests_html
from requests_html import HTMLSession, AsyncHTMLSession
from bs4 import BeautifulSoup
from time import sleep
from random import uniform
import pandas as pd

session = HTMLSession()


def parse_data(url):
    name = []
    types = []
    prices = []
    discounts = []
    reviews = []
    links = []

    resp = session.get(url)
    resp_html = resp.html.render(sleep=1, keep_page=True, scrolldown=5)
    resp_html = resp.html.html
    soup = BeautifulSoup(resp_html, 'lxml')
    product_body = soup.find_all('div', class_='el-col-6')
    for product in product_body:
        link = product.find('a', class_='showHand').get_text().strip()
        prod_name = product.find('div', class_='wordwrap').div.get_text().strip()
        price = product.find('div', class_='wordwrap-price').get_text().strip()
        discount = product.find('span', class_='greenbox').get_text().strip()
        review = product.find('span', class_='twoksh').get_text().strip()

        name.append(prod_name)
        links.append(link)
        prices.append(price)
        reviews.append(review)
        discounts.append(discount)

    df = pd.DataFrame({'Product Name': name, 'Product Link': links,
                       'Price': prices, 'Reviews': reviews,
                       'Discounts': discounts})
    df.to_csv('Kilimall shoes.csv', index=False)
    print(df.head(5))


parse_data('https://www.kilimall.co.ke/new/commoditysearch?q=shoes')  # you can change the link