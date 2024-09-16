import os
import json
from datetime import datetime
from collections import deque
from bs4 import BeautifulSoup
from dateutil import parser

class NewsUpdater:
    def __init__(self):
        self.today = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        self.processed_files = 0
        self.processing_time = 0

    def load_json_file(self, filepath):
        try:
            with open(filepath, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"File not found: {filepath}")
            return []
        except json.JSONDecodeError:
            print(f"Invalid JSON in file: {filepath}")
            return []

    def save_json_file(self, filepath, data):
        try:
            with open(filepath, 'w') as f:
                json.dump(data, f)
        except Exception as e:
            print(f"Error saving file {filepath}: {e}")

    def load_news_api(self, keyword):
        filepath = f'../newsapi/{keyword}.json'
        return self.load_json_file(filepath)

    def load_paged_articles(self, keyword):
        filepath = f'../html/paged/{keyword}-1.json'
        data = self.load_json_file(filepath)
        return deque(data) if data else deque()

    def save_paged_articles(self, keyword, paged):
        filepath = f'../html/paged/{keyword}-1.json'
        self.save_json_file(filepath, list(paged))

    def filter_articles(self, articles):
        required_fields = ['url', 'source', 'title', 'description', 'urlToImage', 'publishedAt', 'content']
        return [
            article for article in articles
            if all(article.get(field) for field in required_fields)
               and 'https://removed.com' not in article.get('url', '')
        ]

    def update_article(self, article_soup, news_item):
        updates = {
            'a.article__image': {'href': news_item['url']},
            'img': {
                'src': news_item['urlToImage'],
                'srcset': '',
                'alt': news_item['title']
            },
            'a.article__badge': {'string': news_item['source']['name']},
            'div.article__badge-date': {'string': parser.isoparse(news_item['publishedAt']).strftime('%d %b %Y')},
            'a.article__title': {
                'href': news_item['url'],
                'string': news_item['title']
            },
            'div:nth-of-type(7)': {'string': news_item['content']}
        }

        for selector, attrs in updates.items():
            element = article_soup.select_one(selector)
            if element:
                for attr, value in attrs.items():
                    if attr == 'string':
                        element.string = value
                    else:
                        element[attr] = value

        return article_soup

    def update_articles(self, soup, sections, num_articles):
        articles = self.load_news_api(os.path.basename(soup.filename).split('-')[0])
        filtered_articles = self.filter_articles(articles.get('articles', []))

        for i, section in enumerate(sections[:num_articles]):
            if i >= len(filtered_articles):
                break
            article_soup = section.copy()
            updated_article = self.update_article(article_soup, filtered_articles[i])
            soup.find_all(section.name, class_=section['class'])[i].replace_with(updated_article)

    def update_page(self, soup, keyword):
        article_sections = [
            ('article', 'mb-15 mb-sm-30 article-item', 4),
            ('div', 'col-12 col-md-6 col-lg-12 mb-20', 5),
            ('div', 'col-12 col-md-6 col-lg-4 col-xl-3 mb-30', 16)
        ]

        for tag, class_, num in article_sections:
            self.update_articles(soup, soup.find_all(tag, class_=class_), num)

        paged_articles = self.load_paged_articles(keyword)
        paged_articles.appendleft(str(soup))
        self.save_paged_articles(keyword, paged_articles)

    def process_file(self, filepath):
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                soup = BeautifulSoup(f, 'html.parser')

            keyword = os.path.basename(filepath).split('-')[0]
            self.update_page(soup, keyword)

            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(str(soup))

            self.processed_files += 1
        except Exception as e:
            print(f"Error processing file {filepath}: {e}")

    def process_directory(self, directory):
        start_time = datetime.now()
        for filename in os.listdir(directory):
            if filename.endswith('.html'):
                self.process_file(os.path.join(directory, filename))
        self.processing_time = (datetime.now() - start_time).total_seconds()

    def run(self, directory):
        self.process_directory(directory)
        print(f"Processed {self.processed_files} files in {self.processing_time:.2f} seconds")

if __name__ == '__main__':
    updater = NewsUpdater()
    updater.run('../html')
