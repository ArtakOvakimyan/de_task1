import os
import re
import json
from bs4 import BeautifulSoup

def parse_item_html(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()
    soup = BeautifulSoup(html, 'html.parser')
    item = {}
    item['name'] = soup.find('h1').get_text()
    price = soup.find('div', attrs={'class': 'product-item-detail-price-current'}).get_text()
    price = re.search(r'(\d+(\s\d+)*)(\sр\.)', price).group(1).replace(" ", "")
    item['price'] = int(price)
    brand = soup.find('span', attrs={'class': 'product-item-detail-properties-value'}).a.get_text()
    item['brand'] = brand
    review_count = soup.find('div', attrs={'class': 'bx-rating text-primary'}).get_text()
    review_count = review_count.strip('() \n\t').replace(' ', '')
    item['review_count'] = int(review_count)
    year_element = soup.find("span", string=lambda text: text and text.startswith("Год начала выпуска"))
    year = year_element.find_next_sibling("span", class_="product-item-detail-properties-value").text.strip()
    item['year'] = int(year)
    return item

def parse_catalog_html(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()

    soup = BeautifulSoup(html, 'html.parser')
    products = soup.find_all('div', attrs={'class': 'product-item'})
    items = []
    for product in products:
        item = {}
        name = product.find('div', attrs={'class': 'product-item-title'}).a.get_text().strip(' \t\n')
        item['name'] = name
        price = product.find('span', attrs={'class': 'product-item-price-current'}).get_text()
        price = re.search(r'(\d+(\s\d+)*)(\sр\.)', price).group(1).replace(" ", "")
        item['price'] = int(price)
        category = re.findall(r'[а-яА-ЯёЁ]+(?:\s+[а-яА-ЯёЁ]+)*', name)
        item['category'] = category[0]
        brand = product.find('div', attrs={'class': 'product-item-info-container product-item-brand-container'}).a.get_text()
        item['brand'] = brand
        items.append(item)
    return items

def process_item_data(data_list):
    sorted_data = sorted(data_list, key=lambda item: item["review_count"])
    filtered_data = [item for item in data_list if item['year'] and item['year'] > 2007]
    prices = [item["price"] for item in data_list]
    price_stats = {
      "sum": sum(prices),
      "min": min(prices),
      "max": max(prices),
      "avg": sum(prices) / len(prices) if prices else 0
    }

    brands = [item["brand"] for item in data_list if 'brand' in item]
    brand_counts = {}
    for brand in brands:
      brand_counts[brand] = brand_counts.get(brand, 0) + 1

    return sorted_data, filtered_data, price_stats, brand_counts

def process_catalog_data(data_list):
    sorted_data = sorted(data_list, key=lambda item: item["name"])
    filtered_data = [item for item in data_list if 'category' in item and item['category'] == 'парфюмерная вода']
    prices = [item["price"] for item in data_list]
    price_stats = {
      "sum": sum(prices),
      "min": min(prices),
      "max": max(prices),
      "avg": sum(prices) / len(prices) if prices else 0
    }

    brands = [item["brand"] for item in data_list if 'brand' in item]
    brand_counts = {}
    for brand in brands:
      brand_counts[brand] = brand_counts.get(brand, 0) + 1

    return sorted_data, filtered_data, price_stats, brand_counts

if __name__ == "__main__":
    catalog_dir = "./data/5/catalog"
    html_files = [f for f in os.listdir(catalog_dir) if f.endswith(".html")]
    parsed_data = []
    for file in html_files:
        filepath = os.path.join(catalog_dir, file)
        data = parse_catalog_html(filepath)
        if data:
            parsed_data += data
    sorted_data, filtered_data, stats, counts = process_catalog_data(parsed_data)

    with open("output_5_18_catalog.json", "w", encoding="utf-8") as f:
        json.dump({"all_data": parsed_data, "sorted_data": sorted_data, "filtered_data": filtered_data, "stats": stats, "counts": counts}, f, ensure_ascii=False)

    item_dir = "./data/5/item-page"
    html_files = [f for f in os.listdir(item_dir) if f.endswith(".html")]
    parsed_data = []
    for file in html_files:
        filepath = os.path.join(item_dir, file)
        data = parse_item_html(filepath)
        if data:
            parsed_data.append(data)
    sorted_data, filtered_data, stats, counts = process_item_data(parsed_data)

    with open("output_5_18_item.json", "w", encoding="utf-8") as f:
        json.dump({"all_data": parsed_data, "sorted_data": sorted_data, "filtered_data": filtered_data,
                   "stats": stats, "counts": counts}, f, ensure_ascii=False)