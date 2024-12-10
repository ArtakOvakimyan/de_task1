import sqlite3
import pandas as pd
import json


def connect_to_db(filename):
    return sqlite3.connect(filename)

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
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS prise (
            name text references tournament(name),
            place integer,
            prise integer
        )
    """)
    conn.commit()
    
def fill_table(data, conn):
    cursor = conn.cursor()
    cursor.executemany("""
        INSERT INTO prise (name, place, prise)
        VALUES (:name, :place, :prise)
    """, data)
    conn.commit()

def first_query(conn):
    cursor = conn.cursor()
    cursor.execute("""
        SELECT t.id, t.name AS tournament_name, p.prise
        FROM tournament t
        JOIN prise p ON t.name = p.name;
    """)
    return cursor.fetchall()

def second_query(conn):
    cursor = conn.cursor()
    cursor.execute("""
        SELECT t.id, t.name AS tournament_name, p.prise
        FROM tournament t
        JOIN prise p ON t.name = p.name
        WHERE p.prise > 1000000;
    """)
    return cursor.fetchall()

def third_query(conn):
    cursor = conn.cursor()
    cursor.execute("""
        SELECT t.name AS tournament_name, SUM(p.prise) AS total_prize
        FROM tournament t
        JOIN prise p ON t.name = p.name
        GROUP BY t.name;
    """)
    return cursor.fetchall()


if __name__ == '__main__':
    data = read_custom_file('./data/1-2/subitem.text')
    conn = connect_to_db('./1task_18.db')
    create_table(conn)
    fill_table(data, conn)
    print("Все турниры с призовыми фондами")
    print(first_query(conn))

    print("Турниры с призовым фондом больше 1,000,000")
    print(second_query(conn))

    print("Общий призовой фонд для каждого турнира")
    print(third_query(conn))
    