from app.auth import bp
from flask import render_template, request, session, redirect, url_for, flash
from app.auth.forms import Login, Register
from app.models import Person
from app import db

from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user

from app import login_manager


@login_manager.user_loader
def load_user(user_id):
    return Person.query.get(int(user_id))


@bp.route('/login', methods=('GET', 'POST'))
def login():
    form = Login(request.form, meta={'csrf_context': session})
    if request.method == 'POST' and form.validate():
        email = request.form['email']
        password = request.form['password']
        remember = True if request.form.get('remember') else False
        user = Person.query.filter_by(email=email).first()

        # Check if the user actually exists
        if not user or not check_password_hash(user.password, password):
            flash('Please check your login details and try again.')
            return redirect(url_for('auth.login'))
        login_user(user, remember=remember)
        # Showing the you're logged in thing
        return redirect(url_for('main.profile'))

    return render_template('auth/login.html', form=form)


@bp.route('/register', methods=('GET', 'POST'))
def register():
    form = Register(request.form, meta={'csrf_context': session})
    if request.method == 'POST' and form.validate():
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        retypePass = request.form['passConfirm']

        # Check if retypePass match
        if password != retypePass:
            return redirect(
                'register',
                flash('Password unmatched')
            )

        # If this returns, email already in database
        user = Person.query.filter_by(email=email).first()
        # If so - reload again the page so user can try again
        if user:
            flash('email already exists')
            return redirect(url_for('auth.register'))

        new_user = Person(
            email=email,
            username=username,
            password=generate_password_hash(password))

        # add the new user to the database
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)


@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))
