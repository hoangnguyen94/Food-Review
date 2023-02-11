import json
import requests
import os
from flask import Flask, render_template, request, flash, redirect, session, g, abort, jsonify

from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError

from forms import CreateUserForm, LoginForm
from models import db, connect_db, User, Food, Like

CURR_USER_KEY = "curr_user"
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = (os.environ.get('DATABASE_URL', 'postgresql:///mealplan_app'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = True

connect_db(app)

db.create_all()



food_data_list = []
DEFAULT_IMAGE = "https://media.istockphoto.com/id/1170315961/ja/%E3%82%B9%E3%83%88%E3%83%83%E3%82%AF%E3%83%95%E3%82%A9%E3%83%88/%E7%99%BD%E3%81%84%E3%83%97%E3%83%AC%E3%83%BC%E3%83%88%E6%9C%A8%E8%A3%BD%E3%81%AE%E3%83%86%E3%83%BC%E3%83%96%E3%83%AB%E3%83%86%E3%83%BC%E3%83%96%E3%83%AB%E3%82%AF%E3%83%AD%E3%82%B9%E7%B4%A0%E6%9C%B4%E3%81%AA%E6%9C%A8%E8%A3%BD%E3%82%AF%E3%83%AA%E3%83%BC%E3%83%B3%E3%82%B3%E3%83%94%E3%83%BC%E3%83%95%E3%83%AA%E3%83%BC%E3%83%94%E3%83%83%E3%82%AF%E3%83%86%E3%83%BC%E3%83%96%E3%83%AB%E3%83%88%E3%83%83%E3%83%97%E3%83%93%E3%83%A5%E3%83%BC%E5%A3%81%E7%B4%99%E7%9A%BF%E5%A3%81%E7%94%BB%E9%8A%80%E5%99%A8.jpg?s=612x612&w=0&k=20&c=wGIdkGONfE87AOQDYGHOF8lmiuFoXdniWHIl2eriLr0="
app.config['SECRET_KEY'] = "DON'T LET THE DOG OUT"


toolbar = DebugToolbarExtension()

#########################################################################
#User signup/login/logout


@app.before_request
def add_user_to_g():
    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])
    
    else:
        g.user = None

def do_login(user):
    """Log in user."""

    session[CURR_USER_KEY] = user.id

def do_logout():
    "Logout user."

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]

def get_food_data(ingredient):
    food_data_list.clear()
    app_id = '685a7401'
    app_key = '24937440d6b1944acfa1858a4445ea97'
    
    url = 'https://api.edamam.com/api/food-database/parser?ingr=' + ingredient + '&app_id=' + app_id + '&app_key=' + app_key
    response = requests.get(url)
    return response.json()

