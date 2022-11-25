from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models.thought import Thought
from flask_app.models.user import User


@app.route('/createThought', methods=['POST'])
def createThought():
    if not Thought.validate_thought(request.form):
        return redirect(request.referrer)
    data = {
        'user_id': session['user_id'],
        'description':request.form['description']
        }
    Thought.create_thought(data)
    return redirect('/')

@app.route('/like/<int:id>')
def addLike(id):
    data = {
        'thought_id': id,
        'user_id': session['user_id']
    }
    Thought.like(data)
    return redirect(request.referrer)

@app.route('/unlike/<int:id>')
def removeLike(id):
    data = {
        'thought_id': id,
        'user_id': session['user_id']
    }
    Thought.unlike(data)
    return redirect(request.referrer)

@app.route('/delete/<int:id>')
def deleteThought(id):
    data = {
        'thought_id': id,
    }
    thought = Thought.get_thought_by_id(data)
    if session['user_id']==thought['user_id']:
        Thought.removeAllLikes(data)
        Thought.deleteThought(data)
        return redirect(request.referrer)
    return redirect(request.referrer)

@app.route('/thought/<int:id>')
def singleThought(id):
    data = {
        'thought_id': id,
        'user_id': session['user_id']

    }
    user = User.get_user_by_id(data)
    thought = Thought.get_thought_by_id(data)
    nrLikes=Thought.getthoughtLikes(data)
    return render_template('thought.html', thought=thought, loggedUser=user, nrLikes=nrLikes)