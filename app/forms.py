from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired


class CreateForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    desc = StringField('Description', validators=[DataRequired()])
    ing_name_1 = StringField('Ingredient', validators=[DataRequired()])
    quantity_1 = StringField('Quantity', validators=[DataRequired()])
    submit = SubmitField('Create')
