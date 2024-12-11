import sqlite3


def connect_db(db_name):
    return sqlite3.connect(db_name)

def create_database():
    conn = connect_db('./5.db')
    cursor = conn.cursor()

    cursor.executescript('''
    CREATE TABLE authors (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL
    );

    CREATE TABLE genres (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL
    );

    CREATE TABLE books (
        id INTEGER PRIMARY KEY,
        author_id INTEGER NOT NULL,
        genre_id INTEGER NOT NULL,
        name TEXT NOT NULL,
        FOREIGN KEY (author_id) REFERENCES authors(id),
        FOREIGN KEY (genre_id) REFERENCES genres(id)
    );
    ''')
    
    conn.commit()
    conn.close()


if __name__ == '__main__':
    create_database()
