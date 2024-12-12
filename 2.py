from pymongo import MongoClient
from dotenv import load_dotenv
import os
import json

load_dotenv()
mongo_password = os.getenv('MONGO_PASSWORD')
MONGODB_URI = f"mongodb+srv://ovakimyanartak3:{mongo_password}@cluster0.hjvi2.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

def connect_mongo():
    return MongoClient(MONGODB_URI)

def get_collection(client):
    db = client['db-2024']
    col = db['jobs1']
    return col

def read_custom_file(file_path):
    results = []
    current_entry = {}

    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            if line == '=====':
                if current_entry:
                    results.append(current_entry)
                    current_entry = {}
            else:
                key, value = line.split('::', 1)
                if key in ['id', 'salary', 'year', 'age']:
                    value = int(value)
                current_entry[key] = value
        if current_entry:
            results.append(current_entry)
    return results

def calculate_salary_statistics(collection):
    """Вывод минимальной, средней, максимальной salary."""
    result = collection.aggregate([
        {
            '$group': {
                '_id': None,
                'min_salary': {'$min': '$salary'},
                'avg_salary': {'$avg': '$salary'},
                'max_salary': {'$max': '$salary'}
            }
        }
    ])
    result = list(result)[0]
    del result['_id']
    return result

def count_jobs_by_profession(collection):
    """Вывод количества данных по представленным профессиям."""
    result = collection.aggregate([
        {
            '$group': {
                '_id': '$job',
                'count': {'$sum': 1}
            }
        }
    ])
    return list(result)

def calculate_salary_by_city(collection):
    """Вывод минимальной, средней, максимальной salary по городу."""
    result = collection.aggregate([
        {
            '$group': {
                '_id': '$city',
                'min_salary': {'$min': '$salary'},
                'avg_salary': {'$avg': '$salary'},
                'max_salary': {'$max': '$salary'}
            }
        }
    ])
    return list(result)

def calculate_salary_by_profession(collection):
    """Вывод минимальной, средней, максимальной salary по профессии."""
    result = collection.aggregate([
        {
            '$group': {
                '_id': '$job',
                'min_salary': {'$min': '$salary'},
                'avg_salary': {'$avg': '$salary'},
                'max_salary': {'$max': '$salary'}
            }
        }
    ])
    return list(result)

def calculate_age_statistics_by_city(collection):
    """Вывод минимального, среднего, максимального возраста по городу."""
    result = collection.aggregate([
        {
            '$group': {
                '_id': '$city',
                'min_age': {'$min': '$age'},
                'avg_age': {'$avg': '$age'},
                'max_age': {'$max': '$age'}
            }
        }
    ])
    return list(result)

def calculate_age_statistics_by_profession(collection):
    """Вывод минимального, среднего, максимального возраста по профессии."""
    result = collection.aggregate([
        {
            '$group': {
                '_id': '$job',
                'min_age': {'$min': '$age'},
                'avg_age': {'$avg': '$age'},
                'max_age': {'$max': '$age'}
            }
        }
    ])
    return list(result)

def max_salary_min_age(collection):
    """Вывод максимальной заработной платы при минимальном возрасте."""
    result = collection.aggregate([
        {
            '$group': {
                '_id': None,
                'max_salary_at_min_age': {'$max': {'$cond': [{'$eq': ['$age', {'$min': '$age'}]}, '$salary', None]}}
            }
        }
    ])
    return list(result)[0]['max_salary_at_min_age']

def min_salary_max_age(collection):
    """Вывод минимальной заработной платы при максимальном возрасте."""
    result = collection.aggregate([
        {
            '$group': {
                '_id': None,
                'min_salary_at_max_age': {'$min': {'$cond': [{'$eq': ['$age', {'$max': '$age'}]}, '$salary', None]}}
            }
        }
    ])
    return list(result)[0]['min_salary_at_max_age']

def age_statistics_with_salary_condition(collection):
    """Вывод минимального, среднего, максимального возраста по городу с условием salary > 50000."""
    result = collection.aggregate([
        {
            '$match': {'salary': {'$gt': 50000}}
        },
        {
            '$group': {
                '_id': '$city',
                'min_age': {'$min': '$age'},
                'avg_age': {'$avg': '$age'},
                'max_age': {'$max': '$age'}
            }
        }
    ])
    return list(result)

def salary_in_ranges(collection):
    """Вывод минимальной, средней, максимальной salary в заданных диапазонах по городу, профессии и возрасту."""
    result = collection.aggregate([
        {
            '$match': {
                '$or': [
                    {'age': {'$gt': 18, '$lt': 25}},
                    {'age': {'$gt': 50, '$lt': 65}}
                ]
            }
        },
        {
            '$group': {
                '_id': {'city': '$city', 'job': '$job'},
                'min_salary': {'$min': '$salary'},
                'avg_salary': {'$avg': '$salary'},
                'max_salary': {'$max': '$salary'}
            }
        }
    ])
    return list(result)

def arbitrary_query(collection):
    """Произвольный запрос с $match, $group, $sort."""
    result = collection.aggregate([
        {
            '$match': {'salary': {'$gt': 60000}}
        },
        {
            '$group': {
                '_id': '$job',
                'total_salary': {'$sum': '$salary'},
                'count_jobs': {'$sum': 1}
            }
        },
        {
            '$sort': {'total_salary': -1}
        }
    ])
    return list(result)

def summarize_results():
    results = {}
    results['salary_statistics'] = calculate_salary_statistics(collection)
    results['jobs_by_profession'] = count_jobs_by_profession(collection)
    results['salary_by_city'] = calculate_salary_by_city(collection)
    results['salary_by_profession'] = calculate_salary_by_profession(collection)
    results['age_statistics_by_city'] = calculate_age_statistics_by_city(collection)
    results['age_statistics_by_profession'] = calculate_age_statistics_by_profession(collection)
    results['max_salary_min_age'] = max_salary_min_age(collection)
    results['min_salary_max_age'] = min_salary_max_age(collection)
    results['age_statistics_with_salary_condition'] = age_statistics_with_salary_condition(collection)
    results['salary_in_ranges'] = salary_in_ranges(collection)
    results['arbitrary_query'] = arbitrary_query(collection)

    return results


if __name__ == '__main__':
    data = read_custom_file('./data/task_2_item.text')
    client = connect_mongo()
    collection = get_collection(client)
    collection.insert_many(data)
    
    results = summarize_results()
    
    with open('res_18_2.json', 'w', encoding='utf-8') as json_file:
        json.dump(results, json_file, ensure_ascii=False)