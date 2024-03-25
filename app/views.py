from flask import render_template, request, redirect, url_for, session, flash
from werkzeug.security import check_password_hash, generate_password_hash
from app import app
from api.models import User
from api import db

@app.route('/')
def home():
    """
    Render the home page.
    """
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Handle login functionality.
    """
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password_hash, password):
            session['user_id'] = user.id
            flash('You were successfully logged in', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password', 'error')
            
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    """
    Render the dashboard page for logged-in users.
    """
    if 'user_id' not in session:
        flash('You need to login first', 'error')
        return redirect(url_for('login'))
    
    # Fetch additional data from the database if needed
    # For example, user details, medical records, etc.
    user_id = session['user_id']
    user = User.query.get(user_id)
    
    return render_template('dashboard.html', user=user)
