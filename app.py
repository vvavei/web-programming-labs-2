from flask import Flask, url_for, redirect
app = Flask(__name__)

@app.errorhandler(404)
def not_found(err):
     css_path = url_for("static", filename="lab1.css")
     er = url_for("static", filename="404.jpg")
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

@app.route('/lab1/error_500')
def trigger_error():
    result = 1 / 0
    return result

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
        <a href="/">Назад</a><br>
        <h2>Список роутов</h2>
        <div>
            <ul>
                <li><a href="/lab1/web">web-сервер на flask</a></li>
                <li><a href="/lab1/author">Автор</a></li>
                <li><a href="/lab1/oak">Дуб</a></li>
                <li><a href="/lab1/counter">Сколько раз вы заходили</a></li>
                <li><a href="/lab1/reset_counter">Очистка счетчика</a></li>
                <li><a href="/lab1/info">Инфо</a></li>
                <li><a href="/lab1/created">что-то создано...</a></li>
                <li><a href="/lab1/student">Страница на выбор студента.Весна</a></li>
                <li><a href="/lab1/error_500">Ошибка 500</a></li>
                <li><a href="/lab1/error_400">Ошибка 400</a></li>
                <li><a href="/lab1/error_401">Ошибка 401</a></li>
                <li><a href="/lab1/error_402">Ошибка 402</a></li>
                <li><a href="/lab1/error_403">Ошибка 403</a></li>
                <li><a href="/lab1/error_405">Ошибка 405</a></li>
                <li><a href="/lab1/error_418">Ошибка 418</a></li>
                <li><a href ="/lab1/source">Дополнительное задание</a></li>
            </ul>
        </div>
    </body>
</html>
'''

@app.route('/lab1/student')
def student_page():
    kartinka = url_for("static", filename="vesna.jpg")
    return ''' <!doctype html>
        <html>
            <body>
                <div>
                    Весна- прекрасное время года. Весной разбухают почки, 
                    становится теплее после холодных зим, 
                    расцветают всеми любимые цветы подснежники. У всех растений начинается жизнь. 
                </div><br>
                <div>
                    Журчат ручьи, по крышам домов капает капель. Солнце светит всё ярче и ярче. 
                    Тает снег, травка зеленеет, птички прилетают с югов. 
                    Весна бывает теплая, бывает холодная.
                </div><br>
                <div>
                    Я надеюсь, что нынешняя весна будет тёплой и селнечной. 
                    Природа оживает в это замечательное время года. А после весны настаёт лето.
                </div>   
                <img src = "''' + kartinka + '''">
            </body>
        </html>''', 200, {
            'Content-Language': 'ru',
            'X-Zagolovok': 'custom',
            'X-AnotherZagolovok': 'customValue'
        }


#Дополнительное задание
resource_created = False 

@app.route('/lab1/source')
def start_resource():
    path = url_for("static", filename="пустырь.webp")
    css = url_for("static", filename="stye.css")
    global resource_created
    status = "Магическая башня построена" if resource_created else "Магической башни еще нет!"
    response = f'''
<!doctype html>
<html>
    <head>
        <link rel="stylesheet" type="text/css" href="{css}">
    </head>
    <body>
        <h1>{status}</h1>
        <a href="/lab1/create">Построить магическую башню</a><br>
        <a href="/lab1/delete">Разрушить магическую башню</a><br>
        <img src = "''' + path + '''">
    </body>
</html>
'''
    return response, 200

@app.route('/lab1/create')
def build_resource():
    css = url_for("static", filename="stye.css")
    path = url_for("static", filename="башня201.jpg")
    path1 = url_for("static", filename="bashnya400.webp")
    global resource_created
    if resource_created:
        return '''
<!doctype html>
<html>
    <head>
        <link rel="stylesheet" type="text/css" href="''' + css + '''">
    </head>
    <body>
        <h1>Магическая башня уже есть! Сначала нужно разрушить!!!!!</h1>
        <a href="/lab1/source">Назад</a><br>
        <img src = "''' + path1 + '''">
    </body>
</html>''', 400
    else:
        resource_created = True 
        return '''
<!doctype html>
<html>
    <head>
        <link rel="stylesheet" type="text/css" href="''' + css + '''">
    </head>
    <body>
        <h1>Магическая башня построена!!</h1>
        <a href="/lab1/source">Назад</a><br>
        <img src = "''' + path + '''">
    </body>
</html>''', 201
    
@app.route('/lab1/delete')
def resource_delete():
    css = url_for("static", filename="stye.css")
    path = url_for("static", filename="разруха.jpg")
    path1 = url_for("static", filename="разруха.jpg")
    global resource_created 
    if resource_created:
        resource_created = False 
        return '''
<!doctype html>
<html>
    <head>
        <link rel="stylesheet" type="text/css" href="''' + css + '''">
    </head>
    <body>
        <h1>Башня разрушена!Можно строить новую!!</h1>
        <a href="/lab1/source">Назад</a><br>
        <img src = "''' + path + '''">
    </body>
</html>''', 200
    else:
        return '''
<!doctype html>
<html>
    <head>
        <link rel="stylesheet" type="text/css" href="''' + css + '''">
    </head>
    <body>
        <h1>Тут одни развалины!!!Сначала нужно построить, чтобы разрушить!!</h1>
        <a href="/lab1/source">Назад</a><br>
        <img src = "''' + path1 + '''">
    </body>
</html>
''', 400 
    
@app.route('/lab2/a/')
def a():
    return 'со слэшем'

@app.route('/lab2/a')
def a2():
    return 'без слэша'

flower_list = ['роза', 'тюльпан', 'незабудка', 'ромашка']

@app.route('/lab2/flowers/<int:flower_id>')
def flowers(flower_id):
    if flower_id >= len(flower_list):
        return "такого цветка нет", 404
    else:
        return "цветок:" + flower_list[flower_id]
    
@app.route('/lab2/add_flower/<name>')
def add_flower(name):
    flower_list.append(name)
    return f'''
<!doctype html>
<html>
   <body>
   <h1>Добавлен новый цветок</h1>
   <p>Название нового цветка: {name} </p>
   <p>Всего цветов: {len(flower_list)}</p>
   <p>Полный список: {flower_list}</p>
   </body>
</html>
'''   