#!/home/al/.venv/bin/python3

import os
from pathlib import Path
from bs4 import BeautifulSoup

# Directory structure
DIRS = [
    'sport', 'sport/boxing-sport', 'sport/boxing-sport/huy', 'sport/cricket-sport',
    'sport/football-sport', 'sport/formula-1-racing', 'sport/tennis-sport',
    'culture', 'culture/popular-films', 'culture/music', 'culture/books',
    'culture/art', 'culture/photography', 'lifestyle', 'lifestyle/shopping',
    'lifestyle/beauty', 'lifestyle/tech-news', 'lifestyle/money', 'lifestyle/fashion',
    'finance', 'finance/financial-markets', 'finance/property-market',
    'finance/stocks-and-shares', 'finance/brexit', 'finance/crypto'
]


# Create directory if it doesn't exist
def create_directory(path):
    Path(path).mkdir(parents=True, exist_ok=True)


# Initialize required directories
def initialize_directories():
    create_directory('../html/paged')
    create_directory('../test/newsapi')
    for directory in DIRS:
        create_directory(f'../html/{directory}')


# Generate breadcrumb navigation
def generate_breadcrumbs(soup, dir_path):
    breadcrumbs = soup.find('div', class_='breadcrumbs')
    breadcrumbs.clear()  # Clear existing breadcrumbs if necessary

    # Add root link
    breadcrumbs.append(create_breadcrumb_link(soup, 'da', '/'))

    # Add breadcrumb links for each directory level
    link = '/'
    for part in dir_path.split('/'):
        link = os.path.join(link, part) + '/'
        breadcrumbs.append(create_breadcrumb_link(soup, part.replace('-', ' '), link))


# Create individual breadcrumb link
def create_breadcrumb_link(soup, text, href):
    tag = soup.new_tag("a", href=href)
    tag.string = text
    return tag


# Modify button with keyword-specific attribute
def update_loadmore_button(soup, keyword):
    button_more = soup.find('a', class_='button-more')
    if button_more:
        button_more['loadmoretype'] = keyword


# Save modified HTML and empty JSON placeholder
def save_files(directory, soup, keyword):
    html_path = f'../html/{directory}/index.html'
    json_path = f'../html/paged/{keyword}-1.json'

    # Save modified HTML
    with open(html_path, 'w') as html_file:
        html_file.write(str(soup))

    # Save empty JSON placeholder
    with open(json_path, 'w') as json_file:
        json_file.write('[]')


# Main processing function
def process_directories():
    with open('me-index.html', 'r') as template_file:
        template_html = template_file.read()

    for directory in DIRS:
        soup = BeautifulSoup(template_html, 'html.parser')
        keyword = os.path.basename(directory)

        # Generate breadcrumbs and update button
        generate_breadcrumbs(soup, directory)
        update_loadmore_button(soup, keyword)

        # Save updated HTML and JSON
        save_files(directory, soup, keyword)


if __name__ == "__main__":
    initialize_directories()
    process_directories()
