from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from .models import User, Clat
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
import json

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        # first_name = request.form.get('')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist', category='error')

    return render_template("login.html", user=current_user)



@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('name')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        elif email == "":
            flash('You must provide an email.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 4 characters.', category='error')
        elif len(name) < 2:
            flash('First Name must be greater than 1 characters.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password at least 7 characters.', category='error')
        else:   # add user to database
            new_user = User(email=email, name=name, password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))

    return render_template("sign-up.html", user=current_user)



@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('views.home'))
    


@auth.route('/delete-account', methods=['GET','POST'])
def delete_user():
    try:
        delete_user = User.query.filter_by(id=current_user.id).first()
        db.session.delete(delete_user)
        flash("Account deleted!", category='success')
        db.session.commit()
    except EOFError:
        flash("error!", category='error')
    return redirect(url_for('views.home'))



# Clat authentication

@auth.route('/create-clat', methods=['GET', 'POST'])
@login_required
def create_clat():
    if request.method == 'POST':
        clatname = request.form.get('clatname')
        clatpassword1 = request.form.get('clatpassword1')
        clatpassword2 = request.form.get('clatpassword2')

        clat = Clat.query.filter_by(clatname=clatname).first()
        if clat:
            flash('Clat name already exists.', category='error')
        elif clatname == "":
            flash('You must provide a Clat name.', category='error')
        elif clatpassword1 != clatpassword2:
            flash('Passwords don\'t match.', category='error')
        elif len(clatpassword1) < 7:
            flash('Password at least 7 characters.', category='error')
        else:   # add clat to database
            new_clat = Clat(clatname=clatname, clatpassword=generate_password_hash(clatpassword1, method='sha256'))
            db.session.add(new_clat)
            db.session.commit()
            flash('Clat created!', category='success')
            return redirect(url_for('views.home'))

    return render_template("create.html", user=current_user)



@auth.route('/', methods=['GET','POST'])
def enter_clat():
    if request.method == 'POST':
        clatname = request.form.get('clatname')
        password = request.form.get('password')

        clat = Clat.query.filter_by(clatname=clatname).first()
        if clat:
            if check_password_hash(clat.password, password):
                flash('Entered successfully!', category='success')
                return redirect(url_for('views.notes'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Clat does not exist', category='error')

    return render_template("home.html", user=current_user)
