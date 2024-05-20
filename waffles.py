import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed

# Function to get the overall star rating from a recipe page
def get_star_rating(link):
    response = requests.get(link)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, 'html.parser')
    rating_element = soup.find('div', id='mntl-recipe-review-bar__rating_1-0')
    if rating_element:
        try:
            return link, float(rating_element.get_text(strip=True))
        except ValueError:
            return link, 0.0
    return link, 0.0

# Function to extract recipe details from a card
def extract_recipe_details(card):
    title_element = card.find('span', class_='card__title-text')
    title = title_element.get_text(strip=True) if title_element else "No title"

    rating_count_element = card.find('div', class_='mntl-recipe-card-meta__rating-count-number')
    if rating_count_element:
        rating_count = rating_count_element.get_text(strip=True).replace('Ratings', '').strip()
        try:
            rating_count = int(rating_count)
        except ValueError:
            rating_count = 0
    else:
        rating_count = 0

    return title, rating_count, card['href']

# Function to check if a category exists
def category_exists(category, soup):
    categories = soup.find_all('a', class_='mntl-link-list__link')
    for cat in categories:
        if category.lower() in cat.get_text(strip=True).lower():
            return cat['href']
    return None

# Function to get the ingredient list from a recipe page
def get_ingredient_list(link):
    response = requests.get(link)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, 'html.parser')
    ingredients = []
    ingredient_elements = soup.find_all('li', class_='mntl-structured-ingredients__list-item')
    for item in ingredient_elements:
        quantity = item.find('span', {'data-ingredient-quantity': 'true'}).get_text(strip=True)
        unit = item.find('span', {'data-ingredient-unit': 'true'}).get_text(strip=True)
        name = item.find('span', {'data-ingredient-name': 'true'}).get_text(strip=True)
        ingredients.append(f"{quantity} {unit} {name}")
    return ingredients

# Main function
def main(category):
    # URL of the Allrecipes recipes A-Z page
    url = 'https://www.allrecipes.com/recipes-a-z-6735880'

    # Send a GET request to the URL
    response = requests.get(url)
    response.raise_for_status()  # Check that the request was successful

    # Parse the HTML content using Beautiful Soup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Check if the category exists
    category_url = category_exists(category, soup)
    if not category_url:
        print(f"Error: Category '{category}' not found.")
        return

    # Fetch the category page
    response = requests.get(category_url)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all recipe cards
    recipe_cards = soup.find_all('a', class_='mntl-card-list-items')

    recipes = []

    # Extract details from all recipe cards
    recipe_details = [extract_recipe_details(card) for card in recipe_cards]

    # Use ThreadPoolExecutor to fetch star ratings concurrently
    with ThreadPoolExecutor(max_workers=10) as executor:
        future_to_recipe = {executor.submit(get_star_rating, recipe[2]): recipe for recipe in recipe_details}

        for future in as_completed(future_to_recipe):
            recipe = future_to_recipe[future]
            link, star_rating = future.result()
            recipes.append((recipe[0], recipe[1], star_rating, link))

    # Calculate the average item's rating (C)
    if recipes:
        C = sum(r[2] for r in recipes) / len(recipes)
    else:
        C = 0.0

    # Tuneable parameter (adjust as needed)
    m = 10

    # Calculate the score for each recipe using the formula
    def calculate_weighted_rating(R, v, C, m):
        return (R * v + C * m) / (v + m)

    # Calculate the scores and sort the recipes
    sorted_recipes = sorted(recipes, key=lambda x: calculate_weighted_rating(x[2], x[1], C, m), reverse=True)

    # Print the top 3 sorted recipes
    print("Top 3 Recipes:")
    for i, (title, rating_count, star_rating, link) in enumerate(sorted_recipes[:3], start=1):
        print(f"{i}. Recipe: {title} - Ratings: {rating_count} - Star Rating: {star_rating} - Link: {link}")

    # Prompt the user to select a recipe
    choice = int(input("Select a recipe (1, 2, or 3): "))
    if 1 <= choice <= 3:
        selected_recipe = sorted_recipes[choice - 1]
        print(f"Fetching ingredients for: {selected_recipe[0]}")

        # Get the ingredient list for the selected recipe
        ingredients = get_ingredient_list(selected_recipe[3])
        print("Ingredients:")
        for ingredient in ingredients:
            print(f"- {ingredient}")
    else:
        print("Invalid choice.")

if __name__ == "__main__":
    input_category = input("Enter the category: ")
    main(input_category)
