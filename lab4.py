from flask import Blueprint, render_template, request, redirect, session
lab4 = Blueprint('lab4', __name__)


@lab4.route('/lab4/')
def lab():
    return render_template('lab4/lab4.html')


@lab4.route('/lab4/div-form')
def div_form():
    return render_template('lab4/div-form.html')


@lab4.route('/lab4/div', methods = ['POST'])
def div():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    if x1 == '' or x2 == '':
        return render_template('lab4/div.html', error = 'Оба поля должны быть заполнены!')
    
    x1 = int(x1)
    x2 = int(x2)
    if x2 == 0:
        return render_template('lab4/div.html', error = 'На ноль делить нельзя!')
    
    result = x1 / x2
    return render_template('lab4/div.html', x1=x1, x2=x2, result=result)


@lab4.route('/lab4/sum-form')
def sum_form():
    return render_template('lab4/sum-form.html')


@lab4.route('/lab4/sum', methods = ['POST'])
def sum():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    if x1 == '':
        x1 = 0

    if x2 == '':
        x2 = 0

    
    x1 = int(x1)
    x2 = int(x2)

    result = x1 + x2
    return render_template('lab4/sum.html', x1=x1, x2=x2, result=result)


@lab4.route('/lab4/umn-form')
def umn_form():
    return render_template('lab4/umn-form.html')


@lab4.route('/lab4/umn', methods = ['POST'])
def umn():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    if x1 == '':
        x1 = 1

    if x2 == '':
        x2 = 1

    
    x1 = int(x1)
    x2 = int(x2)

    result = x1 * x2
    return render_template('lab4/umn.html', x1=x1, x2=x2, result=result)


@lab4.route('/lab4/min-form')
def min_form():
    return render_template('lab4/min-form.html')


@lab4.route('/lab4/min', methods = ['POST'])
def min():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    if x1 == '' or x2 == '':
        return render_template('lab4/min.html', error = 'Оба поля должны быть заполнены!')
    
    x1 = int(x1)
    x2 = int(x2)

    result = x1 - x2
    return render_template('lab4/min.html', x1=x1, x2=x2, result=result)


@lab4.route('/lab4/step-form')
def step_form():
    return render_template('lab4/step-form.html')


@lab4.route('/lab4/step', methods = ['POST'])
def step():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    if x1 == '' or x2 == '':
        return render_template('lab4/step.html', error = 'Оба поля должны быть заполнены!')
    
    x1 = int(x1)
    x2 = int(x2)

    if x1 == 0 and x2 == 0:
        return render_template('lab4/step.html', error = 'Оба поля равны нулю! Исправьте!')

    result = x1 ** x2
    return render_template('lab4/step.html', x1=x1, x2=x2, result=result)


tree_count = 0
@lab4.route('/lab4/tree', methods = ['GET', 'POST'])
def tree():
    global tree_count 
    if request.method == 'GET':
        return render_template('lab4/tree.html', tree_count = tree_count)

    operation = request.form.get('operation')

    if operation == 'cut' and tree_count > 0:
        tree_count -= 1
    elif operation == 'plant' and tree_count < 10:
        tree_count += 1 

    return redirect('/lab4/tree') 


users = [
    {'login': 'alex', 'password': '123', 'name': 'Alexander Ivanov', 'gender': 'male'},
    {'login': 'bob','password': '555', 'name': 'Bob Smith', 'gender': 'male'},
    {'login': 'sonya','password': '333', 'name': 'Sonya Sviridova', 'gender': 'female'},
    {'login': 'alina','password': '777', 'name': 'Alina Klepikova', 'gender': 'female'}
]

@lab4.route('/lab4/login', methods = ['GET', 'POST'])
def  login():
    if request.method == 'GET':
        if 'login' in session:
            authorized = True
            login = session['login']
            user_name = ''
            for user in users:
                if user['login'] == login:
                    user_name = user['name']
                    break
              
           
        else:
            authorized = False
            login = ''
            user_name = ''

        return render_template("lab4/login.html", authorized = authorized, login = login, user_name = user_name)      
    
    login = request.form.get('login')
    password = request.form.get('password')

    # Проверка на пустые значения
    if login == '':
        error = 'Не введён логин'
        return render_template('lab4/login.html', error=error, authorized=False, login=login)
    if password == '':
        error = 'Не введён пароль'
        return render_template('lab4/login.html', error=error, authorized=False, login=login)
    
    for user in users:
        if login == user['login'] and password == user['password']:
            session['login'] = login
            return redirect('/lab4/login')
    
    error = 'Неверный логин и/или пароль'
    return render_template('lab4/login.html', error = error, authorized = False, login = login)

@lab4.route('/lab4/logout', methods = ['POST'])
def logout():
    session.pop('login', None)
    return redirect('/lab4/login')

@lab4.route('/lab4/fridge', methods=['GET', 'POST'])
def fridge():
    error = None
    message = None
    snowflakes = 0

    if request.method == 'POST':
        temperature = request.form.get('temperature')

        # Проверка на пустое значение
        if temperature == '':
            error = "Ошибка: не задана температура"
        else:
            try:
                temp_value = float(temperature)
                if temp_value < -12:
                    error = "Не удалось установить температуру — слишком низкое значение"
                elif temp_value > -1:
                    error = "Не удалось установить температуру — слишком высокое значение"
                elif -12 <= temp_value <= -9:
                    message = f"Установлена температура: {temp_value}°С"
                    snowflakes = 3
                elif -8 <= temp_value <= -5:
                    message = f"Установлена температура: {temp_value}°С"
                    snowflakes = 2
                elif -4 <= temp_value <= -1:
                    message = f"Установлена температура: {temp_value}°С"
                    snowflakes = 1
            except ValueError:
                error = "Ошибка: некорректное значение температуры"

    return render_template("lab4/fridge.html", error=error, message=message, snowflakes=snowflakes)

@lab4.route('/lab4/grain-order', methods=['GET', 'POST'])
def grain_order():
    prices = {
        'barley': 12345,
        'oats': 8522,
        'wheat': 8722,
        'rye': 14111
    }
    
    grain_names = {
        'barley': 'Ячмень',
        'oats': 'Овёс',
        'wheat': 'Пшеница',
        'rye': 'Рожь'
    }
    
    error = None
    message = None
    discount_message = None

    if request.method == 'POST':
        grain_type = request.form.get('grain_type')
        weight = request.form.get('weight')

        # Проверка на пустое значение веса
        if weight == '':
            error = "Ошибка: не указан вес"
        else:
            try:
                weight = float(weight)
                if weight <= 0:
                    error = "Ошибка: вес должен быть больше 0"
                elif weight > 500:
                    error = "Ошибка: такого объёма сейчас нет в наличии"
                elif grain_type not in prices:
                    error = "Ошибка: выбран некорректный тип зерна"
                else:
                    price_per_ton = prices[grain_type]
                    total_cost = weight * price_per_ton
                    discount_amount = 0  # Изначально скидка равна нулю

                    if weight > 50:
                        discount = 0.10
                        discount_amount = total_cost * discount
                        total_cost -= discount_amount
                        discount_message = f"Применена скидка за большой объём: 10% (скидка: {discount_amount:.2f} руб)"

                    message = f"Заказ успешно сформирован. Вы заказали {grain_names[grain_type]}. Вес: {weight} т. Сумма к оплате: {total_cost:.2f} руб"
            except ValueError:
                error = "Ошибка: некорректное значение веса"

    return render_template("lab4/grain_order.html", error=error, message=message, discount_message=discount_message, prices=prices)
