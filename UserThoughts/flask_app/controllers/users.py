from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models.user import User
from flask_app.models.thought import Thought
from flask import flash
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


@app.route('/loginPage')
def loginPage():    
    if 'user_id' in session:
        return redirect('/')
    return render_template('loginRegistration.html')

@app.route('/createUser', methods=['POST'])
def createUser():
    if not User.validate_user(request.form):
        flash('Somethings wrong!', 'signUp')
        return redirect(request.referrer)
    data = {
        'email': request.form['email'],
        'firstname': request.form['firstname'],
        'lastname': request.form['lastname'],
        'password': bcrypt.generate_password_hash(request.form['password'])
    }
    User.createUser(data)
    return redirect('/loginPage')


@app.route('/login', methods=['POST'])
def login():
    
    data = {
        'email': request.form['email']
    }
    if len(request.form['email'])<1:
        flash('Email is required to login', 'emailLogin')
        return redirect(request.referrer)
    if not User.get_user_by_email(data):
        flash('This email doesnt exist in this application', 'emailLogin')
        return redirect(request.referrer)

    user = User.get_user_by_email(data)

    if not bcrypt.check_password_hash(user['password'], request.form['password']):
        flash("Invalid Password", 'passwordLogin')
        return redirect(request.referrer)
    session['user_id'] = user['id']
    return redirect('/dashboard')

@app.route('/')
def dashboard():
    if 'user_id' in session:
        data = {
            'user_id': session['user_id']
        }
        user = User.get_user_by_id(data)
        allThoughts = Thought.getAllThoughts()
        userLikedThoughts = User.get_logged_user_liked_thoughts(data)
        print(len(userLikedThoughts))
        return render_template('dashboard.html', loggedUser= user, allThoughts = allThoughts , userLikedThoughts= userLikedThoughts)
    return redirect('/logout')

@app.route('/profile/<int:id>')
def profile(id):
    if 'user_id' in session:
        data = {
            'user_id': id
        }
        loggedData={
            'user_id':session['user_id']
        }
        user = User.get_user_by_id(data)
        thoughts = User.get_all_user_info(data)
        return render_template('thought.html', thoughts= thoughts, user= user, loggedUser=User.get_user_by_id(loggedData))
    return redirect('/logout')

@app.route('/logout/')
def logout():
    session.clear()
    return redirect('/loginPage')