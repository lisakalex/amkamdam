#!/home/al/.venv/bin/python3
import glob2
from bs4 import BeautifulSoup
from pathlib import Path
import os

# List of directories
dirs = [
    'sport/boxing-sport', 'sport/cricket-sport', 'sport/football-sport', 'sport/formula-1-racing', 'sport/tennis-sport',
    'culture/popular-films', 'culture/music', 'culture/books', 'culture/art', 'culture/photography',
    'lifestyle/shopping', 'lifestyle/beauty', 'lifestyle/tech-news', 'lifestyle/money', 'lifestyle/fashion',
    'finance/financial-markets', 'finance/property-market', 'finance/stocks-and-shares', 'finance/brexit', 'finance/crypto'
]

# Base directories
html_base = '../html'
paged_base = '../html/paged'
newsapi_base = '../test/newsapi'

# Ensure the base directories exist
Path(html_base).mkdir(parents=True, exist_ok=True)
Path(paged_base).mkdir(parents=True, exist_ok=True)
Path(newsapi_base).mkdir(parents=True, exist_ok=True)

# Function to update HTML with new breadcrumb and button
def update_html_for_directory(directory, soup, dir_name):
    breadcrumbs = soup.find('div', class_='breadcrumbs')
    links = breadcrumbs.find_all('a')

    # Update breadcrumbs
    links[1]['href'] = f'/{dir_name[0]}/'
    links[1].string = dir_name[0]
    links[2]['href'] = f'/{directory}/'
    links[2].string = dir_name[1]

    # Update button-more element
    buttonmore = soup.find('a', class_='button-more')
    buttonmore['loadmoretype'] = dir_name[1]

    return soup

# Function to write JSON files
def write_json_files(dir_name):
    with open(f'{paged_base}/{dir_name[0]}-1.json', 'w') as f:
        f.write('[]')
    with open(f'{paged_base}/{dir_name[1]}-1.json', 'w') as f:
        f.write('[]')

# Loop over each directory
for directory in dirs:
    # Split directory into components
    dir_name = directory.split('/')

    # Ensure directory exists
    Path(os.path.join(html_base, directory)).mkdir(parents=True, exist_ok=True)

    # Load the base HTML file and parse it
    with open('me-index.html', 'r') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')

    # Update HTML with the directory-specific information
    soup = update_html_for_directory(directory, soup, dir_name)

    # Write the updated HTML for the specific directory
    with open(f'{html_base}/{directory}/index.html', 'w') as f:
        f.write(str(soup))

    # Update the button-more type and breadcrumbs for the parent category and save
    soup.find('a', class_='button-more')['loadmoretype'] = dir_name[0]
    soup.find_all('a')[2].decompose()

    with open(f'{html_base}/{dir_name[0]}/index.html', 'w') as f:
        f.write(str(soup))

    # Write the empty JSON files for pagination
    write_json_files(dir_name)
