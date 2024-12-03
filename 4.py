import os
import re
import json
from bs4 import BeautifulSoup


def parse_xml(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        xml = f.read()
    clothings = BeautifulSoup(xml, 'xml').find_all('clothing')
    items = []
    for clothing in clothings:
        item = {}
        item['id'] = int(clothing.id.get_text())
        item['name'] = clothing.find_all('name')[0].get_text().strip()
        item['category'] = clothing.category.get_text().strip()
        item['size'] = clothing.size.get_text().strip()
        item['color'] = clothing.color.get_text().strip()
        item['material'] = clothing.material.get_text().strip()
        item['price'] = float(clothing.price.get_text().strip())
        item['rating'] = float(clothing.rating.get_text().strip())
        item['reviews'] = int(clothing.reviews.get_text().strip())
        if clothing.sporty is not None:
            item['sporty'] = clothing.sporty.get_text().strip() == 'yes'
        if clothing.new is not None:
            item['new'] = clothing.new.get_text().strip() == '+'
        if clothing.exclusive is not None:
            item['exclusive'] = clothing.exclusive.get_text().strip() == 'yes'
        items.append(item)
    return items

def process_data(data_list):
    sorted_data = sorted(data_list, key=lambda item: item["rating"])
    filtered_data = [item for item in data_list if 'sporty' in item and item['sporty'] == 'yes']
    prices = [item["price"] for item in data_list]
    price_stats = {
      "sum": sum(prices),
      "min": min(prices),
      "max": max(prices),
      "avg": sum(prices) / len(prices) if prices else 0
    }
    colors = [item["color"] for item in data_list if 'color' in item]
    color_counts = {}
    for color in colors:
      color_counts[color] = color_counts.get(color, 0) + 1

    return sorted_data, filtered_data, price_stats, color_counts


if __name__ == "__main__":
    data_dir = "./data/4"
    absolute_data_dir = os.path.abspath(data_dir)
    html_files = [f for f in os.listdir(absolute_data_dir) if f.endswith(".xml")]
    parsed_data = []
    for file in html_files:
        absolute_filepath = os.path.join(absolute_data_dir, file)
        data = parse_xml(absolute_filepath)
        if data:
            parsed_data += data
    sorted_data, filtered_data, views_stats, city_counts = process_data(parsed_data)

    with open("output_4_18.json", "w", encoding="utf-8") as f:
        json.dump({"all_data": parsed_data, "sorted_data": sorted_data, "filtered_data": filtered_data, "views_stats": views_stats, "city_counts": city_counts}, f, ensure_ascii=False)