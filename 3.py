import sqlite3
import pandas as pd
import json
import msgpack
import pickle


def connect_to_db(filename):
    return sqlite3.connect(filename)
    
def load_json(filename):
    return pd.read_json(filename)
    
def write_json(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f)
        
def load_pkl(filename):
    return pd.DataFrame(pd.read_pickle(filename))
    
def convert_to_table(df, conn):
    df.to_sql('songs', conn, if_exists='replace', index=False)
    
def first_query(conn):
    res = pd.read_sql("""
        SELECT * FROM songs
        ORDER BY duration_ms DESC
        LIMIT 28;
    """, conn)
    return res.to_dict('records')

def second_query(conn):
    res = pd.read_sql("""
        SELECT
            SUM(popularity) as total_pop,
            MIN(popularity) as min_pop,
            MAX(popularity) as max_pop,
            ROUND(AVG(popularity), 2) as avg_pop
        FROM songs
    """, conn)
    return res.iloc[0].to_dict()
    
def third_query(conn):
    res = pd.read_sql("""
        SELECT
            COUNT(*) as count,
            genre
        FROM songs
        GROUP BY genre
    """, conn)
    return res.to_dict('records')
    
def fourth_query(conn):
    res = pd.read_sql("""
        SELECT *
        FROM songs
        WHERE year < 2006
        ORDER BY duration_ms DESC
        LIMIT 33
    """, conn)
    return res.to_dict('records')
    

if __name__ == '__main__':
    conn = connect_to_db('./3task_18.db')
    data1 = load_json('./data/3/_part_1.json')
    data2 = load_pkl('./data/3/_part_2.pkl')
    common_columns = list(set(data1.columns) & set(data2.columns))
    combined_data = pd.concat([data1[common_columns], data2[common_columns]], ignore_index=True)
    convert_to_table(combined_data, conn)
    write_json(first_query(conn), './3task_18_1.json')
    print(second_query(conn))
    print(third_query(conn))
    write_json(fourth_query(conn), './3task_18_4.json')
    conn.close()
