from flask import render_template, request, redirect, url_for, session
from quiz_master_v1.controllers.database import db
from main import app
from flask import flash
from quiz_master_v1.controllers.models import User, Admin
from quiz_master_v1.controllers.models import Subjects, Chapters, Questions, Options, QuizDetails, QuizResponse, Scores

@app.route('/admin_login.html', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'GET':
        return render_template('admin_login.html')
    
    if request.method == 'POST':
        # Get the username and password from the form
        username = request.form['username']
        password = request.form['password']

        # Check if both fields are filled
        if not username or not password:
            flash('Username and password are required', 'error')
            return redirect(url_for('admin_login'))

        # Check if the username is valid
        if '@' not in username:
            flash('Invalid username', 'error')
            return redirect(url_for('admin_login'))

        # Fetch admin user from the database
        admin_user = Admin.query.filter_by(username=username).first()

        # Validate credentials
        if admin_user and admin_user.password == password:
            session['admin'] = True  # Set admin session
            return redirect(url_for('hello_world'))  # Redirect to admin dashboard
        else:
            flash('Invalid credentials', 'error')
            return redirect(url_for('admin_login'))
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    if request.method=='POST':
        username=request.form['username']
        password=request.form['password']
        user=User.query.filter_by(username=username).first()
        if user and user.password==password:
            session['user']=True
            return render_template('user.html')
        else:
            flash('Invalid credentials', 'error')
            return redirect(url_for('login'))
@app.route('/user_register',methods=['GET','POST'])
def user_register():
    if request.method == 'GET':
        return render_template('registration.html')
    if request.method == 'POST':
        username=request.form['username']
        fullname=request.form['fullname']
        dob=request.form['dob']
        qualification=request.form['qualification']
        password=request.form['password']
        user=User.query.filter_by(username=username).first()
        if user:
            flash('User already exists','error')
            return redirect(url_for('user_register'))
        user=User(username=username,fullname=fullname,dob=dob,qualification=qualification,password=password)
        db.session.add(user)
        db.session.commit()
        flash('User registered successfully','success')
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('admin', None)
    session.pop('user', None) #clear the session
    flash('you have been logged out','info')
    return redirect(url_for('hello_world'))# Redirect to admin login page

#don't use render template try to use redirect or url_for for homepage
