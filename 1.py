from pymongo import MongoClient
from dotenv import load_dotenv
import os
import pickle
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

def read_pkl(filename):
    with open(filename, 'rb') as f:
        return pickle.load(f)

def save_results_to_json(results, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False)

def remove_id(documents):
    """Удаление поля _id из документов."""
    for doc in documents:
        doc.pop('_id', None)
    return documents

def get_top_10_jobs(collection):
    jobs = list(collection.find().sort('salary', -1).limit(10))
    return remove_id(jobs)

def get_young_jobs(collection):
    jobs = list(collection.find({'age': {'$lt': 30}}).sort('salary', -1).limit(15))
    return remove_id(jobs)

def get_filtered_jobs(collection, cities, professions):
    complex_filter = {
        'city': {'$in': cities},
        'job': {'$in': professions}
    }
    jobs = list(collection.find(complex_filter).sort('age', 1).limit(10))
    return remove_id(jobs)

def count_filtered_jobs(collection):
    count_filter = {
        'age': {'$gte': 20, '$lte': 40},
        'year': {'$in': [2019, 2020, 2021, 2022]},
        '$or': [
            {'salary': {'$gt': 50000, '$lte': 75000}},
            {'salary': {'$gt': 125000, '$lt': 150000}}
        ]
    }
    return collection.count_documents(count_filter)


if __name__ == '__main__':
    data = read_pkl('./data/task_1_item.pkl')
    client = connect_mongo()
    collection = get_collection(client)
    collection.insert_many(data)
    
    results = {}

    results['top_10_jobs'] = get_top_10_jobs(collection)
    results['young_jobs'] = get_young_jobs(collection)
    
    cities = ['Афины', 'Белград', 'Москва']
    professions = ['IT-специалист', 'Архитектор', 'Инженер']
    
    results['filtered_jobs'] = get_filtered_jobs(collection, cities, professions)
    results['count_result'] = count_filtered_jobs(collection)

    save_results_to_json(results, 'res_18_1.json')
    
    client.close()