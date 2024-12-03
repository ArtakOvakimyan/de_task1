import os
import json
from bs4 import BeautifulSoup

def parse_html(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()
    soup = BeautifulSoup(html, 'html.parser')
    build = soup.find_all('div', attrs={'class': 'build-wrapper'})[0]

    item = dict()
    item['city'] = build.find_all('span')[0].get_text().split(':')[1].strip()
    item['id'] = int(build.h1['id'])
    item['type'] = build.h1.get_text().split(':')[1].strip()
    address_temp = build.p.get_text().strip().replace('\n', '')
    address_temp = address_temp.split('Улица: ')[1].split('Индекс:')
    item['address'] = address_temp[0].strip()
    item['index'] = address_temp[1].strip()
    item['floors'] = int(build.find_all('span', attrs={'class': 'floors'})[0].get_text().split(':')[1])
    item['year'] = int(build.find_all('span', attrs={'class': 'year'})[0].get_text().split('Построено в')[1])
    spans = build.find_all('span', attrs={'class': ''})
    item['parking'] = spans[1].get_text().split(':')[1] == "да"
    item['rating'] = float(spans[2].get_text().split(':')[1])
    item['views'] = int(spans[3].get_text().split(':')[1])
    item['img'] = build.img['src']
    return item

def process_data(data_list):
  sorted_data = sorted(data_list, key=lambda item: item["floors"])
  filtered_data = [item for item in data_list if item["rating"] > 0.8]
  views = [item["views"] for item in data_list]
  views_stats = {
      "sum": sum(views),
      "min": min(views),
      "max": max(views),
      "avg": sum(views) / len(views) if views else 0
  }

  cities = [item["city"] for item in data_list]
  city_counts = {}
  for city in cities:
      city_counts[city] = city_counts.get(city, 0) + 1

  return sorted_data, filtered_data, views_stats, city_counts


if __name__ == "__main__":
    data_dir = "./data/1"
    absolute_data_dir = os.path.abspath(data_dir)
    html_files = [f for f in os.listdir(absolute_data_dir) if f.endswith(".html")]
    parsed_data = []
    for file in html_files:
        absolute_filepath = os.path.join(absolute_data_dir, file)
        data = parse_html(absolute_filepath)
        if data:
            parsed_data.append(data)
    sorted_data, filtered_data, views_stats, city_counts = process_data(parsed_data)

    with open("output_1_18.json", "w", encoding="utf-8") as f:
        json.dump({"all_data": parsed_data, "sorted_data": sorted_data, "filtered_data": filtered_data, "views_stats": views_stats, "city_counts": city_counts}, f, ensure_ascii=False)