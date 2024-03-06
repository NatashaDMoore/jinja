# forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FloatField, SelectField
from wtforms.validators import InputRequired


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
