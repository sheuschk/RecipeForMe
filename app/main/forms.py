from flask_wtf import FlaskForm, Form
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, ValidationError
from app.models import User
import wtforms


class Ingredient1Form(Form):
    ing_name_1 = StringField('Ingredient', validators=[DataRequired()])
    quantity_1 = StringField('Quantity', validators=[DataRequired()])


class Ingredient2Form(Form):
    ing_name_2 = StringField('Ingredient', validators=[DataRequired()])
    quantity_2 = StringField('Quantity', validators=[DataRequired()])


class Ingredient3Form(Form):
    ing_name_3 = StringField('Ingredient')
    quantity_3 = StringField('Quantity')


class Ingredient4Form(Form):
    ing_name_4 = StringField('Ingredient')
    quantity_4 = StringField('Quantity')


class Ingredient5Form(Form):
    ing_name_5 = StringField('Ingredient')
    quantity_5 = StringField('Quantity')


class Ingredient6Form(Form):
    ing_name_6 = StringField('Ingredient')
    quantity_6 = StringField('Quantity')


class Ingredient7Form(Form):
    ing_name_7 = StringField('Ingredient')
    quantity_7 = StringField('Quantity')


class Ingredient8Form(Form):
    ing_name_8 = StringField('Ingredient')
    quantity_8 = StringField('Quantity')


class Ingredient9Form(Form):
    ing_name_9 = StringField('Ingredient')
    quantity_9 = StringField('Quantity')


class Ingredient10Form(Form):
    ing_name_10 = StringField('Ingredient')
    quantity_10 = StringField('Quantity')


class AllIngredientForm(Form):
    ingredient1 = wtforms.FormField(Ingredient1Form)
    ingredient2 = wtforms.FormField(Ingredient2Form)
    ingredient3 = wtforms.FormField(Ingredient3Form)
    ingredient4 = wtforms.FormField(Ingredient4Form)
    ingredient5 = wtforms.FormField(Ingredient5Form)
    ingredient6 = wtforms.FormField(Ingredient6Form)
    ingredient7 = wtforms.FormField(Ingredient7Form)
    ingredient8 = wtforms.FormField(Ingredient8Form)
    ingredient9 = wtforms.FormField(Ingredient9Form)
    ingredient10 = wtforms.FormField(Ingredient10Form)


class CreateForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    desc = StringField('Description', validators=[DataRequired()])

    # ing_name_1 = StringField('Ingredient', validators=[DataRequired()])
    # quantity_1 = StringField('Quantity', validators=[DataRequired()])
    #
    # ing_name_2 = StringField('Ingredient', validators=[DataRequired()])
    # quantity_2 = StringField('Quantity', validators=[DataRequired()])
    #
    # ing_name_3 = StringField('Ingredient')
    # quantity_3 = StringField('Quantity')


    ingredients = wtforms.FormField(AllIngredientForm)

    submit = SubmitField('Create')
    delete = SubmitField('Delete')


class EditCocktailForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    desc = StringField('Description', validators=[DataRequired()])

    submit = SubmitField('Submit')
    delete = SubmitField('Delete')


class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    submit = SubmitField('Submit')

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError('Please use a different username.')

