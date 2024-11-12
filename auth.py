from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from database import get_db_connection

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        password_hash = generate_password_hash(password)

        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
            user = cursor.fetchone()

            if user:
                flash("Gebruikersnaam bestaat al.", "error")
            else:
                cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password_hash))
                conn.commit()
                flash("Registratie succesvol, je kunt nu inloggen.", "success")
                return redirect(url_for('auth.login'))

    return render_template('register.html')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        with get_db_connection() as conn:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
            user = cursor.fetchone()

        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['role'] = user['role']
            flash("Succesvol ingelogd!", "success")
            return redirect(url_for('app_routes.index'))
        else:
            flash("Ongeldige gebruikersnaam of wachtwoord.", "error")

    return render_template('login.html')

@auth.route('/logout')
def logout():
    session.pop('user_id', None)
    flash("Je bent uitgelogd.", "success")
    return redirect(url_for('auth.login'))

