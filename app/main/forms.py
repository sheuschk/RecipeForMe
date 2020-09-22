from flask_wtf import FlaskForm, Form
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, ValidationError, Email, Length
from flask_wtf.file import FileField, FileAllowed, FileRequired
# from flask_uploads import UploadSet, IMAGES
from app.models import User
import wtforms


class Ingredient1Form(Form):
    ing_name_1 = StringField('Ingredient', validators=[Length(max=150)])
    quantity_1 = StringField('Quantity', validators=[Length(max=100)])


class Ingredient2Form(Form):
    ing_name_2 = StringField('Ingredient', validators=[Length(max=150)])
    quantity_2 = StringField('Quantity', validators=[Length(max=100)])


class Ingredient3Form(Form):
    ing_name_3 = StringField('Ingredient', validators=[Length(max=150)])
    quantity_3 = StringField('Quantity', validators=[Length(max=100)])


class Ingredient4Form(Form):
    ing_name_4 = StringField('Ingredient', validators=[Length(max=150)])
    quantity_4 = StringField('Quantity', validators=[Length(max=100)])


class Ingredient5Form(Form):
    ing_name_5 = StringField('Ingredient', validators=[Length(max=150)])
    quantity_5 = StringField('Quantity', validators=[Length(max=100)])


class Ingredient6Form(Form):
    ing_name_6 = StringField('Ingredient', validators=[Length(max=150)])
    quantity_6 = StringField('Quantity', validators=[Length(max=100)])


class Ingredient7Form(Form):
    ing_name_7 = StringField('Ingredient', validators=[Length(max=150)])
    quantity_7 = StringField('Quantity', validators=[Length(max=100)])


class Ingredient8Form(Form):
    ing_name_8 = StringField('Ingredient', validators=[Length(max=150)])
    quantity_8 = StringField('Quantity', validators=[Length(max=100)])


class Ingredient9Form(Form):
    ing_name_9 = StringField('Ingredient', validators=[Length(max=150)])
    quantity_9 = StringField('Quantity', validators=[Length(max=100)])


class Ingredient10Form(Form):
    ing_name_10 = StringField('Ingredient', validators=[Length(max=150)])
    quantity_10 = StringField('Quantity', validators=[Length(max=100)])


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

# images = UploadSet('images', IMAGES)


class CreateForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(max=150)])
    desc = StringField('Description', validators=[DataRequired(), Length(max=500)])

    ingredients = wtforms.FormField(AllIngredientForm)

    picture = FileField(validators=[FileAllowed(['jpg', 'png'], 'Images only!')])

    submit = SubmitField('Create')
    delete = SubmitField('Delete')


class EditRecipeForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(max=150)])
    desc = StringField('Description', validators=[DataRequired(), Length(max=500)])
    picture = FileField(validators=[FileAllowed(['jpg', 'png'], 'Images only!')])

    submit = SubmitField('Submit')
    delete = SubmitField('Delete')


class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Submit')
    delete = SubmitField('Delete')

    def __init__(self, original_username, original_mail, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username
        self.original_mail = original_mail

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        if email.data != self.original_mail:
            mail = User.query.filter_by(email=self.email.data).first()
            if mail is not None:
                raise ValidationError('Please use a different mail adresse.')


class SearchForm(FlaskForm):
    term = StringField('Search', validators=[DataRequired()])
    filter = SelectField(u'Cocktail', choices=[('Cocktail', 'Cocktail'), ('Ingredient', 'Ingredient')])
    submit = SubmitField('Search')
