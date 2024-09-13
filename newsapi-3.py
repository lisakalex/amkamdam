#!/home/al/.venv/bin/python3
from bs4 import BeautifulSoup
import requests
import time
from datetime import datetime, timedelta, date
import os
import json
from collections import deque
from dateutil import parser
import urllib.parse
import logging

# Set up logging
logging.basicConfig(filename='script.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Constants
API_KEY = os.getenv('NEWS_API_KEY', 'your-api-key-here')
NEWS_API_URL = 'https://newsapi.org/v2/everything'
EXCLUDED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.svg', '.gif', '.css', '.js', '.ico', '.woff2', '.woff'}
EXCLUDED_DIRS = {'assets', 'paged'}


def fetch_news(keyword):
    keyword_encoded = urllib.parse.quote_plus(keyword.replace('-', ' '))
    yesterday = (date.today() - timedelta(days=1)).strftime('%Y-%m-%d')
    url = f'{NEWS_API_URL}?q={keyword_encoded}&from={yesterday}&sortBy=publishedAt&language=en&apiKey={API_KEY}'

    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        logging.error(f'Error fetching news: {e}')
        return None


def update_html_with_news(soup, articles):
    sections = [
        (soup.find_all('article', class_='mb-15 mb-sm-30 article-item'), 4),
        (soup.find_all('div', class_='col-12 col-md-6 col-lg-12 mb-20'), 5),
        (soup.find_all('div', class_='col-12 col-md-6 col-lg-4 col-xl-3 mb-30'), 16)
    ]

    for section, count in sections:
        for i in range(min(count, len(articles))):
            article = section[i]
            try:
                link = article.find('a', class_='article__image')
                img = article.find('img')
                badge = article.find('a', class_='article__badge')
                badge_date = article.find('div', class_='article__badge-date')
                link1 = article.find('a', class_='article__title')

                link['href'] = articles[i]['url']
                img['src'] = articles[i]['urlToImage']
                img['srcset'] = ''
                img['alt'] = articles[i]['title']
                badge.string = articles[i]['source']['name']
                badge_date.string = parser.isoparse(articles[i]['publishedAt']).strftime('%d %b %Y')
                link1['href'] = articles[i]['url']
                link1.string = articles[i]['title']

                if 'content' in articles[i]:
                    article.find_all('div')[6].string = articles[i]['content']
            except (AttributeError, IndexError) as e:
                logging.error(f'Error updating article: {e}')
                continue


def replace_text(read_file1, path_file1):
    path_file1_list = path_file1.split('/')
    keyword = path_file1_list[-2]

    newsapi_response = fetch_news(keyword)
    if not newsapi_response:
        return

    newsapi_articles = [r for r in newsapi_response.get('articles', []) if 'https://removed.com' not in r['url'] and r['urlToImage']]

    soup = BeautifulSoup(read_file1, 'html.parser')
    update_html_with_news(soup, newsapi_articles)

    with open(path_file1, "w") as file1:
        file1.write(str(soup))

    try:
        with open('article.html', 'r') as file1:
            soup = BeautifulSoup(file1.read(), 'html.parser')

        paged = deque()
        try:
            with open(f'html/paged/{keyword}-1.json', "r") as f:
                paged = deque(json.load(f))
        except (FileNotFoundError, json.JSONDecodeError) as e:
            logging.error(f'Error loading paged data: {e}')

        for i in newsapi_articles:
            link = soup.find('a', class_='article__image')
            img = soup.find('img')
            badge = soup.find('a', class_='article__badge')
            badge_date = soup.find('div', class_='article__badge-date')
            link1 = soup.find('a', class_='article__title')

            link['href'] = i['url']
            img['src'] = i['urlToImage']
            img['srcset'] = ''
            img['alt'] = i['title']
            badge.string = i['source']['name']
            badge_date.string = parser.isoparse(i['publishedAt']).strftime('%d %b %Y')
            link1['href'] = i['url']
            link1.string = i['title']

            paged.appendleft(str(soup))

        with open(f'html/paged/{keyword}-1.json', 'w') as f:
            json.dump(list(paged), f)
    except Exception as e:
        logging.error(f'Error processing paged data: {e}')


def main():
    count_replace = 0
    for currentpath, _, files in os.walk('html/'):
        for file in files:
            if not any(file.endswith(ext) for ext in EXCLUDED_EXTENSIONS) and not any(dir in currentpath for dir in EXCLUDED_DIRS):
                path_file = os.path.join(currentpath, file)
                try:
                    with open(path_file) as file1:
                        read_file = file1.read()
                    replace_text(read_file, path_file)
                    count_replace += 1
                    logging.info(f'Processed file: {path_file}')
                except Exception as e:
                    logging.error(f'Error processing file {path_file}: {e}')

    finish_time = round((time.time() - start_time) / 60, 2)
    logging.info(f'Copied {count_replace} files, time taken {finish_time} min')

    with open('count_replace.txt', "a") as file:
        file.write(f'{datetime.today().strftime("%Y-%m-%d %H:%M:%S")} files {count_replace}, time {finish_time} min\n')


if __name__ == '__main__':
    start_time = time.time()
    main()
