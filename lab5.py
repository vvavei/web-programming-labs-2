from flask import Blueprint, render_template, request, redirect, session, current_app
import psycopg2
from psycopg2.extras import RealDictCursor
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3
from os import path
lab5 = Blueprint('lab5', __name__)


@lab5.route('/lab5/')
def lab():
    return render_template('lab5/lab5.html', login = session.get('login'))

def db_connect():
    if current_app.config['DB_TYPE'] == 'postgres':
        conn = psycopg2.connect(
            host = '127.0.0.1',
            database = 'abc',
            user  = 'postgres',
            password = 'admin'
        )
        cur = conn.cursor(cursor_factory=RealDictCursor)
    else:
        dir_path = path.dirname(path.realpath(__file__))
        db_path = path.join(dir_path, "database.db")
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()

    return conn, cur

def db_close(conn,cur):
    conn.commit()
    cur.close()
    conn.close()

@lab5.route('/lab5/register', methods = ['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('lab5/register.html')
    
    login = request.form.get('login')
    password = request.form.get('password')

    if not (login or password):
        return render_template('lab5/register.html', error = 'Заполните все поля')
    
    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT login FROM users WHERE login=%s;", (login,))
    else:
        cur.execute("SELECT login FROM users WHERE login=?;", (login,)) 

    if cur.fetchone():
        db_close(conn,cur)
        return render_template('lab5/register.html', error = "Такой пользователь уже существует")
    
    password_hash = generate_password_hash(password)

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("INSERT INTO users (login, password) VALUES (%s, %s);", (login, password_hash))
    else:
        cur.execute("INSERT INTO users (login, password) VALUES (?, ?);", (login, password_hash))


    db_close(conn, cur)
    return render_template('lab5/success.html', login =login)

@lab5.route('/lab5/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('lab5/login.html')
    
    login = request.form.get('login')
    password = request.form.get('password')

    if not (login or password):
        return render_template('lab5/login.html', error = "Заполните все поля")
    
    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT * FROM users WHERE login=%s;", (login,))
    else:
        cur.execute("SELECT * FROM users WHERE login=?;", (login,))
    user = cur.fetchone()

    if not user:
        db_close(conn, cur)
        return render_template('lab5/login.html', error = 'Логин и/или пароль неверны')
    
    if not check_password_hash(user['password'], password):
        db_close(conn, cur)
        return render_template('lab5/login.html', error = 'Логин и/или пароль неверны')
    
    session['login'] = login
    db_close(conn, cur)
    return render_template('lab5/success_login.html', login = login)


@lab5.route('/lab5/create', methods=['GET', 'POST'])
def create():
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')
    
    if request.method == 'GET':
        return render_template('lab5/create_article.html')
    
    # Получаем данные из формы
    title = request.form.get('title')
    article_text = request.form.get('article_text')
    is_public = request.form.get('is_public') == 'on'  # Преобразуем флажок в True или False

    if not title or not article_text:
        error_message = "Заполните все поля: и название, и текст статьи."
        return render_template('lab5/create_article.html', error=error_message)

    # Подключаемся к базе данных
    conn, cur = db_connect()

    # Получаем id пользователя
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT id FROM users WHERE login=%s;", (login,))
    else:
        cur.execute("SELECT id FROM users WHERE login=?;", (login,))
    user = cur.fetchone()

    if user is None:
        db_close(conn, cur)
        return redirect('/lab5')

    user_id = user["id"]

    # Вставляем статью с полем is_public
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute(
            "INSERT INTO articles (user_id, title, article_text, is_public) VALUES (%s, %s, %s, %s);",
            (user_id, title, article_text, is_public)
        )
    else:
        cur.execute(
            "INSERT INTO articles (user_id, title, article_text, is_public) VALUES (?, ?, ?, ?);",
            (user_id, title, article_text, is_public)
        )

    # Сохраняем изменения и закрываем соединение
    conn.commit()
    db_close(conn, cur)
    
    return redirect('/lab5/list')



@lab5.route('/lab5/list')
def list():
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')
    
    conn, cur = db_connect()

    # Получаем id пользователя
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT id FROM users WHERE login=%s;", (login,))
    else:
        cur.execute("SELECT id FROM users WHERE login=?;", (login,))
    user_id = cur.fetchone()["id"]

    # Запрос всех статей с сортировкой по `is_favorite` (любимые статьи идут первыми)
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT * FROM articles WHERE user_id=%s ORDER BY is_favorite DESC, id DESC;", (user_id,))
    else:
        cur.execute("SELECT * FROM articles WHERE user_id=? ORDER BY is_favorite DESC, id DESC;", (user_id,))

    articles = cur.fetchall()

    db_close(conn, cur)
    return render_template('lab5/articles.html', articles=articles)




@lab5.route('/lab5/logout')
def logout():
    session.pop('login', None)  
    return redirect('/lab5/login')  


@lab5.route('/lab5/edit/<int:article_id>', methods=['GET', 'POST'])
def edit_article(article_id):
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')

    conn, cur = db_connect()

    # Получаем id пользователя
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT id FROM users WHERE login=%s;", (login,))
    else:
        cur.execute("SELECT id FROM users WHERE login=?;", (login,))
    user = cur.fetchone()

    if user is None:
        db_close(conn, cur)
        return redirect('/lab5')

    user_id = user["id"]

    # Обработка формы редактирования
    if request.method == 'POST':
        title = request.form.get('title')
        article_text = request.form.get('article_text')

        if not title or not article_text:
            error_message = "Заполните все поля."
            db_close(conn, cur)
            return render_template('lab5/edit_article.html', article={'id': article_id, 'title': title, 'article_text': article_text}, error=error_message)

        # Обновляем статью в базе данных
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("UPDATE articles SET title=%s, article_text=%s WHERE id=%s AND user_id=%s;", (title, article_text, article_id, user_id))
        else:
            cur.execute("UPDATE articles SET title=?, article_text=? WHERE id=? AND user_id=?;", (title, article_text, article_id, user_id))

        conn.commit()
        db_close(conn, cur)
        return redirect('/lab5/list')

    # Получаем статью для редактирования
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT * FROM articles WHERE id=%s AND user_id=%s;", (article_id, user_id))
    else:
        cur.execute("SELECT * FROM articles WHERE id=? AND user_id=?;", (article_id, user_id))

    article = cur.fetchone()

    db_close(conn, cur)

    if article is None:
        return redirect('/lab5/list')

    return render_template('lab5/edit_article.html', article=article)


@lab5.route('/lab5/delete/<int:article_id>', methods=['POST'])
def delete_article(article_id):
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')

    # Подключаемся к базе данных
    conn, cur = db_connect()

    # Получаем id пользователя
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT id FROM users WHERE login=%s;", (login,))
    else:
        cur.execute("SELECT id FROM users WHERE login=?;", (login,))
    user = cur.fetchone()

    if user is None:
        db_close(conn, cur)
        return redirect('/lab5/list')

    user_id = user["id"]

    # Удаляем статью, если она принадлежит пользователю
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("DELETE FROM articles WHERE id=%s AND user_id=%s;", (article_id, user_id))
    else:
        cur.execute("DELETE FROM articles WHERE id=? AND user_id=?;", (article_id, user_id))

    # Сохраняем изменения
    conn.commit()
    db_close(conn, cur)
    
    return redirect('/lab5/list')


#Дополнительное задание

@lab5.route('/lab5/users')
def list_users():
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')

    # Подключаемся к базе данных
    conn, cur = db_connect()

    # Получаем список логинов всех пользователей
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT login FROM users;")
    else:
        cur.execute("SELECT login FROM users;")

    users = cur.fetchall()  # Получаем все логины

    db_close(conn, cur)

    return render_template('lab5/users.html', users=users)


@lab5.route('/lab5/favorite/<int:article_id>', methods=['POST'])
def toggle_favorite(article_id):
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')
    
    # Подключаемся к базе данных
    conn, cur = db_connect()

    # Получаем id пользователя, чтобы убедиться, что статья принадлежит текущему пользователю
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT id FROM users WHERE login=%s;", (login,))
    else:
        cur.execute("SELECT id FROM users WHERE login=?;", (login,))
    user = cur.fetchone()

    if user is None:
        db_close(conn, cur)
        return redirect('/lab5/list')

    user_id = user["id"]

    # Проверяем текущий статус `is_favorite` и меняем его
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT is_favorite FROM articles WHERE id=%s AND user_id=%s;", (article_id, user_id))
    else:
        cur.execute("SELECT is_favorite FROM articles WHERE id=? AND user_id=?;", (article_id, user_id))
    
    article = cur.fetchone()

    # Если статья найдена, переключаем ее статус
    if article is not None:
        new_status = not article['is_favorite']
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("UPDATE articles SET is_favorite=%s WHERE id=%s AND user_id=%s;", (new_status, article_id, user_id))
        else:
            cur.execute("UPDATE articles SET is_favorite=? WHERE id=? AND user_id=?;", (new_status, article_id, user_id))

        conn.commit()

    db_close(conn, cur)
    return redirect('/lab5/list')

@lab5.route('/lab5/public')
def public_articles():
    conn, cur = db_connect()

    # Запрос всех публичных статей, где is_public = TRUE
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT * FROM articles WHERE is_public=TRUE ORDER BY is_favorite DESC, id DESC;")
    else:
        cur.execute("SELECT * FROM articles WHERE is_public=1 ORDER BY is_favorite DESC, id DESC;")

    articles = cur.fetchall()

    db_close(conn, cur)
    return render_template('lab5/public_articles.html', articles=articles)


@lab5.route('/lab5/toggle_public/<int:article_id>', methods=['POST'])
def toggle_public(article_id):
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')
    
    # Подключаемся к базе данных
    conn, cur = db_connect()

    # Получаем id пользователя, чтобы убедиться, что статья принадлежит текущему пользователю
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT id FROM users WHERE login=%s;", (login,))
    else:
        cur.execute("SELECT id FROM users WHERE login=?;", (login,))
    user = cur.fetchone()

    if user is None:
        db_close(conn, cur)
        return redirect('/lab5/list')

    user_id = user["id"]

    # Проверяем текущий статус `is_public` и меняем его
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT is_public FROM articles WHERE id=%s AND user_id=%s;", (article_id, user_id))
    else:
        cur.execute("SELECT is_public FROM articles WHERE id=? AND user_id=?;", (article_id, user_id))
    
    article = cur.fetchone()

    # Если статья найдена, переключаем ее статус
    if article is not None:
        new_status = not article['is_public']
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("UPDATE articles SET is_public=%s WHERE id=%s AND user_id=%s;", (new_status, article_id, user_id))
        else:
            cur.execute("UPDATE articles SET is_public=? WHERE id=? AND user_id=?;", (new_status, article_id, user_id))

        conn.commit()

    db_close(conn, cur)
    return redirect('/lab5/list')







    

