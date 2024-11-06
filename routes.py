from functools import wraps
from flask import Blueprint, request, render_template, redirect, url_for, flash, session
from database import (find_kenteken_in_db, add_kenteken_to_db, get_all_autos, update_auto_in_db, delete_auto_from_db)
from rdw_api import get_vehicle_data_from_rdw
import re

app_routes = Blueprint('app_routes', __name__)

# Patterns and constants
KENTEKEN_PATTERN = re.compile(r'^[A-Z0-9]{1,3}-[A-Z0-9]{1,3}-[A-Z0-9]{1,3}$', re.IGNORECASE)
ITEMS_PER_PAGE = 10

# Decorator for requiring login
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash("Log in om deze pagina te zien.", "error")
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@app_routes.route('/')
def index():
    return render_template('index.html')

@app_routes.route('/check_kenteken', methods=['POST'])
def check_kenteken():
    kenteken = request.form.get('kenteken', '').upper()

    if not KENTEKEN_PATTERN.match(kenteken):
        return render_template(
            'index.html',
            error="Ongeldig kentekenformaat. Gebruik bijv. 'A1-12-BCD' of '123-AB-4'."
        )
    
    kenteken_data = find_kenteken_in_db(kenteken)
    if kenteken_data:
        return render_template('result.html', kenteken_data=kenteken_data, gevonden=True)

    vehicle_data = get_vehicle_data_from_rdw(kenteken)
    if vehicle_data:
        add_kenteken_to_db(
            vehicle_data['kenteken'], 
            vehicle_data['merk'], 
            vehicle_data['kleur']
        )
        return render_template('result.html', kenteken_data=vehicle_data, gevonden=True)
    
    return render_template(
        'result.html', 
        kenteken_data={'kenteken': kenteken},
        gevonden=False,
        fout="Kenteken niet gevonden bij RDW"
    )

@app_routes.route('/dashboard')
@login_required
def dashboard():
    autos = get_all_autos()
    return render_template('dashboard.html', autos=autos)

@app_routes.route('/dashboard/update/<kenteken>', methods=['GET', 'POST'])
@login_required
def update_auto(kenteken):
    if session.get('role') != 'admin':
        flash('Je hebt geen toegang om deze actie uit te voeren.', 'error')
        return redirect(url_for('app_routes.dashboard'))
    
    if request.method == 'POST':
        merk = request.form.get('merk')
        kleur = request.form.get('kleur')
        update_auto_in_db(kenteken, merk, kleur)
        return redirect(url_for('app_routes.dashboard'))

    auto = find_kenteken_in_db(kenteken)
    if not auto:
        flash(f"Auto met kenteken {kenteken} is niet gevonden.")
        return redirect(url_for('app_routes.dashboard'))
    
    return render_template('update_auto.html', auto=auto)

@app_routes.route('/dashboard/delete/<kenteken>')
@login_required
def delete_auto(kenteken):
    if session.get('role') != 'admin':
        flash('Je hebt geen toegang om deze actie uit te voeren.', 'error')
        return redirect(url_for('app_routes.dashboard'))

    delete_auto_from_db(kenteken)
    return redirect(url_for('app_routes.dashboard'))

