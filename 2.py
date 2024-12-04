import os
import re
import json
from bs4 import BeautifulSoup

def parse_html(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()

    soup = BeautifulSoup(html, 'html.parser')
    products = soup.find_all('div', attrs={'class': 'product-item'})
    items = []
    for product in products:
        item = {}
        item['id'] = int(product.a['data-id'])
        item['link'] = product.find_all('a')[1]['href']
        item['img'] = product.img['src']
        item['title'] = product.span.get_text().strip()
        item['price'] = float(product.price.get_text().replace('₽', '').replace(' ', '').strip())
        item['bonus'] = int(product.strong.get_text()
                            .replace('+ начислим', '')
                            .replace(' бонусов', '')
                            .strip()
                            )
        properties = product.ul.find_all('li')
        for prop in properties:
            item[prop['type']] = prop.get_text().strip()
        items.append(item)
    return items


def process_data(data_list):
    sorted_data = sorted(data_list, key=lambda item: item["id"])
    filtered_data = [item for item in data_list if 'ram' in item and int(re.sub(r'[^0-9]', '', item["ram"])) > 8]
    prices = [item["price"] for item in data_list]
    price_stats = {
      "sum": sum(prices),
      "min": min(prices),
      "max": max(prices),
      "avg": sum(prices) / len(prices) if prices else 0
    }

    matrix_types = [item["matrix"] for item in data_list if 'matrix' in item]
    matrix_counts = {}
    for matrix_type in matrix_types:
      matrix_counts[matrix_type] = matrix_counts.get(matrix_type, 0) + 1

    return sorted_data, filtered_data, price_stats, matrix_counts


if __name__ == "__main__":
    data_dir = "./data/2"
    absolute_data_dir = os.path.abspath(data_dir)
    html_files = [f for f in os.listdir(absolute_data_dir) if f.endswith(".html")]
    parsed_data = []
    for file in html_files:
        absolute_filepath = os.path.join(absolute_data_dir, file)
        data = parse_html(absolute_filepath)
        if data:
            parsed_data += data
    sorted_data, filtered_data, stats, counts = process_data(parsed_data)

    with open("output_2_18.json", "w", encoding="utf-8") as f:
        json.dump({"all_data": parsed_data, "sorted_data": sorted_data, "filtered_data": filtered_data, "stats": stats, "counts": counts}, f, ensure_ascii=False)