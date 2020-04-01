from flask_wtf import FlaskForm, Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired
import wtforms


class Ingredient3Form(Form):
    ing_name_3 = StringField('Ingredient')
    quantity_3 = StringField('Quantity')


class Ingredient4Form(Form):
    ing_name_4 = StringField('Ingredient')
    quantity_4 = StringField('Quantity')


class Ingredient5Form(Form):
    ing_name_5 = StringField('Ingredient')
    quantity_5 = StringField('Quantity')
    """
    ing_name_6 = StringField('Ingredient')
    quantity_6 = StringField('Quantity')
    ing_name_7 = StringField('Ingredient')
    quantity_7 = StringField('Quantity')
    ing_name_8 = StringField('Ingredient')
    quantity_8 = StringField('Quantity')
    ing_name_9 = StringField('Ingredient')
    quantity_9 = StringField('Quantity')
    ing_name_10 = StringField('Ingredient')
    quantity_10 = StringField('Quantity')
    """


class AllIngredientForm(Form):
    ingredient3 = wtforms.FormField(Ingredient3Form)
    ingredient4 = wtforms.FormField(Ingredient4Form)
    ingredient5 = wtforms.FormField(Ingredient5Form)


class CreateForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    desc = StringField('Description', validators=[DataRequired()])
    ing_name_1 = StringField('Ingredient', validators=[DataRequired()])
    quantity_1 = StringField('Quantity', validators=[DataRequired()])
    ing_name_2 = StringField('Ingredient', validators=[DataRequired()])
    quantity_2 = StringField('Quantity', validators=[DataRequired()])

    ingredients = wtforms.FormField(AllIngredientForm)

    submit = SubmitField('Create')

