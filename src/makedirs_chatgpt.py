#!/home/al/.venv/bin/python3

import os
from pathlib import Path
from bs4 import BeautifulSoup

# Directory structure
dirs = [
    '',
    'sport',
    'culture',
    'lifestyle',
    'finance',
    'entertainment',
    'technology',
    'business',
    'politics',
    'science',
    'health'
]


# Create necessary directories
def create_directories():
    Path('../html/paged').mkdir(parents=True, exist_ok=True)
    Path('../test/newsapi').mkdir(parents=True, exist_ok=True)

    for directory in dirs:
        Path(f'../html/{directory}').mkdir(parents=True, exist_ok=True)


# Generate breadcrumb navigation and save HTML
def generate_breadcrumbs(soup, dir_path):
    breadcrumbs = soup.find('div', class_='breadcrumbs')

    # Add root link
    root_tag = soup.new_tag("a", href='/')
    root_tag.string = 'da'
    breadcrumbs.append(root_tag)

    # Add breadcrumb links for each directory level
    link = '/'
    for dir_name in dir_path.split('/'):
        link = os.path.join(link, dir_name) + '/'
        tag = soup.new_tag("a", href=link)
        tag.string = dir_name.replace('-', ' ')
        breadcrumbs.append(tag)


# Modify button with keyword-specific attribute
def modify_button(soup, keyword):
    button_more = soup.find('a', class_='button-more')
    button_more['loadmoretype'] = keyword


# Save the modified HTML and JSON files
def save_files(directory, soup, keyword):
    # Save modified HTML
    with open(f'../html/{directory}/index.html', 'w') as f:
        f.write(str(soup))

    # Save empty JSON placeholder
    with open(f'../html/paged/{keyword}-1.json', 'w') as f:
        f.write('[]')


# Create index.php and paged json for it
def add_index():
    with open('me-index.html', 'r') as f:
        template_html = f.read()
    soup = BeautifulSoup(template_html, features='html.parser')
    generate_breadcrumbs(soup, '')

    modify_button(soup, 'html')

    with open(f'../html/index.html', 'w') as f:
        f.write(str(soup))

    with open(f'../html/paged/html-1.json', 'w') as f:
        f.write('[]')


# Main function to process directories
def process_directories():
    # Read the template HTML file once
    with open('me-index.html', 'r') as f:
        template_html = f.read()

    for directory in dirs:
        # Parse template HTML with BeautifulSoup
        soup = BeautifulSoup(template_html, features='html.parser')

        # Get the last part of the directory as the keyword
        keyword = os.path.basename(directory)

        # Generate breadcrumbs based on the directory path
        generate_breadcrumbs(soup, directory)

        # Modify the button-more attribute with the keyword
        modify_button(soup, keyword)

        # Save the updated HTML and JSON files
        save_files(directory, soup, keyword)


if __name__ == "__main__":
    create_directories()
    process_directories()
    add_index()
