from flask import Flask, render_template, request, url_for, session, flash
import os
import sqlite3

DATABASE = 'tmp/flsite.db'
DEBUG = True
SECRET_KEY = 'Jvtyio8T8352#$#@$NRGJff34!#$^%^G%Q%^#Q$gqa3w4f'


app = Flask(__name__)
app.config.from_object(__name__)
app.config.update(dict(DATABASE=os.path.join(app.root_path, 'flsite.db')))


app.config['SECRET KEY'] = 'ba151a06598733474d7cacdfdc2fee920a67433e'


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

#  --- APP.GET  ---
create_db()



@app.route("/")
def home():
    return render_template("index.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/register", methods=['POST', 'GET'])
def register():
    
    if request.method == "POST":
        if len(request.form["username"]) > 2:
            flash('Сообщение отправлено', category="success")
        else:
            flash("Произошла ошибка отправки", category="error")
        
        print(request.form)
    return render_template("register.html")



if __name__ == "__main__":
    app.run(debug=True)



