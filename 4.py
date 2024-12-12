import pandas as pd
from pymongo import MongoClient
import simplejson as json
from dotenv import load_dotenv
import os
from bson import ObjectId


load_dotenv()
mongo_password = os.getenv('MONGO_PASSWORD')
MONGODB_URI = f"mongodb+srv://ovakimyanartak3:{mongo_password}@cluster0.hjvi2.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

def connect_mongo():
    return MongoClient(MONGODB_URI)

def insert_data_from_csv(collection, csv_file, session):
    try:
        data = pd.read_csv(csv_file)
        records = data.to_dict(orient='records')
        collection.insert_many(records, session=session)
        print(f"Данные из {csv_file} успешно вставлены в {collection.name}.")
    except Exception as e:
        print(f"Ошибка при вставке данных из {csv_file}: {e}")
        
client = connect_mongo()
db = client['db-24']
autos_collection = db['autos']
cars_collection = db['cars']

results = {
    "selection_queries": {},
    "aggregation_queries": {},
    "update_delete_results": {}
}

with client.start_session() as session:  # Начинаем транзакцию
    try:
        insert_data_from_csv(autos_collection, './data/autos.csv', session)
        insert_data_from_csv(cars_collection, './data/cars.csv', session)

        print("Запросы на выборку:")
        results["selection_queries"]["dealer_sellers"] = list(autos_collection.find({'seller': 'gewerblich'}, session=session))
        results["selection_queries"]["expensive_cars"] = list(autos_collection.find({'price': {'$gt': 100000}}, session=session))
        results["selection_queries"]["recent_cars"] = list(cars_collection.find({'year_produced': {'$gte': 2019}}, session=session))
        results["selection_queries"]["subaru_cars"] = list(cars_collection.find({'manufacturer_name': 'Subaru'}, session=session).limit(50))
        results["selection_queries"]["first_five_autos"] = list(autos_collection.find().limit(5))
        
        print("\nЗапросы на агрегацию:")
        results["aggregation_queries"]["average_price_by_brand"] = list(autos_collection.aggregate([
            {'$group': {'_id': '$brand', 'average_price': {'$avg': '$price'}}}
        ], session=session))
        results["aggregation_queries"]["count_recent_cars"] = list(cars_collection.aggregate([
            {'$match': {'year_produced': {'$gte': 2010}}},
            {'$group': {'_id': '$model_name', 'count': {'$sum': 1}}}
        ], session=session))
        results["aggregation_queries"]["count_by_fuel_type"] = list(cars_collection.aggregate([
            {'$group': {'_id': '$engine_fuel', 'count': {'$sum': 1}}}
        ], session=session))
        results["aggregation_queries"]["average_power_by_gearbox"] = list(autos_collection.aggregate([
            {'$group': {'_id': '$gearbox', 'average_power': {'$avg': '$powerPS'}}}
        ], session=session))
        results["aggregation_queries"]["max_price_by_vehicle_type"] = list(cars_collection.aggregate([
            {'$group': {'_id': '$model_name', 'max_price': {'$max': '$price_usd'}}}
        ], session=session))

        print("\nЗапросы на обновление/удаление:")
        update_query1 = autos_collection.update_one(
            {'brand': 'mercedes_benz'},
            {'$set': {'price': 12000}},
            session=session
        )
        update_query2 = cars_collection.update_many(
            {'has_warranty': False},
            {'$set': {'has_warranty': True}},
            session=session
        )

        delete_query1 = autos_collection.delete_one({'name': 'Mazda_3_1.6_Sport'}, session=session)
        delete_query2 = cars_collection.delete_many({'price_usd': {'$lt': 2000}}, session=session)

        results["update_delete_results"] = {
            "updated_autos": update_query1.modified_count,
            "updated_cars": update_query2.modified_count,
            "deleted_autos": delete_query1.deleted_count,
            "deleted_cars": delete_query2.deleted_count
        }

    except Exception as e:
        print(f"Произошла ошибка: {e}")
        session.abort_transaction()


with open('res_18_4.json', 'w', encoding='utf-8') as json_file:
    json.dump(results, json_file, ignore_nan=True, indent=4, default=str, ensure_ascii=False)