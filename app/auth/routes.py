from app import db
from flask_login import current_user, login_user, logout_user, login_required
from flask import render_template, redirect, url_for, flash, request

from .forms import LoginForm, RegistrationForm, ResetPasswordForm, ResetPasswordRequestForm, EditProfileForm
from .email import send_password_reset_email
from app.models import User, Recipe, Ingredient
from config import Config

from . import bp

import os


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        print('here')
        return redirect(url_for('main.user', username=current_user.username))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('auth.login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('main.index'))
    return render_template('auth/login.html', title='Sign In', form=form)


@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        login_user(user)
        return redirect(url_for('main.index'))
    return render_template('auth/register.html', title='Register', form=form)


@bp.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash('Check your email for the instructions to reset your password')
        return redirect(url_for('auth.login'))

    return render_template('auth/reset_password_request.html',
                           title='Reset Password', form=form)


@bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('main.index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset.')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html', form=form)


@bp.route('/user/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    """Profile page for User Profile (BAD URL DESIGN)"""
    form = EditProfileForm(current_user.username, current_user.email)
    if form.validate_on_submit():

        # If User wants to delete his account, delete all its recipes
        if form.delete.data:
            cocktails = Recipe.query.filter_by(user_id=current_user.id).all()
            for ct in cocktails:
                if ct.picture:
                    os.path.exists(os.path.join(Config.BASEDIR, 'app', 'static', 'photos', ct.picture))
                    os.remove(os.path.join(Config.BASEDIR, 'app', 'static', 'photos', ct.picture))
                Ingredient.query.filter_by(recipe_key=ct.key).delete()
                Recipe.query.filter_by(name=ct.name).delete()
            User.query.filter_by(username=current_user.username).delete()
            db.session.commit()
            flash('Your account is deleted')
            return redirect(url_for('main.index'))
        # Check if new username is already taken
        if User.query.filter_by(username=form.username.data).all() and form.username.data != current_user.username:
            flash('Changes not saved: Username already exists')
            return redirect(url_for('auth.edit_profile'))

        else:
            # Save new data
            current_user.username = form.username.data
            current_user.email = form.email.data
            db.session.commit()
            flash('Your changes have been saved.')
        return redirect(url_for('main.user', username=current_user.username))

    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template('auth/edit_profile.html', title='Edit Profile',
                           form=form)
