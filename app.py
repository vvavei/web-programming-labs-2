from flask import Flask, url_for, redirect, render_template, request
import os
from lab1 import lab1
from lab2 import lab2
from lab3 import lab3
from lab4 import lab4
from lab5 import lab5
from lab6 import lab6
from lab7 import lab7
from lab8 import lab8

app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'секрет')
app.config['DB_TYPE'] = os.getenv('DB_TYPE', 'postgres')


app.register_blueprint(lab1)
app.register_blueprint(lab2)
app.register_blueprint(lab3)
app.register_blueprint(lab4)
app.register_blueprint(lab5)
app.register_blueprint(lab6)
app.register_blueprint(lab7)
app.register_blueprint(lab8)


@app.errorhandler(404)
def not_found(err):
     css_path = url_for("static", filename="lab1/lab1.css")
     er = url_for("static", filename="lab1/404.jpg")
     return '''
<!doctype html>
<html>
    <head>
        <link rel = "stylesheet" href="''' + css_path + '''">
    </head>
    <body>
        <h2>нет такой страницы!!!!!!!!!!</h2>
        <img src = "''' + er + '''">
    </body>
</html>
''',  404


@app.errorhandler(500)
def internal_server_error(err):
    return '''
<!doctype html>
<html>
    <body>
        <h1>Внутренняя ошибка сервера</h1>
        <div>
            Сервер обнаружил внутреннюю ошибку и не смог выполнить ваш запрос. 
            Либо сервер перегружен, либо ошибка в приложении.
        </div>
    </body>
</html>
''',  500



@app.route('/')
@app.route('/index')
def home():
    return '''
<!doctype html>
<html>
    <head>
        <title>НГТУ, ФБ, Лабораторные работы</title>
    </head>
    <body>
        <header>
            <h1>НГТУ, ФБ, WEB-программирование, часть 2. Список лабораторных</h1>
        </header>
        <div>
            <ul>
                <li><a href="/lab1">Первая лабораторная</a></li>
                <li><a href="/lab2">Вторая лабораторная</a></li>
                <li><a href="/lab3/">Третья лабораторная</a></li>
                <li><a href="/lab4/">Четвертая лабораторная</a></li>
                <li><a href="/lab5/">Пятая лабораторная</a></li>
                <li><a href="/lab6/">Шестая лабораторная</a></li>
                <li><a href="/lab7/">Седьмая лабораторная</a></li>
                <li><a href="/lab8/">Восьмая лабораторная</a></li>
            </ul>
        </div>
        <footer>
            <p>Свиридова Софья Денисовна, ФБИ-22, 3 курс, 2024</p>
        </footer>
    </body>
</html>
'''
 
    



