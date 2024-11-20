import json
import msgpack
import os


with open('./data/third_task.json', 'r', encoding='utf-8') as json_file:
    products = json.load(json_file)

aggregated_data = []
products_stat = {}

for product in products:
    price = product['price']
    name = product['name']
    if name not in products_stat:
        products_stat[name] = []
    products_stat[name].append(price)

for name, prices in products_stat.items():
    avg_price = sum(prices) / len(prices)
    max_price = max(prices)
    min_price = min(prices)

    aggregated_data.append({
        'name': name,
        'average_price': avg_price,
        'max_price': max_price,
        'min_price': min_price
    })

with open('third_task_18.json', 'w') as json_file:
    json.dump(aggregated_data, json_file, indent=4)

with open('third_task_18.msgpack', 'wb') as msgpack_file:
    packed_data = msgpack.packb(aggregated_data)
    msgpack_file.write(packed_data)

json_size = os.path.getsize('third_task_18.json')
msgpack_size = os.path.getsize('third_task_18.msgpack')

print(f"Размер файла JSON: {json_size}")
print(f"Размер файла Msgpack: {msgpack_size}")
print(f"Разница: {json_size-msgpack_size}")