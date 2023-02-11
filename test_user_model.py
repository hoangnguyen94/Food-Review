"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


import os
from unittest import TestCase
from sqlalchemy import exc
from models import db, User


# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///mealplan_test"


# Now we can import app

from app import app

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()

# Don't have WTForms use CSRF at all, since it's a pain to test

app.config['WTF_CSRF_ENABLED'] = False


class UserModelTestCase(TestCase):
    """Test views for foods."""

    def setUp(self):
        """Create test client, add sample data."""

        db.drop_all()
        db.create_all()

        u = User.signup("test1", "password", "email1@test.com", "fname1", "lname1")
        uid = 1111
        u.id = uid

        u = User.query.get(uid)
        
        self.u = u
        self.uid = uid

    def tearDown(self):
        res = super().tearDown()
        db.session.rollback()
        return res


    def test_user_model(self):
        """Does basic model work?"""

        u = User(
            username="testid",
            password="HASHED_PASSWORD",
            email="testing@test.com",
            firstname="test",
            lastname= "testtest"
        )

        db.session.add(u)
        db.session.commit()

        # User should have no messages & no followers
        self.assertEqual(len(u.foods), 0)
        self.assertEqual(len(u.likes), 0)

##################################################################
    # Signup Tests
    
    def test_valid_signup(self):
        u_test = User.signup("tester", "password", "email2@test.com", "fname2", "lname2")
        uid = 99999
        u_test.id = uid
        db.session.commit()

        u_test = User.query.get(uid)
        self.assertIsNotNone(u_test)
        self.assertEqual(u_test.username, "tester")
        self.assertEqual(u_test.email, "email2@test.com")
        self.assertNotEqual(u_test.password, "password")
        self.assertEqual(u_test.firstname, "fname2")
        self.assertEqual(u_test.lastname, "lname2")
        # Bcrypt strings should start with $2b$
        self.assertTrue(u_test.password.startswith("$2b$"))

    def test_invalid_username_signup(self):
        invalid = User.signup(None, "password", "testnull@test.com", "fnamenull", "lnamenull")
        uid = 123456789
        invalid.id = uid
        with self.assertRaises(exc.IntegrityError) as context:
            db.session.commit()

    def test_invalid_email_signup(self):
        invalid = User.signup("testtest", "password", None, "fname", "lname")
        uid = 123789
        invalid.id = uid
        with self.assertRaises(exc.IntegrityError) as context:
            db.session.commit()
    
    def test_invalid_password_signup(self):
        with self.assertRaises(ValueError) as context:
            User.signup("testtest", "","email@email.com", "fname", "lname")
        
        with self.assertRaises(ValueError) as context:
            User.signup("testtest", None,"email@email.com", "fname", "lname")

    
###################################################################
     # Authentication Tests
 
    def test_valid_authentication(self):
        u = User.authenticate(self.u.username, "password")
        self.assertIsNotNone(u)
        self.assertEqual(u.id, self.uid)
    
    def test_invalid_username(self):
        self.assertFalse(User.authenticate("badusername", "password"))

    def test_wrong_password(self):
        self.assertFalse(User.authenticate(self.u.username, "badpassword"))



        




        

