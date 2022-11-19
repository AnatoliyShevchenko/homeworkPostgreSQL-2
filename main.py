from flask import(Flask, render_template, request)
import psycopg2
from psycopg2 import Error
from psycopg2.extensions import (connection as Connection, ISOLATION_LEVEL_AUTOCOMMIT, cursor as Cursor)
from dotenv import load_dotenv
import os


app = Flask(__name__)

name = ''

try:
    load_dotenv()
    connection: Connection = psycopg2.connect(
        user=os.environ.get('USER'),
        password=os.environ.get('PASSWORD'),
        host=os.environ.get('HOST'),
        port=os.environ.get('PORT'),
    )
    connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    print('Connection Successful')
    cursor = connection.cursor()
    cursor.execute("CREATE DATABASE homework2;")
    print('Database is successful created!')

except:
    try:
        load_dotenv()
        connection: Connection = psycopg2.connect(
            user=os.environ.get('USER'),
            password=os.environ.get('PASSWORD'),
            host=os.environ.get('HOST'),
            port=os.environ.get('PORT'),
            database='homework2'
        )
        connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        print('Connection Successful')
        cursor = connection.cursor()
        cursor.execute('CREATE TABLE log(id SERIAL, login VARCHAR(50), password VARCHAR(60));')
        print('Table LOG is successful created!')
    except:
        try:
            load_dotenv()
            connection: Connection = psycopg2.connect(
                user=os.environ.get('USER'),
                password=os.environ.get('PASSWORD'),
                host=os.environ.get('HOST'),
                port=os.environ.get('PORT'),
                database='homework2'
            )    
            connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            print('Connection Successful')
            cursor = connection.cursor()
            cursor.execute('CREATE TABLE post(id SERIAL, about VARCHAR(100), post VARCHAR(500), name VARCHAR(50));')
            print('Table POST is successful created!')
        except:
            print("Все таблицы созданы")



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/autor-ok', methods=['POST'])
def autor_ok():
    global name
    answer = 0
    log = request.form.get('log')
    name = log
    pas = request.form.get('pass')
    cursor.execute("""SELECT * FROM log;""")
    data: list[tuple] = cursor.fetchall()
    print(data)
    print(log, pas)
    for i in data:
        if log == i[1] and pas == i[2]:
            print(i)
            answer: int = 1
            break
        else:
            answer = 0
    print(answer)
    if answer == 0:
        return '<h1 style="color: red;">Неправильный логин или пароль</h1>\
                <a href="/"><button>вернуться</button></a>'
    else:
        return '<h1>Вы успешно вошли</h1>\
                <a href="/post"><button>перейти</button></a>'


@app.route('/reg')
def reg():
    return render_template('reg.html')
    
@app.route('/ok', methods=['POST'])
def success():
    answer = 0
    log = request.form.get('login')
    pas = request.form.get('password')
    ppas = request.form.get('ppassword')
    cursor.execute("""SELECT * FROM log;""")
    data: list[tuple] = cursor.fetchall()
    for i in data:
        if log == i[1]:
            answer: int = 1
            break
        else:
            answer: int = 0

    if answer == 1:
        return '<h1 style="color: red;">Такой логин уже есть</h1>\
            <a href="/reg"><button>Вернуться</button></a>'
    elif answer == 0:
        if pas == ppas:
            cursor.execute(f"""
                INSERT INTO log(login, password)
                VALUES ('{log}', '{pas}')
            """)
            return '<h1>Вы успешно зарегистрировались</h1>\
                <h2>Вернитесь на страницу авторизации и выполните вход</h2>\
                <a href="/"><button>Вернуться</button></a>'
        else:
            return '<h1 style="color: red;">Пароли не совпадают</h1>\
                <a href="/reg"><button>Вернуться</button></a>'

@app.route('/post')
def post():
    cursor.execute("""SELECT * FROM post;""")
    data: list[tuple] = cursor.fetchall()
    return render_template('post.html', data=data)

@app.route('/add', methods=['POST'])
def added():
    global name
    name = name
    about = request.form.get('about')
    text = request.form.get('text')
    print(about, text)
    cursor.execute(f"""
                INSERT INTO post(about, post, name)
                VALUES ('{about}', '{text}', '{name}')
            """)

    return '<h1>Ваш пост успешно добавлен</h1>\
                <a href="/post"><button>Вернуться</button></a>'

if __name__ == "__main__":
    app.run(port=8090, debug=True)