# forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FloatField, SelectField, DecimalField, SubmitField, PasswordField, validators

from wtforms.validators import InputRequired

from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired


# RECIPE ADD FORM
class RecipeAdd(FlaskForm):
  name = StringField('Name', validators=[InputRequired()])
  author = StringField('Author')
  description = TextAreaField('Description')
  ingredients = TextAreaField('Ingredients', validators=[InputRequired()])
  instructions = TextAreaField('Instructions', validators=[InputRequired()])
  rating = FloatField('Rating')
  category_id = SelectField('Category',
                            coerce=int,
                            validators=[InputRequired()])


# RECIPE EDIT FORM
class RecipeEdit(FlaskForm):
  name = StringField('Name', validators=[validators.DataRequired()])
  description = TextAreaField('Description',
                              validators=[validators.DataRequired()])
  ingredients = TextAreaField('Ingredients',
                              validators=[validators.DataRequired()])
  instructions = TextAreaField('Instructions',
                               validators=[validators.DataRequired()])
  category_id = SelectField('Category',
                            coerce=int,
                            validators=[validators.DataRequired()])
  rating = DecimalField('Rating',
                        validators=[validators.NumberRange(min=0, max=5)])


# LOGIN FORM
class LoginForm(FlaskForm):
  email = StringField(
      'Email', validators=[validators.DataRequired(),
                           validators.Email()])
  password = PasswordField('Password', validators=[validators.DataRequired()])
  submit = SubmitField('Login')


# REGISTRATION FORM
class RegistrationForm(FlaskForm):
  first_name = StringField('First Name',
                           validators=[validators.DataRequired()])
  last_name = StringField('Last Name', validators=[validators.DataRequired()])
  email = StringField(
      'Email', validators=[validators.DataRequired(),
                           validators.Email()])
  password = PasswordField('Password', validators=[validators.DataRequired()])
  confirm_password = PasswordField('Confirm Password',
                                   validators=[
                                       validators.DataRequired(),
                                       validators.EqualTo(
                                           'password',
                                           message='Passwords must match')
                                   ])
  submit = SubmitField('Register')


# FORM TO UPLOAD RECIPE PIC
class RecipePicForm(FlaskForm):
  picture = FileField('Recipe Picture',
                      validators=[
                          DataRequired(),
                          FileAllowed(['jpg'], 'Only JPG files allowed.')
                      ])
