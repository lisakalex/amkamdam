#!/home/al/.venv/bin/python3
import time
from datetime import datetime, date, timedelta
from collections import deque
from bs4 import BeautifulSoup
from dateutil import parser
import os
import urllib.parse
import requests
import json
import shutil
from langdetect import detect, DetectorFactory
import re
from textblob import TextBlob


# https://beautiful-soup-4.readthedocs.io/en/latest/


class NewsUpdater:
    def __init__(self):
        self.start_time = time.time()
        self.today_time = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        self.count_replace = 1

    def load_news_api(self, keyword):
        # keyword = keyword.replace('-', ' ')
        # with open(f'../test/newsapi/{keyword}.json', "r") as f:
        with open(f'../test/kak1.json', "r") as f:
            return json.load(f)

    # def load_news_api(self, keyword):
    #     keyword1 = keyword.replace('-', ' ')
    #     keyword1 = urllib.parse.quote_plus(keyword1)
    #     yesterday = (date.today() - timedelta(days=1)).strftime('%Y-%m-%d')
    #     base_url = 'https://newsapi.org/v2/everything'
    #     params = {
    #         'q': keyword1,
    #         'from': yesterday,
    #         'sortBy': 'publishedAt',
    #         'language': 'en',
    #         'apiKey': '41e2e097fbb4457c9b714ee6acd4185b'
    #     }
    #
    #     try:
    #         response = requests.get(base_url, params=params)
    #         response.raise_for_status()  # Raise an exception for HTTP errors
    #         newsapi_data = response.json()
    #
    #         output_path = os.path.join('../test/newsapi', f'{keyword}.json')
    #         with open(output_path, 'w') as f:
    #             json.dump(newsapi_data, f, indent=4)
    #
    #         return newsapi_data
    #     except requests.exceptions.RequestException as e:
    #         print(f"Error fetching data from the NewsAPI: {e}")
    #     return None

    def filter_articles(self, articles):
        kak = [article for article in articles if self._is_valid_article(article)]
        return kak

    def _is_valid_article(self, article):
        required_fields = ['url', 'source', 'title', 'description', 'urlToImage', 'publishedAt', 'content']

        # Check for removed URL
        if 'https://removed.com' in article.get('url', ''):
            return False

        # Check source name
        if not article.get('source', {}).get('name'):
            return False

        # Validate image URL
        image_url = article.get('urlToImage', '')
        if not self._is_valid_image_url(image_url):
            return False

        # Check all required fields are present and non-empty
        return all(article.get(field) not in (None, '') for field in required_fields)

    def _is_valid_image_url(self, url):
        if not url:
            return False

        try:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
            # response = requests.get(url, headers=headers)
            # headers['Referer'] = 'https://gooole.com'
            session = requests.Session()
            response = session.get(url, headers=headers)
            # response = requests.get(url)
            huy = response.status_code
            response.raise_for_status()
            return True
        except Exception as err:
            self._log_error(url, err)
            return False

    def _log_error(self, url, error):
        with open('log_log.txt', 'a') as f:
            f.write(f"{url} error: {str(error)}\n")

    def remove_duplicate_content(self, data):
        seen_content = set()
        seen_title = set()
        seen_description = set()
        seen_urlToImage = set()
        unique_articles = []

        for article in data:
            content = article.get('content', '')
            title = article.get('title', '')
            description = article.get('description', '')
            urlToImage = article.get('urlToImage', '')

            # Check if any of the fields have been seen before
            if (content not in seen_content and
                    title not in seen_title and
                    description not in seen_description and
                    urlToImage not in seen_urlToImage):
                # If all fields are new, add the article and update the sets
                seen_content.add(content)
                seen_title.add(title)
                seen_description.add(description)
                seen_urlToImage.add(urlToImage)
                unique_articles.append(article)

        return unique_articles

    def update_article(self, article, news_item):
        try:
            link = article.find('a', class_='article__image')
            link['href'] = news_item['url']

            img = article.find('img')
            img['src'] = news_item['urlToImage']
            img['srcset'] = ''
            img['alt'] = news_item['title']

            badge = article.find('a', class_='article__badge')
            badge.string = news_item['source']['name']

            badge_date = article.find('div', class_='article__badge-date')
            badge_date.string = parser.isoparse(news_item['publishedAt']).strftime('%d %b %Y')

            link1 = article.find('a', class_='article__title')
            link1['href'] = news_item['url']
            link1.string = news_item['title']
        except Exception as e:
            print(f"Error processing 1: {e}")
        return article

    def update_main_articles(self, soup, news_articles):
        section = soup.find_all('article', class_='mb-15 mb-sm-30 article-item')
        try:
            for i in range(min(4, len(section))):
                article = self.update_article(section[i], news_articles[i])
                article.find_all('div')[6].string = news_articles[i]['content']
        except Exception as e:
            print(f"update_main_articles: {e}")
        return news_articles[4:]

    def update_secondary_articles(self, soup, news_articles):
        section = soup.find_all('div', class_='col-12 col-md-6 col-lg-12 mb-20')
        try:
            for i in range(min(5, len(section))):
                self.update_article(section[i], news_articles[i])
        except Exception as e:
            print(f"update_secondary_articles: {e}")
        return news_articles[5:]

    def update_tertiary_articles(self, soup, news_articles):
        section = soup.find_all('div', class_='col-12 col-md-6 col-lg-4 col-xl-3 mb-30')
        try:
            for i in range(min(16, len(section))):
                self.update_article(section[i], news_articles[i])
        except Exception as e:
            print(f"update_tertiary_articles: {e}")
        return news_articles[16:]

    def update_paged_articles(self, soup, news_articles, keyword):
        paged = self.load_paged_articles(keyword)

        for article in news_articles:
            updated_soup = self.update_article(soup, article)
            paged.appendleft(str(updated_soup))

        self.save_paged_articles(keyword, paged)

    def load_paged_articles(self, keyword):
        try:
            with open(f'../html/paged/{keyword}-1.json', "r") as f:
                return deque(json.load(f))
        except Exception as e:
            print(f"Error loading paged articles: {e}")
            return deque()

    def save_paged_articles(self, keyword, paged):
        try:
            with open(f'../html/paged/{keyword}-1.json', 'w') as f:
                json.dump(list(paged), f)
        except Exception as e:
            print(f"Error saving paged articles: {e}")

    def replace_text(self, read_file, path_file):
        keyword = os.path.basename(os.path.dirname(path_file))
        newsapi = self.load_news_api(keyword)
        news_articles = self.filter_articles(newsapi['articles'])
        news_articles = self.remove_duplicate_content(news_articles)
        soup = BeautifulSoup(read_file, features='html.parser')

        news_articles = self.update_main_articles(soup, news_articles)
        news_articles = self.update_secondary_articles(soup, news_articles)
        news_articles = self.update_tertiary_articles(soup, news_articles)

        with open(path_file, "w") as file:
            file.write(str(soup))

        with open('article.html', 'r') as file:
            article_soup = BeautifulSoup(file.read(), features="html.parser")

        self.update_paged_articles(article_soup, news_articles, keyword)

    def process_files(self):
        for currentpath, _, files in os.walk('../html'):
            for file in files:
                if self.should_process_file(file, currentpath):
                    path_file = os.path.join(currentpath, file)
                    try:
                        with open(path_file) as file:
                            read_file = file.read()
                        self.replace_text(read_file, path_file)
                        print(f"{self.count_replace} {path_file}")
                        self.count_replace += 1
                    except Exception as e:
                        print(f"Error processing 2 {path_file}: {e}")

    def should_process_file(self, file, currentpath):
        excluded_extensions = ('.jpg', '.jpeg', '.png', '.svg', '.gif', '.css', '.js', '.ico', '.woff2', '.woff')
        excluded_dirs = ('assets', 'paged')
        return not file.endswith(excluded_extensions) and not any(dirs in currentpath for dirs in excluded_dirs)

    def run(self):
        self.process_files()
        finish_time = round((time.time() - self.start_time) / 60, 2)
        print(f'Processed {self.count_replace - 1} files, time taken {finish_time} min')

        with open('../test/count_replace.txt', "a") as file:
            file.write(f"{self.today_time} files {self.count_replace - 1}, time {finish_time} min\n")


if __name__ == '__main__':
    updater = NewsUpdater()
    updater.run()
    shutil.copyfile('../html/news/index.html', '../html/index.html')
