# models/__init__.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from models import db
from models.category import Category
from models.recipe import Recipe
from models.chef import Chef
