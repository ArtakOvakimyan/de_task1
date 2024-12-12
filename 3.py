from pymongo import MongoClient
from dotenv import load_dotenv
import os
import json
import msgpack

load_dotenv()
mongo_password = os.getenv('MONGO_PASSWORD')
MONGODB_URI = f"mongodb+srv://ovakimyanartak3:{mongo_password}@cluster0.hjvi2.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

def connect_mongo():
    return MongoClient(MONGODB_URI)

def get_collection(client):
    db = client['db-2024']
    col = db['jobs1']
    return col

def read_msgpack(filename):
    with open(filename, 'rb') as f:
        byte_data = f.read()
    return msgpack.unpackb(byte_data)
    
def delete_salary_out_of_range(collection):
    """Удаляет документы с зарплатой < 25000 или > 175000."""
    collection.delete_many({
        '$or': [
            {'salary': {'$lt': 25000}},
            {'salary': {'$gt': 175000}}
        ]
    })

def increment_age(collection):
    """Увеличивает возраст всех документов на 1."""
    collection.update_many(
        {},
        {'$inc': {'age': 1}}
    )

def raise_salary_for_professions(collection, profession):
    """Поднимает зарплату на 5% для произвольно выбранных профессий."""
    collection.update_many(
        {'profession': {'$in': professions}},
        {'$mul': {'salary': 1.05}}
    )

def raise_salary_for_cities(collection, cities):
    """Поднимает зарплату на 7% для произвольно выбранных городов."""
    collection.update_many(
        {'city': {'$in': cities}},
        {'$mul': {'salary': 1.07}}
    )

def raise_salary_by_complex_predicate(collection, city, professions, age_range):
    """Поднимает зарплату на 10% для выборки по сложному предикату."""
    collection.update_many(
        {
            'city': city,
            'profession': {'$in': professions},
            'age': {'$gte': age_range[0], '$lte': age_range[1]}
        },
        {'$mul': {'salary': 1.10}}
    )
    
def delete_by_custom_predicate(collection, predicate):
    """Удаляет записи по произвольному предикату."""
    collection.delete_many(predicate)


if __name__ == '__main__':
    data = read_msgpack('./data/task_3_item.msgpack')
    client = connect_mongo()
    collection = get_collection(client)
    collection.insert_many(data)
    
    cities = ['Ереван', 'Москва', 'Афины']
    professions = ['IT-специалист', 'Архитектор', 'Инженер']
    
    delete_salary_out_of_range(collection)
    increment_age(collection)
    raise_salary_for_professions(collection, professions)
    raise_salary_for_cities(collection, cities)
    raise_salary_by_complex_predicate(collection, cities[0], professions[1:], (30, 50))
    custom_predicate = {'age': {'$lt': 20}}
    delete_by_custom_predicate(collection, custom_predicate)