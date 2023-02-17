# FoodReview: Food Nutritions
Food Review allows users easily to access the food information about nutrition that help users to understand about food ingredient and make a meal plan for them to use in eating habit. It makes everything easy to know which nutrients that they need for daily. Currently, this app is for portfolio purposes only. The API used is on a free plan and limited to only 10 API calls per hour, and it does not have any specific about the list. It only give few example of nutrition's.
# User Flow
# Sign Up:
Sign up with Username, Password, Email, Name. Your password is hashed using bcrypt.
# Search Food:
In the homepage, the app have a text to search for the ingredient that need to know about and a image so users can get to know about the food users can make with that ingredient
The homepage also display the Ingredients that the users liked in recently. It can easy to see the Ingredients without make any research.
# Favorite Ingredients:
Users can save the Ingredients to their homepage with a Like button display next to the Ingredients List. 
# External API:
This app uses https://www.edamam.com/. On a searching box the user can type in the ingredient. The API will return a list of ingredients with Name, Image and Nutritions per 100g. 
# Technical Stack:
PostgreSQL, Flask, Python, JavaScript, Boostrap 