@app.route('/signup', methods=["GET", "POST"])
def signup():
    """Handle user signup.
    Create new user and add to DB. Redirect to homepage.
    If form not valid. present form.
    If there already is a user with that username: flash message
    and re-present form."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]

    form = CreateUserForm()

    if form.validate_on_submit():
        try:
            user = User.signup(
                username=form.username.data,
                password=form.password.data,
                email=form.email.data,
                firstname=form.firstname.data,
                lastname=form.lastname.data
            )
            
            db.session.commit()

        except IntegrityError:
            flash("Username already exist.", 'danger')
            return render_template('users/signup.html', form=form)
        
        do_login(user)

        return redirect("/")
    
    else: 
        return render_template('users/signup.html', form=form)

@app.route('/login', methods=["GET", "POST"])
def login():
    """Handle user login"""

    form = LoginForm()

    if form.validate_on_submit():
        user = User.authenticate(form.username.data,
                                form.password.data)
            
        if user:
            do_login(user)
            flash(f"Welcome, {user.username}", 'success')
            return redirect("/")
        flash("Invalid password", 'danger')

    return render_template('users/login.html', form=form)

@app.route('/logout')
def logout():
    """Handle logout user."""

    do_logout()
    flash("Success log out!", 'success')

    return redirect("/login") 

##############################################################################
# Food search

@app.route('/food_search', methods=['GET'])
def food_search():
    # Searching for food
    if g.user is None or not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/login")
    
    else:
        ingredient = request.args.get('q')
        data = get_food_data(ingredient)

        '''save the api data to an array and show on the template'''
        for a_hints in data['hints']:
            '''get the image_url or return default image'''
            image_url = a_hints['food'].get('image') if a_hints['food'].get('image') else DEFAULT_IMAGE

            '''get the nutrition list and return a single item in nutrition'''
            nutritions = a_hints['food'].get('nutrients')
            nutrition_list = []
            for nutrient_name, nutrient_value in nutritions.items():
                nutrition_list.append({'name': nutrient_name, 'value': round(nutrient_value, 2)})

            food_data_list.append({'api_id': a_hints['food'].get('foodId'),
                            'label': a_hints['food'].get('label'),
                            'image_url': image_url,
                            'nutrition': nutrition_list})
            
            user_id = g.user.id

    food_likes = [food.api_id for food in User.query.get(user_id).foods]
    
    return render_template('foods/show.html', food_list=food_data_list, food_likes = food_likes, user_id= user_id)

#############################################################################
# Like and Food database

@app.route('/like', methods=['POST'])
def like():

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    
    api_id = request.json.get('apiId')
    user_id = request.json.get('userId')

    '''Access to the Food data to make a remove the food database'''

    foods = Food.query.filter_by(api_id=api_id).first()
    if foods:
        liked = Like.query.filter_by(user_id=int(user_id), food_id=foods.id).first()
        
        if liked:
            db.session.delete(liked)
            db.session.commit()
        if foods:
            db.session.delete(foods)
            db.session.commit()

            return {'success': True} 
        
    ''' Retrieve the food api from the food_data_list and add to database'''

    food = next((food for food in food_data_list if food['api_id'] == api_id), None)
    
    if food:
        new_food = Food(
            api_id= food['api_id'],
            user_id=user_id,
            label=food['label'],
            image_url = food['image_url'], 
            nutrition=json.dumps(food['nutrition'])) 
        db.session.add(new_food)
        db.session.commit()
          
    if like:
        new_like = Like(user_id = user_id,
                        food_id = new_food.id)
        
        db.session.add(new_like)
        db.session.commit()
        return {'success': True}
    
        

 
##############################################################################
# Homepage and error pages

@app.route('/')
def homepage():
    """Show homepage:

    - anon users: no foods
    - logged in: liked food list
    """
    if g.user:
        foods = (Food.query
                  .filter(Food.likes.any(user_id=g.user.id))
                  .all())
        liked = [food.id for food in g.user.likes]

        food_list = []
        
        for food in foods:
            nutrition_list = []
            nutrition = json.loads(food.nutrition)
            
            for item in nutrition:
                name = item['name']
                value = item['value']
                nutrition_list.append({'name' : name, 'value': round(value, 2)})
        
                food_data = {
                    'api_id': food.api_id,
                    'user_id': food.user_id,
                    'label': food.label,
                    'image_url': food.image_url,
                    'nutrition': nutrition_list
                }
                
            food_list.append(food_data)                 
        
        
        return render_template('home.html', foods=food_list, liked=liked)
    
    else:
        return render_template('home-anon.html') 
    
    

@app.errorhandler(404)
def page_not_found(e):
    """404 NOT FOUND page"""

    return render_template('404.html'),  404

##############################################################################
# Turn off all caching in Flask
#   (useful for dev; in production, this kind of stuff is typically
#   handled elsewhere)
#
# https://stackoverflow.com/questions/34066804/disabling-caching-in-flask

@app.after_request
def add_header(req):
    """Add non-caching headers on every request."""

    req.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    req.headers["Pragma"] = "no-cache"
    req.headers["Expires"] = "0"
    req.headers['Cache-Control'] = 'public, max-age=0'
    return req