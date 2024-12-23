from flask import Blueprint, render_template, request, redirect, session, current_app, jsonify
from os import path
import sqlite3
import psycopg2
from werkzeug.security import check_password_hash, generate_password_hash
from psycopg2.extras import RealDictCursor

rgz = Blueprint('rgz', __name__)

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

@rgz.route('/rgz/index')
def index():
    return render_template('rgz/index.html')

@rgz.route('/rgz/')
def main():
    return render_template('rgz/cells.html')

@rgz.route('/rgz/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('rgz/register.html')
    
    login = request.form.get('login')
    password = request.form.get('password')

    if not (login and password):
        return render_template('rgz/register.html', error='Заполните все поля')
    
    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT login FROM users WHERE login=%s;", (login,))
    else:
        cur.execute("SELECT login FROM users WHERE login=?;", (login,))

    if cur.fetchone():
        db_close(conn, cur)
        return render_template('rgz/register.html', error='Такой пользователь уже существует')
    
    password_hash = generate_password_hash(password)

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("INSERT INTO users (login, password) VALUES (%s, %s);", (login, password_hash))
    else:
        cur.execute("INSERT INTO users (login, password) VALUES (?, ?);", (login, password_hash))

    db_close(conn, cur)

    # Автоматическая авторизация после регистрации
    session['login'] = login
    return render_template('rgz/success_login.html', login=login)

# Роут для авторизации
@rgz.route('/rgz/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('rgz/login.html')
    
    login = request.form.get('login')
    password = request.form.get('password')

    if not (login and password):
        return render_template('rgz/login.html', error='Заполните все поля')
    
    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT * FROM users WHERE login=%s;", (login,))
    else:
        cur.execute("SELECT * FROM users WHERE login=?;", (login,))
    user = cur.fetchone()

    if not user:
        db_close(conn, cur)
        return render_template('rgz/login.html', error='Логин и/или пароль неверны')
    
    if not check_password_hash(user['password'], password):
        db_close(conn, cur)
        return render_template('rgz/login.html', error='Логин и/или пароль неверны')
    
    session['login'] = login
    db_close(conn, cur)
    return render_template('rgz/success_login.html', login=login)

@rgz.route('/rgz/logout', methods=['POST'])
def logout():
    login = session.get('login')
    if not login:
        return redirect('/rgz/login')

    # Удаляем данные пользователя из сессии
    session.pop('login', None)
    return redirect('/rgz/')

@rgz.route('/rgz/cells/', methods=['GET'])
def get_cells():
    conn, cur = db_connect()
    cur.execute('SELECT id, is_booked, booked_by FROM cells ORDER BY id')
    cells = cur.fetchall()

    # Добавляем логин пользователя, если ячейка забронирована
    for cell in cells:
        if cell['booked_by']:
            cur.execute('SELECT login FROM users WHERE id = %s', (cell['booked_by'],))
            user = cur.fetchone()
            if user:
                cell['user_login'] = user['login']
            else:
                cell['user_login'] = None
        else:
            cell['user_login'] = None

    db_close(conn, cur)

    total_cells = len(cells)
    booked_cells = sum(1 for cell in cells if cell['is_booked'])
    free_cells = total_cells - booked_cells

    # Проверяем, авторизован ли пользователь
    login = session.get('login')
    if login:
        # Если авторизован, возвращаем полные данные
        return jsonify({
            'cells': cells,
            'total_cells': total_cells,
            'booked_cells': booked_cells,
            'free_cells': free_cells,
            'is_authorized': True
        })
    else:
        # Если не авторизован, возвращаем данные без возможности бронирования
        return jsonify({
            'cells': cells,
            'total_cells': total_cells,
            'booked_cells': booked_cells,
            'free_cells': free_cells,
            'is_authorized': False
        })

@rgz.route('/rgz/cells/<int:cell_id>/book/', methods=['PUT'])
def book_cell(cell_id):
    login = session.get('login')
    if not login:
        return jsonify({'error': 'Unauthorized'}), 401

    conn, cur = db_connect()

    # Найти идентификатор пользователя по логину
    cur.execute('SELECT id FROM users WHERE login = %s', (login,))
    user = cur.fetchone()
    if not user:
        db_close(conn, cur)
        return jsonify({'error': 'User not found'}), 404

    user_id = user['id']

    # Проверка на существование ячейки
    cur.execute('SELECT is_booked, booked_by FROM cells WHERE id = %s', (cell_id,))
    cell = cur.fetchone()

    if not cell:
        db_close(conn, cur)
        return jsonify({'error': 'Cell not found'}), 404

    if cell['is_booked']:
        db_close(conn, cur)
        return jsonify({'error': 'Ячейка уже забронирована'}), 400

    # Проверка, сколько ячеек уже забронировал пользователь
    cur.execute('SELECT COUNT(*) FROM cells WHERE booked_by = %s', (user_id,))
    booked_count = cur.fetchone()['count']
    if booked_count >= 5:
        db_close(conn, cur)
        return jsonify({'error': 'Вы можете забронировать только 5 ячеек'}), 400

    # Бронирование ячейки
    cur.execute('UPDATE cells SET is_booked = TRUE, booked_by = %s WHERE id = %s', (user_id, cell_id))
    db_close(conn, cur)

    return jsonify({'success': 'Cell successfully booked'}), 200

@rgz.route('/rgz/cells/<int:cell_id>/cancel/', methods=['DELETE'])
def cancel_cell(cell_id):
    login = session.get('login')
    if not login:
        return jsonify({'error': 'Unauthorized'}), 401

    conn, cur = db_connect()

    # Найти идентификатор пользователя по логину
    cur.execute('SELECT id FROM users WHERE login = %s', (login,))
    user = cur.fetchone()
    if not user:
        db_close(conn, cur)
        return jsonify({'error': 'User not found'}), 404

    user_id = user['id']

    # Проверка на существование ячейки
    cur.execute('SELECT is_booked, booked_by FROM cells WHERE id = %s', (cell_id,))
    cell = cur.fetchone()

    if not cell:
        db_close(conn, cur)
        return jsonify({'error': 'Cell not found'}), 404

    if not cell['is_booked']:
        db_close(conn, cur)
        return jsonify({'error': 'Cell is not booked'}), 400

    # Проверка, что текущий пользователь является владельцем брони
    if cell['booked_by'] != user_id:
        db_close(conn, cur)
        return jsonify({'error': 'You can only cancel your own bookings'}), 403

    # Отмена брони
    cur.execute('UPDATE cells SET is_booked = FALSE, booked_by = NULL WHERE id = %s', (cell_id,))
    db_close(conn, cur)

    return jsonify({'success': 'Cell booking canceled'}), 200

@rgz.route('/rgz/delete_account', methods=['DELETE'])
def delete_account():
    login = session.get('login')
    if not login:
        return jsonify({'error': 'Unauthorized'}), 401

    conn, cur = db_connect()

    # Удаляем аккаунт пользователя из базы данных
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("DELETE FROM users WHERE login=%s;", (login,))
    else:
        cur.execute("DELETE FROM users WHERE login=?;", (login,))

    db_close(conn, cur)

    # Удаляем данные пользователя из сессии
    session.pop('login', None)

    return jsonify({'success': 'Account deleted successfully'}), 200