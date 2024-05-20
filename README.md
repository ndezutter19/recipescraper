Overview

This Python script allows you to fetch and analyze recipes from Allrecipes.com. It enables you to search for a specific recipe category, fetch the top-rated recipes based on a custom formula, and view the ingredients and steps of a selected recipe.
Features

    Category Validation: Ensures the category exists on Allrecipes before proceeding.
    Fetch Top Recipes: Retrieves and ranks recipes based on the number of ratings and average star rating using a weighted formula.
    Concurrent Fetching: Utilizes asynchronous requests to fetch star ratings efficiently.
    Ingredient and Step Listing: Displays the ingredient list and steps for a selected recipe.
    List Categories: Lists all available categories when prompted.

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
    Type "list categories" to see all available categories.

View Top 3 Recipes:

    The script will display the top 3 recipes based on the custom weighted rating formula.

Select a Recipe:

    Choose a recipe by entering the number corresponding to the recipe (1, 2, or 3).

View Ingredients and Steps:

    The script will display the ingredient list and steps for the selected recipe.
