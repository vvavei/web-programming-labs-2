from flask import Blueprint, render_template, request, redirect, session, current_app, flash
from werkzeug.security import check_password_hash, generate_password_hash

from db import db
from db.models import users, articles
from flask_login import login_user, login_required, current_user, logout_user

lab8 = Blueprint('lab8', __name__)


@lab8.route('/lab8/')
def lab():
    return render_template('lab8/lab8.html', user = current_user)

@lab8.route('/lab8/register/', methods = ['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('lab8/register.html')
    
    login_form = request.form.get('login')
    password_form = request.form.get('password')


    if not login_form:
        return render_template('/lab8/register.html', error='Имя пользователя не может быть пустым')
    
  
    if not password_form:
        return render_template('/lab8/register.html', error='Пароль не может быть пустым')
    
    login_exists = users.query.filter_by(login = login_form).first()
    if login_exists:
        return render_template('/lab8/register.html', error = 'Такой пользователь уже существует')
    
    password_hash = generate_password_hash(password_form)
    new_user = users(login = login_form, password = password_hash)
    db.session.add(new_user)
    db.session.commit()

    # Автоматический логин после регистрации
    login_user(new_user, remember=False)

    return redirect('/lab8/')

@lab8.route('/lab8/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('lab8/login.html')
    
    login_form = request.form.get('login')
    password_form = request.form.get('password')
    remember_me = request.form.get('remember_me')

    if not login_form:
        return render_template('/lab8/login.html', error='Имя пользователя не может быть пустым')
    
    if not password_form:
        return render_template('/lab8/login.html', error='Пароль не может быть пустым')

    user = users.query.filter_by(login = login_form).first()

    if user:
        if check_password_hash(user.password, password_form):
            login_user(user, remember = remember_me == True)
            return redirect('/lab8/')
        
    return render_template('/lab8/login.html', error = 'Ошибка входа: логин и/или пароль неверны')

@lab8.route('/lab8/articles/')
@login_required
def article_list():
    all_articles = articles.query.filter_by(login_id=current_user.id).all()
    return render_template('lab8/articles.html', articles=all_articles)
    

@lab8.route('/lab8/logout')
@login_required
def logout():
    logout_user()
    return redirect('/lab8/')

@lab8.route('/lab8/create', methods=['GET', 'POST'])
@login_required
def create_article():
    if request.method == 'GET':
        return render_template('lab8/create_article.html')
    
    title = request.form.get('title')
    content = request.form.get('content')
    is_public = request.form.get('is_public') == 'on'  # Проверяем, отмечен ли флажок

    if not title or not content:
        return render_template('lab8/create_article.html', error='Заголовок и содержимое статьи не могут быть пустыми')
    
    new_article = articles(
        title=title,
        article_text=content,
        login_id=current_user.id,
        is_public=is_public  # Сохраняем значение is_public
    )
    db.session.add(new_article)
    db.session.commit()

    return redirect('/lab8/articles')

@lab8.route('/lab8/edit/<int:article_id>', methods=['GET', 'POST'])
@login_required
def edit_article(article_id):
    article = articles.query.get(article_id)

    if not article:
        return "Статья не найдена", 404

    # Проверяем, что статья принадлежит текущему пользователю
    if article.login_id != current_user.id:
        return "У вас нет прав на редактирование этой статьи", 403

    if request.method == 'GET':
        return render_template('lab8/edit_article.html', article=article)
    
    title = request.form.get('title')
    article_text = request.form.get('content')  # Используем 'content' из формы

    if not title or not article_text:
        return render_template('lab8/edit_article.html', article=article, error='Заголовок и содержимое статьи не могут быть пустыми')
    
    article.title = title
    article.article_text = article_text  # Используем правильное имя поля
    db.session.commit()

    return redirect('/lab8/articles')


@lab8.route('/lab8/delete/<int:article_id>', methods=['POST'])
@login_required
def delete_article(article_id):
    article = articles.query.get(article_id)

    if not article:
        return "Статья не найдена", 404

 
    if article.login_id != current_user.id:
        return redirect('/lab8')

    db.session.delete(article)
    db.session.commit()

    return redirect('/lab8/articles')

@lab8.route('/lab8/public_articles')
def public_articles():
    # Получаем все публичные статьи
    all_public_articles = articles.query.filter_by(is_public=True).all()
    return render_template('lab8/public_articles.html', articles=all_public_articles)

@lab8.route('/lab8/search', methods=['GET'])
def search_articles():
    query = request.args.get('query')  # Получаем строку поиска из параметров запроса

    # Ищем статьи, содержащие строку поиска в заголовке или тексте
    search_results = articles.query.filter(
        (articles.title.contains(query)) | (articles.article_text.contains(query))
    ).all()

    return render_template('lab8/search_results.html', query=query, articles=search_results)