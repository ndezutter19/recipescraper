Overview

This Python script allows you to fetch and analyze recipes from Allrecipes.com. It enables you to search for a specific recipe category, fetch the top-rated recipes based on a custom formula, and view the ingredients and steps of a selected recipe.

Features:

* Category Validation: Ensures the category exists on Allrecipes before proceeding.
* Fetch Top Recipes: Retrieves and ranks recipes based on the number of ratings and average star rating using a weighted formula.
* Concurrent Fetching: Utilizes asynchronous requests to fetch star ratings efficiently.
* Ingredient and Step Listing: Displays the ingredient list and steps for a selected recipe.
* List Categories: Lists all available categories when prompted.

Requirements

    Python 3.6+
    Required Python libraries:
        requests
        beautifulsoup4
        aiohttp
        asyncio

Installation

Clone the Repository:

    git clone https://github.com/yourusername/recipe-scraper.git

Install Dependencies:

    pip install requests beautifulsoup4 aiohttp

Usage

Run the Script:

    python waffles.py

Input the Category:

    When prompted, enter the category you want to search for (e.g., "Waffles").
    Type "list categories" to see all available categories.

View Top 10 Recipes:

    The script will display the top 10 recipes based on the custom weighted rating formula.

Select a Recipe:

    Choose a recipe by entering the number corresponding to the recipe (1-10).

View Ingredients and Steps:

    The script will display the ingredient list and steps for the selected recipe.
