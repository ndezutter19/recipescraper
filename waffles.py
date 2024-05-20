import requests
from bs4 import BeautifulSoup

# URL of the Allrecipes "Waffles" category page
url = 'https://www.allrecipes.com/recipes/1316/breakfast-and-brunch/waffles/'

# Send a GET request to the URL
response = requests.get(url)
response.raise_for_status()  # Check that the request was successful

# Parse the HTML content using Beautiful Soup
soup = BeautifulSoup(response.content, 'html.parser')

# Find all elements that contain the recipe titles and their corresponding rating count
recipe_elements = soup.find_all('span', class_='card__title-text')

# Iterate through each recipe element to extract title and corresponding rating count
for element in recipe_elements:
    title = element.get_text(strip=True)
    
    # Find the closest parent with the rating count number
    rating_parent = element.find_parent('span', class_='card__title')
    if rating_parent:
        rating_count_element = rating_parent.find_next('div', class_='mntl-recipe-card-meta__rating-count-number')
        if rating_count_element:
            rating_count = rating_count_element.get_text(strip=True)
            # Remove trailing "Ratings" text if present
            rating_count = rating_count.replace('Ratings', '').strip()
        else:
            rating_count = "No ratings"
    else:
        rating_count = "No ratings"
    
    print(f"Recipe: {title} - Ratings: {rating_count}")
