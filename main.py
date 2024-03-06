from flask import Flask, render_template, request, url_for, redirect, flash
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

# To create a secret key
import os

# Using JSON for data
import json

import utils as util

# import recipeadd
from forms import RecipeAdd

# Database
from models import db
from models.category import Category
from models.recipe import Recipe

# loads default recipe data
from default_data import create_default_data

app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY',
                                          'default_secret_key')

# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///recipes.db'
db.init_app(app)

#=================== ROUTES ===================#


@app.route('/')
def index():
  title = "Home"
  return render_template("index.html", title=title)


@app.route('/about')
def about():
  title = "About"
  return render_template("about.html", title=title)


@app.route('/hipster')
def hipster():
  title = "Hipster"
  return render_template("hipster.html", title=title)


@app.route('/coffee')
def coffee():
  title = "Coffee"
  return render_template("coffee.html", title=title)


#----- Movie dictionary -----#
movie_dict = [{
    "title": "Napoleon",
    "genre": "Drama",
    "rating": 5
}, {
    "title": "Oppenheimer",
    "genre": "Drama",
    "rating": 4.5
}, {
    "title": "Saltburn",
    "genre": "Horror",
    "rating": 3
}, {
    "title": "Barbie",
    "genre": "Comedy",
    "rating": 2
}, {
    "title": "John Wick 4",
    "genre": "Action",
    "rating": 1.5
}]

# Variable that holds the movie.stars function that movie_dict passes thru
movie_dict = util.movie_stars(movie_dict)


@app.route('/movies')
def movies():

  context = {"title": "Movies", "movies": movie_dict}

  return render_template("movies.html", **context)


#----- Form Page -----#
@app.route('/register', methods=['GET', 'POST'])
def register():
  title = "Register"
  feedback = None
  if request.method == 'POST':
    feedback = register_data(request.form)

  context = {"title": title, "feedback": feedback}
  return render_template('register.html', **context)


# Replace _ with space,
# Title case key and value, excludes email and bio from title case
# Lists all hobbies selected
def register_data(form_data):
  return [
      f"{key.replace('_', ' ').replace('[]', '').title()}: {', '.join(map(str, form_data.getlist(key))).title()}"
      if key == 'hobbies[]' else
      f"{key.replace('_', ' ').title()}: {value.title()}" if key.lower()
      not in ['email', 'bio'] else f"{key.replace('_', ' ').title()}: {value}"
      for key, value in form_data.items()
  ]

# --- Recipe add_form route with feedback ---

@app.route('/add_recipe', methods=['GET', 'POST'])
def add_recipe():
    form = RecipeAdd()

    # Populate the category choices dynamically
    form.category_id.choices = [(category.id, category.name) for category in Category.query.all()]

    if request.method == 'POST' and form.validate_on_submit():
        # Create a new recipe instance and add it to the database
        new_recipe = Recipe(
            name=form.name.data,
            author=form.author.data,
            description=form.description.data,
            ingredients=form.ingredients.data,
            instructions=form.instructions.data,
            rating=form.rating.data,
            category_id=form.category_id.data
        )
        db.session.add(new_recipe)
        db.session.commit()

        #inform user of success!
        flash('Recipe added successfully!', 'success')
        return redirect(url_for('recipes'))

    #form did NOT validate
    if request.method == 'POST' and not form.validate():
          for field, errors in form.errors.items():
              for error in errors:
                  flash(f"Error in {field}: {error}", 'error')
          return render_template('add_recipe.html', form=form)

    #default via GET shows form  
    return render_template('add_recipe.html', form=form)


#----- Recipes Page -----#
@app.route("/recipes")
def recipes():
  all_recipes = Recipe.query.all()
  title = "Recipes"
  context = {"title": title, "recipes": all_recipes}
  return render_template("recipes.html", **context)


#----- Recipe Page -----#
@app.route("/recipe/<int:recipe_id>")
def recipe(recipe_id):
  this_recipe = db.session.get(Recipe, recipe_id)
  title = "Recipe"
  context = {"title": "Recipe", "recipe": this_recipe}
  if this_recipe:
    return render_template('recipe.html', **context)
  else:
    return render_template("404.html", title="404"), 404


# ---- old code -----
# used list comprehension to simplify code
# def register_data(form_data):
#   return [f"{key}: {value}" for key, value in form_data.items()]

# ---- old code -----
# def register_data(form_data):
#   feedback = []
#   for key, value in form_data.items():
#     feedback.append(f"{key}: {value}")
#   return feedback


#----- Users Page -----#
@app.route('/users')
def users():

  # Read project data from JSON file (test.json)
  with open('test.json') as json_file:
    user_data = json.load(json_file)
    print(user_data)

  context = {"title": "Users", "users": user_data}

  return render_template("users.html", **context)


#----- User Page -----#
@app.route('/user/<int:user_number>')
def show_user(user_number):
  this_user = load_user_data(user_number)
  if this_user:
    title = "User"
    context = {"title": title, "user": this_user}
    return render_template("user.html", **context)
  else:
    return 'User not found', 404


def load_user_data(user_number):
  # Read project data from JSON file
  with open('test.json') as json_file:
    user_data = json.load(json_file)
    user = next((u for u in user_data if u['id'] == user_number), None)
    return user


# ----- old code -----
# @app.route('/user/<int:user_number>')
# def user(user_number):
#   # Read project data from JSON file
#   with open('test.json') as json_file:
#       user_data = json.load(json_file)
#       this_user = user_data[user_number]
#   title = "User"
#   context = {
#     "title": title,
#     "user":  this_user
#   }
#   return render_template("user.html", **context)

# ----- old code -----
# @app.route('/user/<int:user_number>')
# def user(user_number):
#   return f'Content for User {user_number}'


class RecipeView(ModelView):
  column_searchable_list = ['name', 'author']


# Admin page
admin = Admin(app)
admin.url = '/admin/'  #would not work on repl w/o this!
admin.add_view(RecipeView(Recipe, db.session))
admin.add_view(ModelView(Category, db.session))

#----- Database -----#
with app.app_context():
  db.create_all()

  # !! Remove this code to add your own data instead of default data
  #removes all data and loads defaults:
  create_default_data(db, Recipe, Category)

app.run(host='0.0.0.0', port=81)
