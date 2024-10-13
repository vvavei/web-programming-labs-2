from flask import Blueprint, url_for, redirect, render_template, request
lab2 = Blueprint('lab2', __name__)


#Лабораторная работа 2
@lab2.route('/lab2/a/')
def a():
    return 'со слэшем'


@lab2.route('/lab2/a')
def a2():
    return 'без слэша'


# Список цветов и их цен
flower_list = [
    {'name': 'роза', 'price': 100},
    {'name': 'тюльпан', 'price': 80},
    {'name': 'незабудка', 'price': 60},
    {'name': 'ромашка', 'price': 40}
]


@lab2.route('/lab2/flowers/<int:flower_id>')
def flowers(flower_id):
    if flower_id >= len(flower_list):
        return '''
        <html>
        <body>
            <h1>Ошибка 404</h1>
            <p>Такого цветка нет</p>
            <a href="/lab2/flowers">Вернуться ко всем цветам</a>
        </body>
        </html>
        ''', 404
    else:
        flower = flower_list[flower_id]
        return f'''
        <html>
        <body>
            <h1>Цветок: {flower['name']}</h1>
            <p>Цена: {flower['price']} руб.</p>
            <a href="/lab2/flowers">Вернуться ко всем цветам</a>
        </body>
        </html>
        '''


@lab2.route('/lab2/clear_flowers')
def clear_flowers():
    flower_list.clear()
    return '''
    <html>
    <body>
        <h1>Список цветов очищен</h1>
        <a href="/lab2/flowers">Вернуться ко всем цветам</a>
    </body>
    </html>
    '''

 
@lab2.route('/lab2/example')
def example():
    name, group, course, number_lab = 'Софья Свиридова','ФБИ-22','3 курс', '2'
    fruits = [
        {'name':'яблоки', 'price': 100},
        {'name': 'груши', 'price': 120}, 
        {'name': 'апельсины', 'price': 80},  
        {'name':'мандарины', 'price': 95},
        {'name': 'манго', 'price': 321}
    ]
    return render_template('lab2/example.html', name = name, group = group, 
                           course = course, number_lab = number_lab, fruits = fruits)


@lab2.route('/lab2/')
def lab():
    return render_template('lab2/lab2.html')


@lab2.route('/lab2/filters')
def filtres():
    phrase = "О <b>сколько</b> <u>нам</u> <i>открытий</i> чудных..."
    return render_template('lab2/filter.html', phrase = phrase)


@lab2.route('/lab2/flowers')
def all_flowers():
    return render_template('lab2/flowers.html', flowers=flower_list)


@lab2.route('/lab2/delete_flower/<int:flower_id>', methods=['POST', 'GET'])
def delete_flower(flower_id):
    if flower_id >= len(flower_list):
        return '''
        <html>
        <body>
            <h1>Ошибка 404</h1>
            <p>Такого цветка нет</p>
            <a href="/lab2/flowers">Вернуться ко всем цветам</a>
        </body>
        </html>
        ''', 404
    else:
        flower_list.pop(flower_id)
        return redirect(url_for('lab2.all_flowers'))
    

@lab2.route('/lab2/add_flower/', methods=['GET', 'POST'])
def add_flower():
    if request.method == 'POST':
        name = request.form.get('name')
        price = request.form.get('price')
        if not name or not price.isdigit():
            return '''
            <html>
            <body>
                <h1>Ошибка 400</h1>
                <p>Вы не задали имя цветка или цену</p>
                <a href="/lab2/flowers">Вернуться ко всем цветам</a>
            </body>
            </html>
            ''', 400
        else:
            flower_list.append({'name': name, 'price': int(price)})
            return redirect(url_for('lab2.all_flowers'))
    return '''
    <html>
    <body>
        <h1>Добавить новый цветок</h1>
        <form method="post">
            <label>Название цветка: <input type="text" name="name" required></label><br>
            <label>Цена цветка: <input type="number" name="price" required></label><br>
            <input type="submit" value="Добавить">
        </form>
        <a href="/lab2/flowers">Вернуться ко всем цветам</a>
    </body>
    </html>
    '''


books = [
    {"title": "1984", "author": "Джордж Оруэлл", "genre": "Дистопия", "pages": 328},
    {"title": "Мастер и Маргарита", "author": "Михаил Булгаков", "genre": "Роман", "pages": 384},
    {"title": "Война и мир", "author": "Лев Толстой", "genre": "Исторический роман", "pages": 1225},
    {"title": "Преступление и наказание", "author": "Фёдор Достоевский", "genre": "Роман", "pages": 430},
    {"title": "Тошнота", "author": "Жан-Поль Сартр", "genre": "Философский роман", "pages": 250},
    {"title": "451 градус по Фаренгейту", "author": "Рэй Брэдбери", "genre": "Научная фантастика", "pages": 249},
    {"title": "Гордость и предубеждение", "author": "Джейн Остин", "genre": "Роман", "pages": 432},
    {"title": "Убить пересмешника", "author": "Харпер Ли", "genre": "Роман", "pages": 281},
    {"title": "Маленький принц", "author": "Антуан де Сент-Экзюпери", "genre": "Сказка", "pages": 96},
    {"title": "Алхимик", "author": "Пауло Коэльо", "genre": "Философский роман", "pages": 208}
]


@lab2.route('/lab2/books/')
def book_list():
    return render_template('lab2/books.html', books=books)


@lab2.route('/lab2/calc')
def trasp():
    return redirect("/lab2/calc/1/1")


@lab2.route('/lab2/calc/<int:a>')
def redirect_calc(a):
    return redirect(url_for('operations', a=a, b=1))


@lab2.route('/lab2/calc/<int:a>/<int:b>')
def operations(a, b):
    multiplication = a * b
    division = a / b if b != 0 else 'Ошибка: деление на ноль'
    addition = a + b
    subtraction = a - b
    exponentiation = a ** b

    return f'''
<!doctype html>
<html>
    <body>
    <h1>Расчет с параметрами:</h1>
    <p>Умножение: {a} * {b} = {multiplication}</p>
    <p>Деление: {a} / {b} = {division}</p>
    <p>Сложение: {a} + {b} = {addition}</p>
    <p>Вычитание: {a} - {b} = {subtraction}</p>
    <p>Возведение в степень: {a} <sup>{b}</sup> = {exponentiation}</p>
    </body>
</html>
'''


furnitures = [
    {
        'name': 'Диван',
        'description': 'Удобная мебель для отдыха и приема гостей.',
        'image': 'диван.jpg'
    },
    {
        'name': 'Стул',
        'description': 'Основной элемент для сидения за столом или в других местах.',
        'image': 'стул.jpg'
    },
    {
        'name': 'Стол',
        'description': 'Используется для приема пищи, работы или учебы.',
        'image': 'стол.jpg'
    },
    {
        'name': 'Кровать',
        'description': 'Мебель для сна и отдыха, важный элемент в спальне.',
        'image': 'кровать.jpg'
    },
    {
        'name': 'Шкаф',
        'description': 'Хранит одежду, обувь и другие вещи, помогает поддерживать порядок.',
        'image': 'шкаф.jpg'
    }
]


@lab2.route('/lab2/furniture')
def show_furniture():
    return render_template('lab2/furniture.html', furnitures=furnitures) 