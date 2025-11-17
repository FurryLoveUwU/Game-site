from flask import Flask, render_template, request, url_for, session, flash, g
import os
import sqlite3
from dotenv import load_dotenv
from FDataBase import FDataBase
from passlib.hash import argon2

load_dotenv()


DATABASE = os.getenv('DATABASE')
DEBUG = True
SECRET_KEY = os.getenv('SECRET_KEY')


app = Flask(__name__)
app.config.from_object(__name__)
app.config.update(dict(DATABASE=os.path.join(app.root_path, 'flsite.db')))




#  --- DEFS  ---

def connect_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn

def create_db():
    db = connect_db()
    with app.open_resource('sq_db.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()

def get_db():
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db

#  --- APP.GET  ---
create_db()



@app.route("/")
def home():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    db = get_db()
    dbase = FDataBase(db)
    if request.method == "POST":

        if len(request.form["username"]) > 2 and len(request.form['password']) > 2:
            try:
                unhash_pass = request.form["password"]
                username = request.form["username"]
                res = dbase.login_account(username, unhash_pass)

                if res == 100:
                    flash("Пользователя не существует. Проверь имя или почту.")
                elif res == 300:
                    flash("Пароль введен не верно.")
                elif res == 200:
                    flash("Вход успешен")
                    session["username"] = username
                else:
                    
                    flash(f"Неизвестная ошибка {res}")

            except:
                pass
    return render_template("login.html")

@app.route("/register", methods=['POST', 'GET'])
def register():
    db = get_db()
    dbase = FDataBase(db)

    
    if request.method == "POST":
        if len(request.form["username"]) and len(request.form["password1"]) > 4:
            try:
                username = (request.form["username"])
                email = (request.form["mail"])

                unsecured_password = (request.form["password1"])
                secured_password = argon2.hash(unsecured_password)
            
                print(username, secured_password, email)
                
                check_status = dbase.register_user(username, secured_password, email)
                if check_status == False:
                    flash("Такой ник или почта уже заняты")
                else:
                    flash("Регистрация успешна")
                    

            except:
                pass






        else:
            flash("Произошла ошибка. Пароль и имя должны содержать минимум 4 символа.", category="error")
        
        print(request.form)
    return render_template("register.html")

@app.route("/profile")
def profile():
    return render_template("profile.html")

if __name__ == "__main__":
    app.run(debug=True)



