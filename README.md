Overview

This Python script allows you to fetch and analyze recipes from Allrecipes.com. It lets you search for a specific recipe category, fetch the top-rated recipes based on a custom formula, and view the ingredients of a selected recipe.
Features

    Category Validation: Ensures the category exists on Allrecipes before proceeding.
    Fetch Top Recipes: Retrieves and ranks recipes based on the number of ratings and average star rating using a weighted formula.
    Concurrent Fetching: Utilizes asynchronous requests to fetch star ratings efficiently.
    Ingredient Listing: Displays the ingredient list for a selected recipe.

Requirements

    Python 3.6+
    Required Python libraries:
        requests
        beautifulsoup4
        aiohttp
        asyncio

Installation

    Clone the Repository:

    sh

git clone https://github.com/yourusername/recipe-scraper.git
cd recipe-scraper

Create a Virtual Environment:

sh

python3 -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`

Install Dependencies:

sh

    pip install requests beautifulsoup4 aiohttp

Usage

    Run the Script:

    sh

python script.py

Input the Category:

    When prompted, enter the category you want to search for (e.g., "Waffles").

View Top 3 Recipes:

    The script will display the top 3 recipes based on the custom weighted rating formula.

Select a Recipe:

    Choose a recipe by entering the number corresponding to the recipe (1, 2, or 3).

View Ingredients:

    The script will display the ingredient list for the selected recipe.
