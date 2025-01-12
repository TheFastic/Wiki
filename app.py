from flask import *
import sqlite3

app = Flask(__name__)

app.config['SECRET_KEY'] = "dfbfdberggee444"


def getConnection():
    conn = sqlite3.connect("users.db")
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/')
def index():
    login = session.get('login')
    return render_template('index.html', login = login)
    

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        login = request.form['login']
        password = request.form['password']
        conn = getConnection()
        user = conn.execute("SELECT * FROM info_perso WHERE login = ? AND password = ?", (login, password)).fetchone()
        if user:
            session['login'] = user['login']
            return redirect(url_for('index'))
        else:
            flash("Логін або пароль не вірний")
            return redirect(url_for('login'))
    
    return render_template('login.html')


@app.route('/signup', methods = ['GET', 'POST'])
def signup():
    if request.method == 'POST':
        login = request.form['login']
        password = request.form['password']
        confirmPassword = request.form['confirm_password']
        if password != confirmPassword:
            flash("Паролі не співпадають")
            return redirect(url_for('signup'))
        conn = getConnection()
        user = conn.execute("SELECT * FROM info_perso WHERE login = ? AND password = ?", (login, password)).fetchone()
        if user:
            flash("Такий користувач уже є")
            conn.close()
            return redirect(url_for('signup'))
        conn.execute("INSERT INTO info_perso (login, password) VALUES (?, ?)", (login, password))
        conn.commit()
        conn.close()
        return redirect(url_for('login'))
    
    return render_template('signup.html')

@app.route('/logout')
def logout():
    session.pop('login', None)
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run()