from flask import render_template, request, flash, redirect, url_for, jsonify
from notes import app, db
import bcrypt
from notes.models import User, Notes
from flask_login import login_user, login_required, current_user, logout_user
import json


@app.route('/')
def func():
    return redirect(url_for('login'))


@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        passw = request.form.get('pass')
        hashed = bcrypt.hashpw(passw.encode('utf-8'), bcrypt.gensalt())
        passw = hashed
        if email and username and passw:
            user = User(username=username, password=passw, email=email)
            db.session.add(user)
            db.session.commit()
            login_user(user, remember=True)
            flash("User Created Successfully", category='user_created')
        return redirect(url_for('mainapp'))
    return render_template('signup.html', user=current_user)


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        passw = request.form.get('pass')
        user = User.query.filter_by(username=username).first()
        if not user or not passw:
            flash("Please Enter Username and Password. Do you want to Sign Up?", category='error')
        else:
            if bcrypt.checkpw(passw.encode('utf-8'), user.password):
                flash("Logged In", category='success')
                login_user(user, remember=True)
                return redirect(url_for('mainapp'))
            else:
                flash("Wrong Something", category='error')
    return render_template('login.html', user=current_user)


@app.route('/mainapp', methods=['POST', 'GET'])
@login_required
def mainapp():
    if request.method == 'POST':
        notes = request.form.get('note')
        if len(notes) < 1:
            flash("Enter a valid note", category='error')
        else:
            post = Notes(content=notes, author_id=current_user.id)
            db.session.add(post)
            db.session.commit()
    return render_template('mainapp.html', user=current_user)


@app.route('/previous-tweets')
@login_required
def previous_tweets():
    return render_template('previous_tweets.html', user=current_user)


@app.route('/delete-tweet', methods=['POST'])
@login_required
def deleteNote():
    note = json.loads(request.data)
    note_id = note['notesID']
    note = Notes.query.get(note_id)
    if note:
        if note.author_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
            return jsonify({})


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Logged Out", category='success')
    return redirect(url_for('login'))


@app.route('/about')
def about():
    return render_template('about.html', user=current_user)
