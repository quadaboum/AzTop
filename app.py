import os
import psycopg2
from flask import Flask, render_template, request, redirect, url_for, flash, session, abort
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'CHANGEMOI_VITE')

def get_db_connection():
    return psycopg2.connect(
        host=os.getenv("PGHOST"),
        database=os.getenv("PGDATABASE"),
        user=os.getenv("PGUSER"),
        password=os.getenv("PGPASSWORD"),
        port=os.getenv("PGPORT", 5432)
    )

def is_logged_in():
    return 'user_id' in session

def is_admin():
    return session.get('is_admin', False)

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not is_logged_in():
            flash("Merci de te connecter.", "warning")
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated

def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not is_logged_in() or not is_admin():
            abort(403)
        return f(*args, **kwargs)
    return decorated

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if is_logged_in():
        return redirect(url_for('menu'))
    if request.method == 'POST':
        pseudo = request.form['username']
        password = request.form['password']
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, password, is_admin FROM "user" WHERE pseudo = %s", (pseudo,))
        user = cur.fetchone()
        if user and check_password_hash(user[1], password):
            session['user_id'] = user[0]
            session['username'] = pseudo
            session['is_admin'] = user[2]
            # Log de connexion (user_log)
            cur.execute("INSERT INTO user_log (user_id, ip, user_agent) VALUES (%s, %s, %s)", (
                user[0], request.remote_addr, request.user_agent.string))
            conn.commit()
            conn.close()
            flash("Connecté avec succès!", "success")
            return redirect(url_for('menu'))
        else:
            conn.close()
            flash("Identifiants incorrects.", "danger")
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if is_logged_in():
        return redirect(url_for('menu'))
    if request.method == 'POST':
        pseudo = request.form['username']
        password = request.form['password']
        code = request.form['code']
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT id FROM "user" WHERE pseudo = %s", (pseudo,))
        if cur.fetchone():
            flash("Ce pseudo existe déjà.", "danger")
            conn.close()
            return render_template('register.html')
        # Vérification code invitation valide
        cur.execute("SELECT id, is_used FROM invite_code WHERE code = %s", (code,))
        code_row = cur.fetchone()
        if not code_row or code_row[1]:
            flash("Code d'invitation invalide ou déjà utilisé.", "danger")
            conn.close()
            return render_template('register.html')
        hash_pw = generate_password_hash(password)
        cur.execute("INSERT INTO "user" (pseudo, password, is_admin, invite_code) VALUES (%s, %s, %s, %s) RETURNING id", (pseudo, hash_pw, False, code))
        user_id = cur.fetchone()[0]
        cur.execute("UPDATE invite_code SET is_used = TRUE, used_by = %s, used_at = %s WHERE id = %s", (user_id, datetime.now(), code_row[0]))
        conn.commit()
        conn.close()
        flash("Compte créé ! Connecte-toi.", "success")
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    session.clear()
    flash("Déconnecté !", "info")
    return redirect(url_for('login'))

@app.route('/menu')
@login_required
def menu():
    return render_template('menu.html')

@app.route('/dashboard')
@admin_required
def dashboard():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*), COALESCE(SUM(donations),0), COALESCE(SUM(prestige),0) FROM "user"")
    nb_users, total_dons, total_prestige = cur.fetchone()
    cur.execute("SELECT COUNT(*) FROM user_log")
    nb_logins = cur.fetchone()[0]
    stats = {
        'nb_users': nb_users,
        'total_dons': total_dons,
        'total_prestige': total_prestige,
        'nb_logins': nb_logins
    }
    conn.close()
    return render_template('dashboard.html', stats=stats)

@app.errorhandler(403)
def forbidden(e):
    return render_template('unauthorized.html'), 403

@app.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404

if __name__ == "__main__":
    app.run(debug=True)
