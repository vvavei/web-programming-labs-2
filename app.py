from flask import Flask, url_for, redirect
app = Flask(__name__)

@app.errorhandler(404)
def not_found(err):
    return "нет такой страницы", 404

@app.route("/lab1/error_400")
def bad_request():
    return '''
<!doctype html>
<html>
    <body>
        <div>Неверный запрос</div>
    </body>
</html>
''',  400 

@app.route("/lab1/error_401")
def error_401():
    return '''
<!doctype html>
<html>
    <body>
        <div>Запрос требует аутентификации пользователя</div>
    </body>
</html>
''',  401

@app.route("/lab1/error_402")
def error_402():
    return '''
<!doctype html>
<html>
    <body>
        <div>Зарезервировано для будущего использования</div>
    </body>
</html>
''',  402

@app.route("/lab1/error_403")
def error_403():
    return '''
<!doctype html>
<html>
    <body>
        <div>У вас нет разрешения на доступ к этому ресурсу</div>
    </body>
</html>
''',  403

@app.route("/lab1/error_405")
def error_405():
    return '''
<!doctype html>
<html>
    <body>
        <div>Метод не поддерживается</div>
    </body>
</html>
''',  405

@app.route("/lab1/error_418")
def error_418():
    return '''
<!doctype html>
<html>
    <body>
        <div>Я - чайник</div>
    </body>
</html>
''',  418

@app.route("/lab1/web")
def web():
    return '''<!doctype html>
        <html>
            <body>
                <h1>web-сервер на flask</h1>
                <a href = "/lab1/author">author</a>
            </body> 
        </html>''', 200, {
            'X-Server': 'sample',
            'Content-Type': 'text/plain; charset=utf-8'
        }

@app.route("/lab1/author")
def author():
    name = "Свиридова Софья Денисовна"
    group = "ФБИ-22"
    faculty = "ФБ"

    return '''<!doctype html>
        <html>
            <body>
               <p>Студент: ''' + name + '''</p>
               <p>Группа: ''' + group + '''</p>
               <p>Факультет: ''' + faculty + '''</p>
               <a href = "/lab1/web">web</a>
            </body>
        </html>'''    

@app.route("/lab1/oak")
def oak():
    path = url_for("static", filename="oak.jpg")
    css_path = url_for("static", filename="lab1.css")
    return '''
<!doctype html>
<html>
    <head>
        <link rel = "stylesheet" href="''' + css_path + '''">
    </head>
    <body>
        <h1>Дуб</h1>
        <img src = "''' + path + '''">
    </body>
</html>
'''      
count = 0

@app.route('/lab1/counter')
def counter():
    global count
    count += 1
    return '''
<!doctype html>
<html>
    <body>
        Сколько раз вы сюда заходили: ''' + str(count) + '''
        <a href="/lab1/reset_counter">Очистить счётчик</a>
    </body>
</html>
'''    

@app.route('/lab1/reset_counter')
def reset_counter():
    global count
    count = 0  
    return '''
<!doctype html>
<html>
    <body>
        <h1>Счётчик был очищен. Можете перейти обратно на страницу счётчика.</h1>
        <a href="/lab1/counter">Назад к счётчику</a>
    </body>
</html>
'''

@app.route("/lab1/info")
def info():
    return redirect("/lab1/author")

@app.route("/lab1/created")
def created():
    return '''
<!doctype html>
<html>
    <body>
        <h1>Создано успешно</h1>
        <div><i>что-то создано...</i></div>
    </body>
</html>
''',  201 

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
            </ul>
        </div>
        <footer>
            <p>Свиридова Софья Денисовна, ФБИ-22, 3 курс, 2024</p>
        </footer>
    </body>
</html>
'''


@app.route('/lab1')
def menu():
    return '''
<!doctype html>
<html>
    <head>
        <title>Лабораторная 1</title>
    </head>
    <body>
        <div>
        Flask — фреймворк для создания веб-приложений на языке
        программирования Python, использующий набор инструментов
        Werkzeug, а также шаблонизатор Jinja2. Относится к категории так
        называемых микрофреймворков — минималистичных каркасов
        веб-приложений, сознательно предоставляющих лишь самые базовые возможности.
        </div>   
        <a href="/">Назад</a> 
    </body>
</html>
'''

