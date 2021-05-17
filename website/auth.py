from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user


auth = Blueprint('auth', __name__)


@auth.route('/log-in', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('ברוכים הבאים!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('הסיסמה שגויה. נסה שנית.', category='error')
        else:
            flash('הEmail לא קיים. נסה שנית.', category='error')

    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        area = request.form.get('area')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('הEmail כבר קיים במערכת.', category='error')
        elif len(email) < 4:
            flash('הEmail חייב להכיל יותר מ3 ספרות.', category='error')
        elif len(first_name) < 2:
            flash('השם הפרטי חייב להכיל לפחות שתי אותיות.', category='error')
        elif password1 != password2:
            flash('הסיסמה אינה נכונה.', category='error')
        elif len(password1) < 7:
            flash('הסיסמה חייבת להכיל לפחות 7 ספרות.', category='error')
        else:
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(
                password1, method='sha256'),area=area)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))

    return render_template("sign_up.html", user=current_user)