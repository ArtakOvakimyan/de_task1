import sqlite3
import pandas as pd

def get_conn(db_name):
    conn = sqlite3.connect(db_name)
    return conn

def conv_to_dfs():
    books_df = pd.read_csv('./books.csv')
    authors_df = pd.read_csv('./authors.csv')
    genres_df = pd.read_csv('./genres.csv')
    return [books_df, authors_df, genres_df]

def conv_to_tables():
    books_df, authors_df, genres_df = conv_to_dfs()
    conn = get_conn('./5.db')
    books_df.to_sql('books', conn, if_exists='append', index=False)
    authors_df.to_sql('authors', conn, if_exists='append', index=False)
    genres_df.to_sql('genres', conn, if_exists='append', index=False)
    conn.close()
    
if __name__ == '__main__':
    conv_to_tables()
