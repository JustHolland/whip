import models

from flask import Blueprint, request, jsonify
from playhouse.shortcuts import model_to_dict
from flask_login import current_user

API_KEY = os.environ.get("SPOONACULAR_KEY")


@recipe.route('/', methods=['GET', 'POST'])
def recipes():
    if request.method == 'POST':
        content = requests.get(
            "https://api.spoonacular.com/recipes/findByIngredients?ingredients=" +
            convert_input(request.form['restaurant_name']) +
            "&apiKey=" + API_KEY)
        json_response = json.loads(content.text)
        print json_response
        return render_template("restaurant_list.html", response=json_response) if json_response != [] else render_template(
            "restaurant_list.html", response="")
    else:
        return render_template("restaurant_list.html")



@recipe.route('https://api.spoonacular.com/recipes/random?apiKey=68d99d68c7e64c0bac45eb3d9dd0faf3', methods=['GET'])
def recipe(recipe_id):
    response = requests.get("https://api.spoonacular.com/recipes/random?apiKey=68d99d68c7e64c0bac45eb3d9dd0faf3)
    return make_response(render_template("recipe_details.html", recipe_id=json.loads(response.text)), 200)




@recipe.route('/api/search_results', methods=["POST"])
def search_results():


    # unencode from JSON
    data = request.get_json()
    # User's input is a string of comma-separated list of ingredients
    input_ingredients_str = data['ingredients']

    # spoonacular's api url
    url = "https://api.spoonacular.com/recipes/complexSearch"
    # api parameters
    payload = {"apiKey": API_KEY,
               "includeIngredients": input_ingredients_str,
               "addRecipeInformation": True,
               "sort": "max-used-ingredients",
               "instructionsRequired": True,
               "fillIngredients": True,
               "number": 15,
               }
    # make http request to spoonacular's complexSearch API
    res = requests.get(url, params=payload)
    # convert json into python dictionary -> API is a List of dictionaries
    data = res.json()
    # list of recipes (which are dictionaries about recipe details)
    recipes_complex_data = data['results']

    recipe_results = []
    # parse only details we need from api endpoint
    for recipe in recipes_complex_data:
        recipe_data = helper_functions.parse_API_recipe_details(recipe)
        recipe_results.spoonend(recipe_data)

    return jsonify(recipe_results)



    https://api.spoonacular.com/recipes/random
