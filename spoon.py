from flask import Flask, render_template, request
import requests

app = Flask(__name__)
url = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/"
headers = {
  'x-rapidapi-host': "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com",
  'x-rapidapi-key': "68d99d68c7e64c0bac45eb3d9dd0faf3>",
  }
random_joke = "food/jokes/random"
find = "recipes/findByIngredients"
randomFind = "recipes/random"
@app.route('/')
def search_page():
  joke_response = str(requests.request("GET", url + random_joke, headers=headers).json()['text'])
  return render_template('search.html', joke=joke_response)
if __name__ == '__main__':
  app.run()
