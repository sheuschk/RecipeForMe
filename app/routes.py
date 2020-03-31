from app import app, db
from flask import Blueprint, render_template, redirect, url_for, flash, jsonify, request
from .forms import CreateForm
from app.models import Cocktail, Ingredient
# from requests import request


@app.route('/')
@app.route('/index')
def index():
    cocktails = Cocktail.query.all()
    ing_dict = {}
    for ct in cocktails:
        ings = ct.ingredients
        ing_dict[ct.name] = ings

    return render_template('home.html', cocktails=cocktails, ingredients=ing_dict)


@app.route('/create', methods=['GET', 'POST'])
def create():
    form = CreateForm()
    if form.validate_on_submit():
        name = form.name.data
        desc = form.desc.data
        ing_1 = form.ing_name_1.data
        quant_1 = form.quantity_1.data
        if Cocktail.query.filter_by(name=name).all():
            flash("Cocktail already exists")
            return redirect(url_for('.create'))
        try:
            cocktail = Cocktail(name=name, desc=desc)
            print(cocktail.name, type(cocktail.name))
            db.session.add(cocktail)
            db.session.commit()
            ct = Cocktail.query.filter_by(name=name).first()
            print(ct)
            ing = Ingredient(cocktail_key=ct.key, name=ing_1, quantity=quant_1)
            print(ing)
            db.session.add(ing)
            db.session.commit()
            flash('Cocktail created')
        except:
            flash('Cocktail was not created')
        return redirect(url_for('.index'))

    return render_template('create.html', form=form)


@app.route('/ajax/validate_cocktail/', methods=['GET'])
def validate_cocktail_name():
    taken = False
    ct_name = request.args.get('cocktail_name', None)
    exist = Cocktail.query.filter_by(name=ct_name).first()
    if exist is not None:
        taken = True
    data = {'is_taken': taken}
    return jsonify(data)


"""
def create_blueprint():
    
    blueprint = Blueprint("", __name__, template_folder='templates')
    blueprint.add_url_rule('/', 'index', index)
    blueprint.add_url_rule('/create', 'create', create, methods=['GET', 'POST'])
    return blueprint
"""