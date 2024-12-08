from flask import Blueprint,  render_template, request, redirect, jsonify, session, current_app
from os import path
import sqlite3
import psycopg2
from psycopg2.extras import RealDictCursor
import datetime

lab7 = Blueprint('lab7', __name__)

def db_connect():
    if current_app.config['DB_TYPE'] == 'postgres':
        conn = psycopg2.connect(
            host='127.0.0.1',
            database='abc',
            user='postgres',
            password='admin'
        )
        cur = conn.cursor(cursor_factory=RealDictCursor)
    else:
        dir_path = path.dirname(path.realpath(__file__))
        db_path = path.join(dir_path, "database.db")
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()

    return conn, cur

def db_close(conn, cur):
    conn.commit()
    cur.close()
    conn.close()



@lab7.route('/lab7/')
def main():
    return render_template('lab7/lab7.html')

@lab7.route('/lab7/rest-api/films/', methods=['GET'])
def get_films():
    conn, cur = db_connect()
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT * FROM films ORDER BY id")
    else:
        cur.execute("SELECT * FROM films ORDER BY id")
    films = cur.fetchall()
    db_close(conn, cur)
    return jsonify([dict(film) for film in films])

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['GET'])
def get_film(id):
    conn, cur = db_connect()
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT * FROM films WHERE id = %s", (id,))
    else:
        cur.execute("SELECT * FROM films WHERE id = ?", (id,))
    film = cur.fetchone()
    db_close(conn, cur)
    if film is None:
        return "Film not found", 404
    return jsonify(dict(film))

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['DELETE'])
def del_film(id):
    conn, cur = db_connect()
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("DELETE FROM films WHERE id = %s", (id,))
    else:
        cur.execute("DELETE FROM films WHERE id = ?", (id,))
    db_close(conn, cur)
    return '', 204

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['PUT'])
def put_film(id):
    conn, cur = db_connect()
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT * FROM films WHERE id = %s", (id,))
    else:
        cur.execute("SELECT * FROM films WHERE id = ?", (id,))
    film = cur.fetchone()
    if film is None:
        db_close(conn, cur)
        return "Film not found", 404
    
    data = request.get_json()
    
    # Проверка описания
    if data['description'] == '':
        db_close(conn, cur)
        return {'description': 'Заполните описание'}, 400
    if len(data['description']) > 2000:
        db_close(conn, cur)
        return {'description': 'Описание должно быть не более 2000 символов'}, 400
    
    # Проверка оригинального названия
    if data['title'] == '' and data['title_ru'] == '':
        db_close(conn, cur)
        return {'title': 'Заполните оригинальное или русское название'}, 400
    
    # Проверка русского названия
    if data['title_ru'] == '':
        db_close(conn, cur)
        return {'title_ru': 'Заполните русское название'}, 400
    
    # Проверка года
    try:
        film_year = int(data['film_year'])
        current_year = datetime.datetime.now().year
        if not (1895 <= film_year <= current_year):
            db_close(conn, cur)
            return {'film_year': f'Год должен быть от 1895 до {current_year}'}, 400
    except ValueError:
        db_close(conn, cur)
        return {'film_year': 'Год должен быть числом'}, 400
    
    # Если оригинальное название пустое, устанавливаем его равным русскому названию
    if data['title'] == '':
        data['title'] = data['title_ru']
    
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("UPDATE films SET title = %s, title_ru = %s, film_year = %s, description = %s WHERE id = %s",
                    (data['title'], data['title_ru'], data['film_year'], data['description'], id))
    else:
        cur.execute("UPDATE films SET title = ?, title_ru = ?, film_year = ?, description = ? WHERE id = ?",
                    (data['title'], data['title_ru'], data['film_year'], data['description'], id))
    db_close(conn, cur)
    return jsonify(data)

@lab7.route('/lab7/rest-api/films/', methods=['POST'])
def add_film():
    data = request.get_json()
    
    # Проверка описания
    if data['description'] == '':
        return {'description': 'Заполните описание'}, 400
    if len(data['description']) > 2000:
        return {'description': 'Описание должно быть не более 2000 символов'}, 400
    
    # Проверка оригинального названия
    if data['title'] == '' and data['title_ru'] == '':
        return {'title': 'Заполните оригинальное или русское название'}, 400
    
    # Проверка русского названия
    if data['title_ru'] == '':
        return {'title_ru': 'Заполните русское название'}, 400
    
    # Проверка года
    try:
        film_year = int(data['film_year'])
        current_year = datetime.datetime.now().year
        if not (1895 <= film_year <= current_year):
            return {'film_year': f'Год должен быть от 1895 до {current_year}'}, 400
    except ValueError:
        return {'film_year': 'Год должен быть числом'}, 400
    
    # Если оригинальное название пустое, устанавливаем его равным русскому названию
    if data['title'] == '':
        data['title'] = data['title_ru']
    
    conn, cur = db_connect()
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("INSERT INTO films (title, title_ru, film_year, description) VALUES (%s, %s, %s, %s) RETURNING id",
                    (data['title'], data['title_ru'], data['film_year'], data['description']))
    else:
        cur.execute("INSERT INTO films (title, title_ru, film_year, description) VALUES (?, ?, ?, ?)",
                    (data['title'], data['title_ru'], data['film_year'], data['description']))
    new_film_id = cur.fetchone()['id'] if current_app.config['DB_TYPE'] == 'postgres' else cur.lastrowid
    db_close(conn, cur)
    return {"index": new_film_id}, 201

