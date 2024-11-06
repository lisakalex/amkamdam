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


def load_news_api(keyword):
    if keyword == '':
        keyword = 'world-news'
    keyword1 = keyword.replace('-', ' ')
    keyword1 = urllib.parse.quote_plus(keyword1)
    yesterday = (date.today() - timedelta(days=1)).strftime('%Y-%m-%d')
    base_url = 'https://newsapi.org/v2/everything'
    params = {
        'q': keyword1,
        'from': yesterday,
        'sortBy': 'publishedAt',
        'language': 'en',
        'apiKey': '41e2e097fbb4457c9b714ee6acd4185b'
    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Raise an exception for HTTP errors
        newsapi_data = response.json()

        output_path = os.path.join('../test/load_news_api', f'{keyword}.json')
        with open(output_path, 'w') as f:
            json.dump(newsapi_data, f, indent=4)

        return newsapi_data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from the NewsAPI: {e}")
    return None


load_news_api('news')
