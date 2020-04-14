from app import db
from flask_login import current_user, login_required
from flask import render_template, redirect, url_for, flash, jsonify, request

from app.main.forms import CreateForm, EditCocktailForm, EditProfileForm
from app.models import Cocktail, Ingredient, User

from . import bp

@bp.route('/')
@bp.route('/index')
def index():
    cocktails = Cocktail.query.all()
    ing_dict = {}
    for ct in cocktails:
        ings = ct.ingredients
        ing_dict[ct.name] = ings

    return render_template('main/home.html', cocktails=cocktails, ingredients=ing_dict)


@bp.route('/create', methods=['GET', 'POST'])
@login_required
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
            return redirect(url_for('main.create'))
        try:
            if current_user.is_authenticated:
                print('hi')
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

    return render_template('main/create.html', form=form)


@bp.route('/ajax/validate_cocktail/', methods=['GET'])
def validate_cocktail_name():
    taken = False
    ct_name = request.args.get('cocktail_name', None)
    exist = Cocktail.query.filter_by(name=ct_name).first()
    if exist is not None:
        taken = True
    data = {'is_taken': taken}
    return jsonify(data)


@bp.route('/user/<username>', methods=['GET', 'POST'])
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    cocktails = Cocktail.query.filter_by(user_id=current_user.id).all()
    ing_dict = {}
    for ct in cocktails:
        ings = ct.ingredients
        ing_dict[ct.name] = ings

    return render_template('main/profile.html', user=user, cocktails=cocktails, ingredients=ing_dict, title='Profile')


@bp.route('/cocktail/<name>', methods=['GET', 'POST'])
@login_required
def cocktail(name):
    cocktail = Cocktail.query.filter_by(name=name).first()
    if cocktail is None:
        return redirect('../index')
    if cocktail.user_id != current_user.id:
        return redirect('../index')

    form = EditCocktailForm(obj=cocktail)

    if form.validate_on_submit():
        if form.delete.data:
            Cocktail.query.filter_by(name=cocktail.name).delete()
            Ingredient.query.filter_by(cocktail_key=cocktail.key).delete()
            db.session.commit()
            flash(f'Cocktail {cocktail.name} deleted')
            return redirect('../index')
        else:
            cocktail.name = form.name.data
            cocktail.desc = form.desc.data
            db.session.commit()
            flash('Cocktail got changed')
            return redirect('../index')

    return render_template('main/create.html', form=form)


@bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('main.user', username=current_user.username))
    elif request.method == 'GET':
        form.username.data = current_user.username
    return render_template('main/edit_profile.html', title='Edit Profile',
                           form=form)
