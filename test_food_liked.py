"""User Food Liked tests."""

# run these tests like:
#
#    python -m unittest test_food_liked.py

import os
import json
from unittest import TestCase
from models import db, User, Food, Like
from bs4 import BeautifulSoup

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///mealplan_test"

# Now we can import app

from app import app, requests

db.drop_all()
db.create_all()

class HomepageTestCase(TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

        self.user = User(username='testuser', password='testpassword', email='testing@test.com', firstname='fname', lastname='lname')
        db.session.add(self.user)
        db.session.commit()

        self.food1 = Food(api_id='1', user_id=self.user.id, label='food1', image_url='image1', nutrition='{"calories": 100, "protein": 10}')
        self.food2 = Food(api_id='2', user_id=self.user.id, label='food2', image_url='image2', nutrition='{"calories": 200, "protein": 20}')
        
        db.session.add_all([self.food1, self.food2])

        self.like1 = Like(user_id=self.user.id, food_id=self.food1.id)
        self.like2 = Like(user_id=self.user.id, food_id=self.food2.id)
        db.session.add_all([self.like1, self.like2])
        db.session.commit()

        
    def test_homepage(self):

        session = requests.Session()

        # Log in
        login_response = session.post('http://localhost:5000/login', data={
            'username': 'testuser',
            'password': 'testpassword'})
        
        if login_response.status_code == 200:
            # Get the home page using the same session
            home_page_response = session.get('http://localhost:5000/')
            # Use the response object to access the content of the home page
            print(home_page_response.text)
        else:
            print("Login failed")
        # Get the homepage
        response = session.get('http://localhost:5000/')
        self.assertEqual(response.status_code, 200)
        
        # Parse the response
        soup = BeautifulSoup(response.text, 'html.parser')
        logout_button = soup.find('a', str='Log out')
    
        print("Content: ", response.content)
        
        print("Headers: ", response.headers)
        
        print("Status Code: ", response.status_code)

        self.assertIsNotNone(logout_button)
        # Check if the food list is present
        food1 = Food.query.filter_by(api_id='1').first()
        food2 = Food.query.filter_by(api_id='2').first()
        food_list = [food1, food2]
        print(response.text)
        # for food in food_list:
        #     food_name = food.label
        #     self.assertTrue(soup.find(string=food_name))
        # self.assertEqual(soup, food_list)
        # with requests.Session() as session:
        #     response = session.post('http://localhost:5000/login', data={
        #     'username': 'testuser',
        #     'password': 'testpassword'
        #     })
        #     soup = BeautifulSoup(response.text, 'html.parser')
        #     print('!!!!!!!!!!!!!!!!!')
        #     print(soup)
        #     self.assertEqual(response.status_code, 200)

        #     response = session.get('http://localhost:5000/')
            
        #     self.assertEqual(response.status_code, 200)
            
        #     soup = BeautifulSoup(response.text, 'html.parser')
        #     print('@@@@@@@@@@@@@@@')
        #     print(soup)
        #     food1 = Food.query.filter_by(api_id='1').first()
        #     food2 = Food.query.filter_by(api_id='2').first()
        #     food_list = [food1, food2]
        #     self.assertEqual(soup, food_list)



        # self.assertIn(str(food1.id), response.data.decode('utf-8'))
        # self.assertIn(str(food2.id), response.data.decode('utf-8'))
        # self.assertIn(food1.label, response.data.decode('utf-8'))
        # self.assertIn(food2.label, response.data.decode('utf-8'))
    # def test_homepage(self):
    #     # Send a post request to the login endpoint
    #     response = self.app.post('/login', data={
    #     'username': 'testuser',
    #     'password': 'testpassword'})

    #     # Check if the response is successful (status code 200)
    #     self.assertEqual(response.status_code, 200)
        
    #     response = self.app.get('/')
    #     self.assertEqual(response.status_code, 200)

        
    #     food1 = Food.query.filter_by(api_id='1').first()
    #     food2 = Food.query.filter_by(api_id='2').first()

    #     food_list = [food1, food2]
    #     print(response.get_json())
    #     self.assertEqual(response.get_json()['foods'], food_list)
    #     self.assertEqual(response.get_json()['foods'], food_list)
        # self.assertEqual(response.get_json['liked'], [self.food1.id, self.food2.id])

    def tearDown(self):
        db.session.remove()
