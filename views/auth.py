from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.security import generate_password_hash

from forms.auth_forms import RegistrationForm, LoginForm
from models import db, User

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/')
def index():
    return redirect(url_for('auth.login'))


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        
        if current_user.role == 'Analyst':
            return redirect(url_for('trans.home'))
        elif current_user.role == 'Admin':
            return redirect(url_for('customer.customer_dashboard'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()

        if user and user.check_password(form.password.data):
            login_user(user)
            if user.role == 'Analyst':
                return redirect(url_for('trans.home'))
            elif user.role == 'Admin':
                return redirect(url_for('customer.customer_dashboard'))
        else:
            flash('Invalid email or password', 'danger')

    return render_template('auth/login.html', form=form)


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('auth.index'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        new_user = User(
            name=form.name.data,  
            email=form.email.data.lower(),
            role="Analyst" 
        )
        new_user.set_password(form.password.data)  
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/register.html', form=form)


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
