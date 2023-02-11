"""Food api tests."""

# run these tests like:
#
#    python -m unittest test_food_api.py

from unittest import TestCase
from flask import Flask
from app import food_data_list, get_food_data

class FoodTestCase(TestCase):
    def test_add_to_food_data_list(self):
        food_data_list.clear()
        ingredient = "chicken"
        food_data = get_food_data(ingredient)
        food_data_list.append(food_data)
        self.assertEqual(len(food_data_list), 1)

    def test_clear_food_data_list(self):
        food_data_list.clear()
        self.assertEqual(len(food_data_list), 0)
    


