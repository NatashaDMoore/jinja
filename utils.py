# movie_stars function - movie_dict passes thru
def movie_stars(movie_dict):
  for movie in movie_dict:
    movie['stars'] = add_stars(movie['rating'])
  return movie_dict

# add_stars function - rating from movie_dict passes thru
def add_stars(rating):
  my_return = ""
  for x in range(1, 6):
      if rating >= x:
          my_return += "<span class=\"fa fa-star\"></span>"
      elif rating >= x - 0.5:
          my_return += "<span class=\"fa fa-star-half-o\"></span>"
      else:
          my_return += "<span class=\"fa fa-star-o\"></span>"
  return my_return