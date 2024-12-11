import sqlite3
import json

# Подключение к существующей базе данных
conn = sqlite3.connect('./5.db')
cursor = conn.cursor()

# Функция для сохранения результатов в JSON файл
def save_to_json(data, filename):
    with open(filename, 'w') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)

# Запрос 1: Выборка книг по автору с сортировкой и ограничением
query1 = '''
SELECT name FROM books WHERE author_id = 1 ORDER BY name LIMIT 2
'''
result1 = cursor.execute(query1).fetchall()
result1_json = [row[0] for row in result1]
#save_to_json(result1_json, 'books_by_author.json')


# Запрос 2: Подсчет количества книг по жанру
query2 = '''
SELECT g.name, COUNT(b.id) as book_count FROM genres g
LEFT JOIN books b ON g.id = b.genre_id
GROUP BY g.name
'''
result2 = cursor.execute(query2).fetchall()
# Преобразование результатов в список словарей
result2_json = [{"genre": row[0], "book_count": row[1]} for row in result2]
#save_to_json(result2_json, 'book_count_by_genre.json')

# Запрос 3: Группировка книг по авторам
query3 = '''
SELECT a.name, COUNT(b.id) as book_count FROM authors a
LEFT JOIN books b ON a.id = b.author_id
GROUP BY a.name
'''
result3 = cursor.execute(query3).fetchall()
# Преобразование результатов в список словарей
result3_json = [{"author": row[0], "book_count": row[1]} for row in result3]
#save_to_json(result3_json, 'book_count_by_author.json')

# Запрос 4: Обновление названия книги
update_query = '''
UPDATE books SET name = "Harry Potter and the Philosopher's Stone" WHERE id = 1
'''
cursor.execute(update_query)
conn.commit()

# Проверка обновления
check_update_query = '''
SELECT name FROM books WHERE id = 1
'''
updated_result = cursor.execute(check_update_query).fetchall()
# Преобразование результатов в список строк
updated_result_json = [row[0] for row in updated_result]
#save_to_json(updated_result_json, 'updated_book_title.json')

# Запрос 5: Выборка книг по жанру с сортировкой и ограничением
query5 = '''
SELECT b.name FROM books b
JOIN genres g ON b.genre_id = g.id
WHERE g.name = 'Fiction' ORDER BY b.name LIMIT 2;
'''
result5 = cursor.execute(query5).fetchall()
result5_json = [{"book_name": row[0]} for row in result5]
#save_to_json(result5_json, 'books_in_fiction.json')

# Запрос 6: Подсчет количества книг по авторам с условием на жанр
query6 = '''
SELECT a.name, COUNT(b.id) as book_count FROM authors a
JOIN books b ON a.id = b.author_id
JOIN genres g ON b.genre_id = g.id
WHERE g.name = 'Science Fiction'
GROUP BY a.name;
'''
result6 = cursor.execute(query6).fetchall()
result6_json = [{"author": row[0], "book_count": row[1]} for row in result6]

results = {
    'books_by_author': result1_json,
    'book_count_by_genre': result2_json,
    'book_count_by_author': result3_json,
    'updated_book_title': updated_result_json,
    'books_in_fiction': result5_json,
    'book_count_by_author_in_sci_fi': result6_json
}

save_to_json(results, 'results.json')

# Закрытие соединения с базой данных
conn.close()
