#!/home/al/.venv/bin/python3
import os
import json
import time
from datetime import datetime
from collections import deque
from bs4 import BeautifulSoup
from dateutil import parser


class NewsUpdater:
    def __init__(self):
        self.start_time = time.time()
        self.today_time = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        self.count_replace = 1

    def load_news_api(self, keyword):
        with open(f'../test/newsapi/{keyword}.json', "r") as f:
            # with open(f'../newsapi/kak.json', "r") as f:
            return json.load(f)

    def filter_articles(self, articles):
        return [article for article in articles if self._is_valid_article(article)]

    def _is_valid_article(self, article):
        required_fields = ['url', 'source', 'title', 'description', 'urlToImage', 'publishedAt', 'content']

        if 'https://removed.com' in article.get('url', ''):
            return False

        if not article.get('source', {}).get('name'):
            return False

        return all(article.get(field) is not None for field in required_fields)

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
            print(f"Error processing : {e}")
        return article

    def update_main_articles(self, soup, news_articles):
        section = soup.find_all('article', class_='mb-15 mb-sm-30 article-item')
        for i in range(min(4, len(section))):
            article = self.update_article(section[i], news_articles[i])
            article.find_all('div')[6].string = news_articles[i]['content']
        return news_articles[4:]

    def update_secondary_articles(self, soup, news_articles):
        section = soup.find_all('div', class_='col-12 col-md-6 col-lg-12 mb-20')
        for i in range(min(5, len(section))):
            self.update_article(section[i], news_articles[i])
        return news_articles[5:]

    def update_tertiary_articles(self, soup, news_articles):
        section = soup.find_all('div', class_='col-12 col-md-6 col-lg-4 col-xl-3 mb-30')
        for i in range(min(16, len(section))):
            self.update_article(section[i], news_articles[i])
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
        path_file_list = path_file.split('/')
        keyword = path_file_list[-2]

        newsapi = self.load_news_api(keyword)
        news_articles = self.filter_articles(newsapi['articles'])

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
        for currentpath, _, files in os.walk('../html/'):
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
                        print(f"Error processing {path_file}: {e}")

    def should_process_file(self, file, currentpath):
        excluded_extensions = ('.jpg', '.jpeg', '.png', '.svg', '.gif', '.css', '.js', '.ico', '.woff2', '.woff')
        excluded_dirs = ('assets', 'paged')
        return not file.endswith(excluded_extensions) and not any(dir in currentpath for dir in excluded_dirs)

    def run(self):
        self.process_files()
        finish_time = round((time.time() - self.start_time) / 60, 2)
        print(f'Processed {self.count_replace - 1} files, time taken {finish_time} min')

        with open('../test/count_replace.txt', "a") as file:
            file.write(f"{self.today_time} files {self.count_replace - 1}, time {finish_time} min\n")


if __name__ == '__main__':
    updater = NewsUpdater()
    updater.run()
