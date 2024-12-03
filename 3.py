import os
import re
import json
from bs4 import BeautifulSoup


def parse_xml(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        xml = f.read()
    star = BeautifulSoup(xml, 'xml').star
    item = {}
    for el in star:
        if el.name is None:
            continue
        item[el.name] = el.get_text().strip()
    item['radius'] = int(item['radius'])
    return item

def process_data(data_list):
    sorted_data = sorted(data_list, key=lambda item: int(item["radius"]))
    filtered_data = [item for item in data_list if 'rotation' in item and float(re.sub(r'[^0-9.]', '', item["rotation"])) > 500]
    distances = [float(re.sub(r'[^0-9.]', '', item["distance"])) for item in data_list]
    distance_stats = {
      "sum": sum(distances),
      "min": min(distances),
      "max": max(distances),
      "avg": sum(distances) / len(distances) if distances else 0
    }

    constellations = [item["constellation"] for item in data_list if 'constellation' in item]
    constellation_counts = {}
    for constellation in constellations:
      constellation_counts[constellation] = constellation_counts.get(constellation, 0) + 1

    return sorted_data, filtered_data, distance_stats, constellation_counts


if __name__ == "__main__":
    data_dir = "./data/3"
    absolute_data_dir = os.path.abspath(data_dir)
    html_files = [f for f in os.listdir(absolute_data_dir) if f.endswith(".xml")]
    parsed_data = []
    for file in html_files:
        absolute_filepath = os.path.join(absolute_data_dir, file)
        data = parse_xml(absolute_filepath)
        if data:
            parsed_data.append(data)
    sorted_data, filtered_data, views_stats, city_counts = process_data(parsed_data)

    with open("output_3_18.json", "w", encoding="utf-8") as f:
        json.dump({"all_data": parsed_data, "sorted_data": sorted_data, "filtered_data": filtered_data, "views_stats": views_stats, "city_counts": city_counts}, f, ensure_ascii=False)