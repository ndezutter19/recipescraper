import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed

# URL of the Allrecipes "Waffles" category page
url = 'https://www.allrecipes.com/recipes/1316/breakfast-and-brunch/waffles/'

# Send a GET request to the URL
response = requests.get(url)
response.raise_for_status()  # Check that the request was successful

# Parse the HTML content using Beautiful Soup
soup = BeautifulSoup(response.content, 'html.parser')

# Find all recipe cards
recipe_cards = soup.find_all('a', class_='mntl-card-list-items')

recipes = []

# Function to get the overall star rating from a recipe page
def get_star_rating(card):
    link = card['href']
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

# Extract details from all recipe cards
recipe_details = [extract_recipe_details(card) for card in recipe_cards]

def main():
    # Use ThreadPoolExecutor to fetch star ratings concurrently
    with ThreadPoolExecutor(max_workers=10) as executor:
        future_to_recipe = {executor.submit(get_star_rating, card): card for card in recipe_cards}

        for future in as_completed(future_to_recipe):
            card = future_to_recipe[future]
            link, star_rating = future.result()
            for recipe in recipe_details:
                if recipe[2] == link:
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

    # Print the sorted recipes
    for title, rating_count, star_rating, link in sorted_recipes:
        print(f"Recipe: {title} - Ratings: {rating_count} - Star Rating: {star_rating}")
    

if __name__ == "__main__":
    main()