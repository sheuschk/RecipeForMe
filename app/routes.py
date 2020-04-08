from app import app, db
from flask_login import current_user, login_user, logout_user, login_required
from flask import Blueprint, render_template, redirect, url_for, flash, jsonify, request
from .forms import CreateForm, LoginForm, RegistrationForm
from app.models import Cocktail, Ingredient, User
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

        ingredients = form.ingredients.data

        for fieldname, value in form.data.items():
            print(fieldname, ": ", value)

        if Cocktail.query.filter_by(name=name).all():
            flash("Cocktail already exists")
            return redirect(url_for('.create'))
        try:
            if current_user:
                cocktail = Cocktail(name=name, desc=desc, user_id=current_user.id)
            else:
                cocktail = Cocktail(name=name, desc=desc)
            print(cocktail.name, type(cocktail.name))
            db.session.add(cocktail)
            db.session.commit()
            ct = Cocktail.query.filter_by(name=name).first()
            print(ct)

            for key in ingredients.keys():
                numb = "".join(x for x in key if x.isdigit())
                name = f"ing_name_{numb}"
                quant = f"quantity_{numb}"
                if key == 'csrf_token':
                    print('token')
                    pass
                elif ingredients[key][quant] == '' or ingredients[key][name] == '':
                    print('pass')
                    pass
                else:
                    print(f"name: {ingredients[key][name]}, quant: {ingredients[key][quant]}")
                    new_ing = Ingredient(cocktail_key=ct.key, name=ingredients[key][name], quantity=ingredients[key][quant])
                    db.session.add(new_ing)

            db.session.commit()
            flash('Cocktail created')
        except:
            Cocktail.query.filter_by(name=name).delete()
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


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


"""
def create_blueprint():
    
    blueprint = Blueprint("", __name__, template_folder='templates')
    blueprint.add_url_rule('/', 'index', index)
    blueprint.add_url_rule('/create', 'create', create, methods=['GET', 'POST'])
    return blueprint
"""