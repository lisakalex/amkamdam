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
# logging.basicConfig(filename='script.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
#
# # Constants
# API_KEY = os.getenv('NEWS_API_KEY', 'your-api-key-here')
# NEWS_API_URL = 'https://newsapi.org/v2/everything'
# EXCLUDED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.svg', '.gif', '.css', '.js', '.ico', '.woff2', '.woff'}
# EXCLUDED_DIRS = {'assets', 'paged'}


# def fetch_news(keyword):
#     keyword_encoded = urllib.parse.quote_plus(keyword.replace('-', ' '))
#     yesterday = (date.today() - timedelta(days=1)).strftime('%Y-%m-%d')
#     url = f'{NEWS_API_URL}?q={keyword_encoded}&from={yesterday}&sortBy=publishedAt&language=en&apiKey={API_KEY}'
url = 'https://chatgpt.com/c/67420edc-e3ac-800b-b6e2-98c4a26f8fcb'
try:
    response = requests.get(url)
    response.raise_for_status()
    # return response.json()
except requests.RequestException as e:
    logging.error(f'Error fetching news: {e}')
    # return None
