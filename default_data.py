# default_data.py

# Create default recipes
DEFAULT_RECIPES = [
    {
        'name': 'Green Eggs and Ham',
        'author': 'Dr. Seuss',
        'description': 'A classic dish from a classic book',
        'ingredients': 'Eggs, Ham, Food coloring',
        'instructions':
        'Cook the eggs and ham. Add green food coloring for fun!',
        'rating': 5.0,
        'category_name': 'Breakfast'
    },
    {
        'name': 'Spaghetti Ice Cream',
        'author': 'Chef Playful',
        'description': 'Sweet and cold spaghetti-inspired ice cream',
        'ingredients':
        'Vanilla ice cream, Strawberry sauce, White chocolate shavings, Gummy worms',
        'instructions':
        'Scoop vanilla ice cream, drizzle with strawberry sauce, sprinkle with white chocolate shavings, and top with gummy worms.',
        'rating': 4.5,
        'category_name': 'Dessert'
    },
    {
        'name': 'Invisible Sandwich',
        'author': 'The Vanishing Chef',
        'description': 'A sandwich that\'s so good, it\'s almost invisible',
        'ingredients':
        'Two slices of imaginary bread, secret sauce, mystery meat, lettuce pray',
        'instructions':
        'Assemble the sandwich with the imaginary ingredients.',
        'rating': 4.2,
        'category_name': 'Lunch'
    },
    {
        'name': 'Banana Dolphin',
        'author': 'Fruit Artist',
        'description': 'Turn a banana into a fun and edible dolphin',
        'ingredients': 'Banana, Chocolate chips, Blueberries',
        'instructions':
        'Peel the banana, add chocolate chips for eyes, and blueberries for water splashes.',
        'rating': 4.8,
        'category_name': 'Dessert'
    },
    {
        'name': 'Pancake Art',
        'author': 'Creative Cook',
        'description': 'Create your own pancake masterpiece',
        'ingredients':
        'Pancake batter, Food coloring, Toppings like syrup, Whipped cream, Sprinkles',
        'instructions':
        'Pour pancake batter into creative shapes, add food coloring, and decorate with toppings.',
        'rating': 4.6,
        'category_name': 'Breakfast'
    },
    {
        'name': 'Rainbow Grilled Cheese',
        'author': 'Colorful Chef',
        'description': 'Add a burst of color to your grilled cheese sandwich',
        'ingredients':
        'Bread, Various colors of food coloring, Favorite cheese',
        'instructions':
        'Dye the bread with different colors, assemble the sandwich, and grill until the cheese melts.',
        'rating': 4.4,
        'category_name': 'Lunch'
    },
    {
        'name': 'Bubblegum Soup',
        'author': 'Bazooka Joe',
        'description': 'A soup that\'s as fun to chew as it is to eat',
        'ingredients': 'Chicken broth, Vegetables, Surprise bubblegum treat',
        'instructions':
        'Prepare chicken broth with vegetables and surprise your guests with a hidden bubblegum treat in each bowl.',
        'rating': 4.7,
        'category_name': 'Dinner'
    },
    # Add more default recipes as needed
]


def create_default_data(db, Recipe, Category):
  with db.session():

    #clear previous records
    db.session.query(Category).delete()
    db.session.commit()

    db.session.query(Recipe).delete()
    db.session.commit()

    # Create default categories
    default_categories = [
        'Breakfast', 'Lunch', 'Dinner', 'Dessert', 'Salad', 'Side Dish'
    ]
    for category_name in default_categories:
      category = Category.query.filter_by(name=category_name).first()
      if not category:
        new_category = Category(name=category_name)
        db.session.add(new_category)
        db.session.commit()

    for recipe_data in DEFAULT_RECIPES:
      category_name = recipe_data.pop('category_name')
      category = Category.query.filter_by(name=category_name).first()
      if not category:
        raise Exception(f"Category '{category_name}' not found.")

      recipe = Recipe.query.filter_by(name=recipe_data['name']).first()
      if not recipe:
        new_recipe = Recipe(category=category, **recipe_data)
        db.session.add(new_recipe)
        db.session.commit()
