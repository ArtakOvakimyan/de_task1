import pandas as pd
import json
import pickle


with open('./data/fourth_task_products.json', 'rb') as file:
    products = pickle.load(file)

with open('./data/fourth_task_updates.json', 'rb') as file:
    price_updates = json.load(file)

product_map = {}
for product in products:
    product_map[product['name']] = product

methods = {
    'percent-': lambda price, param: price * (1 - param),
    'percent+': lambda price, param: price * (1 + param),
    'add': lambda price, param: price + param,
    'sub': lambda price, param: price - param
}

for update in price_updates:
    product = product_map[update['name']]
    product['price'] = methods[update['method']](product['price'], update['param'])

products = list(product_map.values())

with open('fourth_task.pkl', 'wb') as f:
    pickle.dump(products, f)
