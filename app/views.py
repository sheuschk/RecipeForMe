from flask import Blueprint, render_template, redirect, url_for, flash
from .forms import CreateForm
from app.models import Cocktail

def index():
    form = CreateForm()
    return render_template('home.html', form=form)


def create():
    form = CreateForm()
    if form.validate_on_submit():

        flash('Cocktail created')
        return redirect(url_for('.index'))

    return render_template('create.html', form=form)
