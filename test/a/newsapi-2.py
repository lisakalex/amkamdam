#!/home/al/.venv/bin/python3
from bs4 import BeautifulSoup
import requests
import time
from pathlib import Path
from datetime import datetime, timedelta, date
import os
import json
from collections import deque
from dateutil import parser
import urllib.parse
import logging

# Configure logging
logging.basicConfig(filename='script.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

API_KEY = '41e2e097fbb4457c9b714ee6acd4185b'


def replace_text(read_file, path_file):
    path_file_list = path_file.split('/')
    keyword = path_file_list[-2]
    keyword1 = keyword.replace('-', ' ')
    keyword1 = urllib.parse.quote_plus(keyword1)
    yesterday = (date.today() - timedelta(days=1)).strftime('%Y-%m-%d')
    url = (f'https://newsapi.org/v2/everything?q={keyword1}&from={yesterday}&sortBy=publishedAt&language=en&apiKey={API_KEY}')

    try:
        newsapi_json = requests.get(url).text
        newsapi = json.loads(newsapi_json)
    except Exception as e:
        logging.error(f'Error fetching news API data: {e}')
        return

    with open(f'newsapi/{keyword}.json', 'w') as f:
        f.write(newsapi_json)

    newsapi_articles = [r for r in newsapi.get('articles', []) if 'https://removed.com' not in r['url'] and r['urlToImage']]

    soup = BeautifulSoup(read_file, 'html.parser')

    sections = [
        (soup.find_all('article', class_='mb-15 mb-sm-30 article-item'), 4),
        (soup.find_all('div', class_='col-12 col-md-6 col-lg-12 mb-20'), 5),
        (soup.find_all('div', class_='col-12 col-md-6 col-lg-4 col-xl-3 mb-30'), 16)
    ]

    for section, count in sections:
        for i in range(min(count, len(newsapi_articles))):
            try:
                article = section[i]
                link = article.find('a', class_='article__image')
                link['href'] = newsapi_articles[i]['url']

                img = article.find('img')
                img['src'] = newsapi_articles[i]['urlToImage']
                img['srcset'] = ''
                img['alt'] = newsapi_articles[i]['title']

                badge = article.find('a', class_='article__badge')
                badge.string = newsapi_articles[i]['source']['name']

                badge_date = article.find('div', class_='article__badge-date')
                badge_date.string = parser.isoparse(newsapi_articles[i]['publishedAt']).strftime('%d %b %Y')

                link1 = article.find('a', class_='article__title')
                link1['href'] = newsapi_articles[i]['url']
                link1.string = newsapi_articles[i]['title']
                article.find_all('div')[6].string = newsapi_articles[i]['content']
            except Exception as e:
                logging.error(f'Error updating article: {e}')
                continue

        del newsapi_articles[:count]

    try:
        with open(path_file, "w") as file1:
            file1.write(str(soup))
    except Exception as e:
        logging.error(f'Error writing to file {path_file}: {e}')

    paged = deque()
    try:
        with open(f'html/paged/{keyword}-1.json', "r") as f:
            paged = deque(json.load(f))
    except FileNotFoundError:
        pass
    except Exception as e:
        logging.error(f'Error loading paged data: {e}')

    for i in newsapi_articles:
        try:
            link = soup.find('a', class_='article__image')
            link['href'] = i['url']

            img = soup.find('img')
            img['src'] = i['urlToImage']
            img['srcset'] = ''
            img['alt'] = i['title']

            badge = soup.find('a', class_='article__badge')
            badge.string = i['source']['name']

            badge_date = soup.find('div', class_='article__badge-date')
            badge_date.string = parser.isoparse(i['publishedAt']).strftime('%d %b %Y')

            link1 = soup.find('a', class_='article__title')
            link1['href'] = i['url']
            link1.string = i['title']

            paged.appendleft(str(soup))
        except Exception as e:
            logging.error(f'Error updating paged data: {e}')

    try:
        with open(f'html/paged/{keyword}-1.json', 'w') as f:
            json.dump(list(paged), f)
    except Exception as e:
        logging.error(f'Error saving paged data: {e}')


def main():
    count_replace = 0
    for currentpath, folders, files in os.walk('html/'):
        for file in files:
            if not any(ext in file for ext in ['.jpg', '.jpeg', '.png', '.svg', '.gif', '.css', '.js', '.ico', '.woff2', '.woff']) and 'assets' not in currentpath and 'paged' not in currentpath:
                path_file = os.path.join(currentpath, file)
                try:
                    with open(path_file) as file1:
                        read_file = file1.read()
                    replace_text(read_file, path_file)
                    count_replace += 1
                    logging.info(f'Processed {count_replace} file: {path_file}')
                except Exception as e:
                    logging.error(f'Error processing file {path_file}: {e}')

    finish_time = round((time.time() - start_time) / 60, 2)
    logging.info(f'Copied {count_replace} files, time taken {finish_time} min')

    with open('count_replace.txt', "a") as file:
        file.write(f'{datetime.today().strftime("%Y-%m-%d %H:%M:%S")} files {count_replace}, time {finish_time} min\n')


if __name__ == '__main__':
    start_time = time.time()
    main()
