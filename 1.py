import sqlite3
import pandas as pd
import json


def connect_to_db(filename):
    return sqlite3.connect(filename)
    
def load_csv(filename):
    return pd.read_csv(filename, sep=';', dtype={'begin': str})
    
def convert_to_table(df, conn):
    df.to_sql('tournament', conn, if_exists='append', index=False)
    
def first_query(conn):
    res = pd.read_sql("""
        SELECT *
        FROM tournament
        ORDER BY min_rating
        LIMIT 28
    """, conn)
    return res.to_dict('records')

def second_query(conn):
    res = pd.read_sql("""
        SELECT
            COUNT(*) as tournament_count,
            MIN(tours_count) as min_tours_count,
            MAX(tours_count) as max_tours_count,
            ROUND(AVG(min_rating), 2) as avg_min_rating
        FROM tournament
    """, conn)
    return res.iloc[0].to_dict()
    
def third_query(conn):
    res = pd.read_sql("""
        SELECT
            COUNT(*) as count,
            system
        FROM tournament
        GROUP BY system
    """, conn)
    return res.to_dict('records')
    
def fourth_query(conn):
    res = pd.read_sql("""
        SELECT *
        FROM tournament
        WHERE min_rating < 2300
        ORDER BY min_rating DESC
        LIMIT 28
    """, conn)
    return res.to_dict('records')
    

if __name__ == '__main__':
    csv = load_csv('./data/1-2/item.csv')
    conn = connect_to_db('./1task_18.db')
    convert_to_table(csv, conn)

    with open('./1task_18_1.json', 'w', encoding='utf-8') as f:
        json.dump(first_query(conn), f, ensure_ascii=False)
        
    print(second_query(conn))
    print(third_query(conn))

    with open('./1task_18_4.json', 'w', encoding='utf-8') as f:
        json.dump(fourth_query(conn), f, ensure_ascii=False)
