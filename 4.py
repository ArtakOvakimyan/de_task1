import sqlite3
import pandas as pd
import msgpack
import csv


def read_csv(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, [
            'name', 'price', 'quantity', 'category', 'fromCity', 'isAvailable', 'views'
        ], delimiter=';')
        reader.__next__()
        items = []
        for item in list(reader):
            item['price'] = float(item['price'])
            item['quantity'] = bool(item['isAvailable'])
            if item['views'] is not None:
                item['views'] = int(item['views'])
                items.append(item)
    return items

def read_custom_file(file_path):
    """
    Все попытки прочитать файл как msgpack приводили к ошибке:
        msgpack.exceptions.ExtraData: unpack(b) received extra data.
    """
    results = []
    current_entry = {}

    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            if line == '=====':
                if current_entry:
                    if current_entry['method'] == 'available':
                        current_entry['param'] = bool(current_entry['param'])
                    elif current_entry['method'] != 'remove':
                        current_entry['param'] = float(current_entry['param'])
                    results.append(current_entry)
                    current_entry = {}
            else:
                key, value = line.split('::', 1)
                current_entry[key] = value
        if current_entry:
            results.append(current_entry)
    return results

def create_table(conn):
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY,
            name TEXT,
            price FLOAT,
            quantity INTEGER,
            category TEXT,
            fromCity TEXT,
            isAvailable BOOLEAN,
            views INTEGER,
            version INTEGER DEFAULT 0
        )''')
    conn.commit()
    
def fill_table(conn, data):
    cursor = conn.cursor()
    cursor.executemany('''
        INSERT INTO products 
        (name, price, quantity, category, fromCity, isAvailable, views) 
        VALUES (:name, :price, :quantity, :category, :fromCity, :isAvailable, :views);
    ''', data)
    conn.commit()

def modify(data, conn):
    cursor = conn.cursor()
    for update in data:
        try:
            cursor.execute('SELECT * FROM products WHERE name = ?', (name,))
            product = cursor.fetchone()
            if not product:
                continue
            if method == 'price_abs':
                new_price = price + float(param)
                if new_price >= 0:
                    cursor.execute('UPDATE products SET price = ?, version = version + 1 WHERE id = ?', (new_price, product_id))

            elif method == 'price_percent':
                new_price = price * (1 + float(param))
                if new_price >= 0:
                    cursor.execute('UPDATE products SET price = ?, version = version + 1 WHERE id = ?', (new_price, product_id))

            elif method == 'quantity_add':
                new_quantity = quantity + int(param)
                cursor.execute('UPDATE products SET quantity = ?, version = version + 1 WHERE id = ?', (new_quantity, product_id))

            elif method == 'quantity_sub':
                new_quantity = quantity - int(param)
                if new_quantity >= 0:
                    cursor.execute('UPDATE products SET quantity = ?, version = version + 1 WHERE id = ?', (new_quantity, product_id))

            elif method == 'available':
                cursor.execute('UPDATE products SET isAvailable = ?, version = version + 1 WHERE id = ?', (int(param == 'True'), product_id))

            elif method == 'remove':
                cursor.execute('DELETE FROM products WHERE id = ?', (product_id,))
            conn.commit()
        except:
            continue

def top_products(cursor):
    res = cursor.execute('SELECT name, version FROM products ORDER BY version DESC LIMIT 10')
    return res.fetchall()

def price_stat(cursor):
    res = cursor.execute('''
        SELECT 
        category,
        SUM(price) as total, 
        MIN(price) as min_price, 
        MAX(price) as max_price, 
        AVG(price) as avg_price, 
        COUNT(*) as product_count
    FROM products
    GROUP BY category
    ''')
    return res.fetchall()

def left_stat(cursor):
    res = cursor.execute('''
    SELECT 
        category, 
        SUM(quantity) as total_quantity, 
        MIN(quantity) as min_quantity, 
        MAX(quantity) as max_quantity, 
        AVG(quantity) as avg_quantity, 
        COUNT(*) as product_count
    FROM products
    GROUP BY category
    ''')
    return res.fetchall()

def available_fruits(cursor):
    res = cursor.execute('SELECT name, views FROM products WHERE category = "fruit" AND isAvailable = 1 AND views > 5000')
    return res.fetchall()

if __name__ == '__main__':
    conn = sqlite3.connect('./4task_18.db')
    conn.cursor().execute("DROP TABLE products")
    data = read_csv('./data/4/_product_data.csv')
    updates = read_custom_file('./data/4/_update_data.text')
    create_table(conn)
    fill_table(conn, data)
    modify(updates, conn)
    cursor = conn.cursor()

    print('10 самых обновляемых товаров')
    print(top_products(cursor))

    print('Анализ цен товаров')
    print(price_stat(cursor))

    print('Анализ остатков товаров в группах (по категориям)')
    print(left_stat(cursor))

    print('Список доступных фруктов с просмотрами более 5000')
    print(available_fruits(cursor))

    conn.close()
