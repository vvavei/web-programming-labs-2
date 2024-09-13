from flask import Flask, url_for, redirect
app = Flask(__name__)

@app.errorhandler(404)
def not_found(err):
    return "нет такой страницы", 404

@app.route("/web")
def web():
    return '''<!doctype html>
        <html>
            <body>
                <h1>web-сервер на flask</h1>
                <a href = "/author">author</a>
            </body> 
        </html>''', 200, {
            'X-Server': 'sample',
            'Content-Type': 'text/plain; charset=utf-8'
        }

@app.route("/author")
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
               <a href = "/web">web</a>
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

@app.route("/info")
def info():
    return redirect("/author")

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