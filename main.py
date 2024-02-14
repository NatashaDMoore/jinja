from flask import Flask, render_template, request, url_for

# To create a secret key
import os

# Using JSON for data
import json

app = Flask(__name__)

import utils as util

app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY',
                                          'default_secret_key')


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


# Route for the form page
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


# Route for the users page
@app.route('/users')
def users():

  # Read project data from JSON file (test.json)
  with open('test.json') as json_file:
    user_data = json.load(json_file)
    print(user_data)

  context = {"title": "Users", "users": user_data}

  return render_template("users.html", **context)


# View page for each user
@app.route('/user/<int:user_number>')
def user(user_number):
  return f'Content for User {user_number}'


app.run(host='0.0.0.0', port=81)
