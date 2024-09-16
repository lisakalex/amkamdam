#!/home/al/.venv/bin/python3
import json
import os
import requests
import time
from bs4 import BeautifulSoup
from collections import deque
from datetime import datetime
from dateutil import parser
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


def replace_text(read_file, path_file):
    """
    Replace text in HTML file based on news API data.

    :param read_file: Content of the HTML file.
    :param path_file: Path to the HTML file.
    """
    path_file_list = path_file.split('/')
    keyword = path_file_list[-2]
    newsapi_path = f'newsapi/{keyword}.json'

    # Load news API data
    try:
        with open(newsapi_path, "r") as f:
            newsapi = json.load(f)
    except FileNotFoundError:
        logging.error(f'News API file not found: {newsapi_path}')
        return
    except json.JSONDecodeError as e:
        logging.error(f'Error decoding JSON from {newsapi_path}: {e}')
        return

    newsapi_articles = [
        r for r in newsapi['articles']
        if 'https://removed.com' not in r['url'] and r['urlToImage'] is not None
    ]

    # Update HTML file with news data
    soup = BeautifulSoup(read_file, features='html.parser')
    sections = [
        {'selector': 'article', 'class': 'mb-15 mb-sm-30 article-item', 'count': 4},
        {'selector': 'div', 'class': 'col-12 col-md-6 col-lg-12 mb-20', 'count': 5},
        {'selector': 'div', 'class': 'col-12 col-md-6 col-lg-4 col-xl-3 mb-30', 'count': 16}
    ]

    try:
        for section in sections:
            elements = soup.find_all(section['selector'], class_=section['class'])
            for i in range(min(section['count'], len(newsapi_articles))):
                article = elements[i]
                update_article(article, newsapi_articles[i])
            del newsapi_articles[:section['count']]
    except Exception as e:
        logging.error(f'Error processing HTML file: {e}')

    # Save updated HTML file
    with open(path_file, "w") as file1:
        file1.write(str(soup))

    # Update paged articles
    update_paged_articles(keyword, newsapi_articles)


def update_article(article, news_article):
    """
    Update a single article element with news data.

    :param article: BeautifulSoup article element.
    :param news_article: News article data.
    """
    link = article.find('a', class_='article__image')
    link['href'] = news_article['url']

    img = article.find('img')
    img['src'] = news_article['urlToImage']
    img['srcset'] = ''
    img['alt'] = news_article['title']

    badge = article.find('a', class_='article__badge')
    badge.string = news_article['source']['name']

    badge_date = article.find('div', class_='article__badge-date')
    badge_date.string = parser.isoparse(news_article['publishedAt']).strftime('%d %b %Y')

    link1 = article.find('a', class_='article__title')
    link1['href'] = news_article['url']
    link1.string = news_article['title']


def update_paged_articles(keyword, newsapi_articles):
    """
    Update JSON file with paged articles.

    :param keyword: Keyword to identify the articles.
    :param newsapi_articles: List of news articles.
    """
    paged_path = f'html/paged/{keyword}-1.json'
    paged = deque()
    try:
        with open(paged_path, "r") as f:
            paged = deque(json.load(f))
    except FileNotFoundError:
        logging.warning(f'Paged file not found: {paged_path}')
    except json.JSONDecodeError as e:
        logging.error(f'Error decoding JSON from {paged_path}: {e}')

    try:
        with open('article.html', 'r') as file1:
            soup = BeautifulSoup(file1.read(), features="html.parser")

        for i in newsapi_articles:
            update_article(soup, i)
            paged.appendleft(str(soup))

        with open(paged_path, 'w') as f:
            json.dump(list(paged), f)
    except Exception as e:
        logging.error(f'Error updating paged articles: {e}')


def main():
    start_time = time.time()
    count_replace = 0

    for currentpath, _, files in os.walk('html/'):
        for file in files:
            if not file.endswith(('.jpg', '.jpeg', '.png', '.svg', '.gif', '.css', '.js', '.ico', '.woff2', '.woff')):
                if 'assets' not in currentpath and 'paged' not in currentpath:
                    path_file = os.path.join(currentpath, file)
                    try:
                        with open(path_file) as file1:
                            read_file = file1.read()
                        replace_text(read_file, path_file)
                        count_replace += 1
                        logging.info(f'Processed {path_file}')
                    except Exception as e:
                        logging.error(f'Error processing file {path_file}: {e}')

    finish_time = round((time.time() - start_time) / 60, 2)
    logging.info(f'Copied {count_replace} files, time taken {finish_time} min')

    with open('count_replace.txt', "a") as file:
        file.write(f'{datetime.today().strftime("%Y-%m-%d %H:%M:%S")} files {count_replace}, time {finish_time} min\n')


if __name__ == '__main__':
    main()
