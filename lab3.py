from flask import Blueprint, render_template, request, make_response, redirect
lab3 = Blueprint('lab3', __name__)


@lab3.route('/lab3/')
def lab():
    name = request.cookies.get('name')
    name_color = request.cookies.get('name_color')
    return render_template('lab3/lab3.html', name=name, name_color = name_color)


@lab3.route('/lab3/cookie')
def cookie():
    resp = make_response(redirect('/lab3/'))
    resp.set_cookie('name', 'Alex', max_age=5)
    resp.set_cookie('age', '20')
    resp.set_cookie('name_color', 'magenta')
    return resp


@lab3.route('/lab3/del_cookie')
def del_cookie():
    resp = make_response(redirect('/lab3/'))
    resp.delete_cookie('name')
    resp.delete_cookie('age')
    resp.delete_cookie('name_color')
    return resp


@lab3.route('/lab3/form1')
def form1():
    errors = {}
    user = request.args.get('user')
    if user == '':
        errors['user'] = 'Заполните поле!'

    age = request.args.get('age')
    if age == '':
        errors['age'] = 'Заполните поле!'

    sex = request.args.get('sex')
    return render_template('lab3/form1.html', user = user, age=age, sex=sex, errors = errors)


@lab3.route('/lab3/order')
def order():
    return render_template('lab3/order.html')

@lab3.route('/lab3/pay')
def pay():
    price = 0
    drink = request.args.get('drink')
    # Пусть кофе стоит 120 рублей, черный чай - 80 рублей, зеленый - 70 рублей.
    if drink == 'coffee':
        price = 120
    elif drink == 'black-tea':
        price = 80
    else:
        price = 70

    #Добавка молока удорожает напиток на 30 рублей, а сахара - на 10.
    if request.args.get('milk') == 'on':
        price += 30 
    if request.args.get('sugar') == 'on':
        price += 10

    return render_template('lab3/pay.html', price=price)


@lab3.route('/lab3/success')
def success():
    price = request.args.get('price')  
    return render_template('lab3/success.html', price=price)

@lab3.route('/lab3/settings')
def settings():
    # Получаем значения из cookies или параметров запроса
    color = request.args.get('color')
    background = request.args.get('background')
    font_size = request.args.get('font_size')
    font_weight = request.args.get('font_weight')

    # Создаем ответ
    resp = make_response(redirect('/lab3/settings'))

    # Устанавливаем cookie для всех параметров, если они переданы
    if color:
        resp.set_cookie('color', color)
    if background:
        resp.set_cookie('background', background)
    if font_size:
        resp.set_cookie('font_size', font_size)
    if font_weight:
        resp.set_cookie('font_weight', font_weight)

    # Если никаких параметров нет, рендерим страницу с текущими значениями
    if not color and not background and not font_size and not font_weight:
        color = request.cookies.get('color')
        background = request.cookies.get('background')
        font_size = request.cookies.get('font_size')
        font_weight = request.cookies.get('font_weight')
        resp = make_response(render_template('lab3/settings.html', color=color, background=background, font_size=font_size, font_weight=font_weight))

    return resp


