# Grequests - Canoes & Kayaks
# Tutorial from John Watson Rooney

import grequests 
from bs4 import BeautifulSoup
import time
import pandas as pd

def get_urls():
    urls = []
    for x in range(1,11):
        urls.append(f'https://www.canoeandkayakstore.co.uk/collections/activity-recreational-beginner?page={x}')
    return urls

def get_data(urls):
    reqs = [grequests.get(link) for link in urls]
    resp = grequests.map(reqs)
    return resp

'product-grid-item__info'
def parse(resp):
    product_list = []
    for r in resp:
        soup = BeautifulSoup(r.text, 'lxml')
        product = soup.find_all('div', class_='product-grid-item__info')
        for item in product:
            title = item.find_all('a')[0].text.strip()
            price = item.find('span', {'class': 'product-grid-item-price'}).find_all('span')[0].text.strip()
            availability = item.find('span', {'class': 'product-grid-item__info__availability--value'}).text.strip()

            product = {
                'title': title, 
                'price': price, 
                'availability': availability,
            }

            product_list.append(product)
            print('Added:', title)

    return product_list

urls = get_urls()
resp = get_data(urls)
df = pd.DataFrame(parse(resp))
print(df.head())
df.to_csv('Canoes.csv', index=False)
print('Saved items to CSV file')