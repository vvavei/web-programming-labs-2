from flask import Blueprint, render_template, request, redirect, session, current_app
from os import path
import sqlite3
import psycopg2
from psycopg2.extras import RealDictCursor

lab6 = Blueprint('lab6', __name__)

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

@lab6.route('/lab6/')
def main():
    return render_template('lab6/lab6.html')

@lab6.route('/lab6/json-rpc-api/', methods=['POST'])
def api():
    data = request.json
    id = data['id']

    if data['method'] == 'info':
        conn, cur = db_connect()
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute('SELECT * FROM offices ORDER BY number')
        else:
            cur.execute('SELECT * FROM offices ORDER BY number')
        offices = cur.fetchall()
        total_rent_cost = sum(office['price'] for office in offices if office['tenant'])
        db_close(conn, cur)
        return {
            'jsonrpc': '2.0',
            'result': {
                'offices': [dict(office) for office in offices],
                'total_rent_cost': total_rent_cost
            },
            'id': id
        }

    login = session.get('login')
    if not login:
        return {
            'jsonrpc': '2.0',
            'error': {
                'code': 1,
                'message': 'Unauthorized'
            },
            'id': id
        }

    if data['method'] == 'booking':
        office_number = data['params']
        conn, cur = db_connect()
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute('SELECT * FROM offices WHERE number = %s', (office_number,))
        else:
            cur.execute('SELECT * FROM offices WHERE number = ?', (office_number,))
        office = cur.fetchone()
        if office['tenant']:
            db_close(conn, cur)
            return {
                'jsonrpc': '2.0',
                'error': {
                    'code': 2,
                    'message': 'Already booked'
                },
                'id': id
            }
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute('UPDATE offices SET tenant = %s WHERE number = %s', (login, office_number))
        else:
            cur.execute('UPDATE offices SET tenant = ? WHERE number = ?', (login, office_number))
        db_close(conn, cur)
        return {
            'jsonrpc': '2.0',
            'result': 'success',
            'id': id
        }

    if data['method'] == 'cancellation':
        office_number = data['params']
        conn, cur = db_connect()
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute('SELECT * FROM offices WHERE number = %s', (office_number,))
        else:
            cur.execute('SELECT * FROM offices WHERE number = ?', (office_number,))
        office = cur.fetchone()
        if not office['tenant']:
            db_close(conn, cur)
            return {
                'jsonrpc': '2.0',
                'error': {
                    'code': 3,
                    'message': 'Офис не арендован'
                },
                'id': id
            }
        if office['tenant'] != login:
            db_close(conn, cur)
            return {
                'jsonrpc': '2.0',
                'error': {
                    'code': 4,
                    'message': 'Вы не можете снять чужую аренду'
                },
                'id': id
            }
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute('UPDATE offices SET tenant = %s WHERE number = %s', ('', office_number))
        else:
            cur.execute('UPDATE offices SET tenant = ? WHERE number = ?', ('', office_number))
        db_close(conn, cur)
        return {
            'jsonrpc': '2.0',
            'result': 'success',
            'id': id
        }

    return {
        'jsonrpc': '2.0',
        'error': {
            'code': -32601,
            'message': 'Method not found'
        },
        'id': id
    }