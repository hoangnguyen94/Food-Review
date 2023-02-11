"""User login tests."""

# run these tests like:
#
#    python -m unittest test_user_login.py

import os
from unittest import TestCase
from models import db, User

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///mealplan_test"

# Now we can import app

from app import app

db.create_all()

class FoodSearchTestCase(TestCase):
    def setUp(self):
        self.app = app
        self.client = self.app.test_client()

        with self.app.app_context():
            db.drop_all()
            db.create_all()

            # Create a test user and log them in
            user = User(username='testuser', password='testpassword', email='testing@test.com', firstname='fname', lastname='lname')
            db.session.add(user)
            db.session.commit()

    def tearDown(self):
        with self.app.app_context():
            db.drop_all()

    def test_user_login(self):
        # Send a post request to the login endpoint
        response = self.client.post('/login', data={
        'username': 'testuser',
        'password': 'testpassword'
        })
        # Check if the response is successful (status code 200)
        self.assertEqual(response.status_code, 200)