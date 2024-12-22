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


def get_bad_image(url):
    # if keyword == '':
    #     keyword = 'world-news'
    # keyword1 = keyword.replace('-', ' ')
    # keyword1 = urllib.parse.quote_plus(keyword1)
    # yesterday = (date.today() - timedelta(days=1)).strftime('%Y-%m-%d')
    # base_url = 'https://newsapi.org/v2/everything'
    # params = {
    #     'q': keyword1,
    #     'from': yesterday,
    #     'sortBy': 'publishedAt',
    #     'language': 'en',
    #     'apiKey': '41e2e097fbb4457c9b714ee6acd4185b'
    # }

    # try:
    # response = requests.get(url, params=params)
    # response = requests.get(url)
    # response.raise_for_status()  # Raise an exception for HTTP errors
    # content_type = response.headers.get('Content-Type')
    # print("Content-Type:", content_type)

    global response
    try:
        response = requests.get(url)
        # response.raise_for_status()  # Raise HTTPError for bad responses (4xx, 5xx)
        status_code = response.status_code
        print("HTTP error occurred:", status_code)

    # content_type = response.headers.get('Content-Type')
    # print("Content-Type:", content_type)
    # except requests.exceptions.HTTPError as err:
    #     print("HTTP error occurred:", err)
    except Exception as err:
        print("An error occurred:", err)
        # newsapi_data = response.json()

        # output_path = os.path.join('../test/load_news_api', f'{keyword}.json')
        with open('kk.htm', 'w') as f:
            f.write(response.text)
        #
        # return newsapi_data
        # except requests.exceptions.RequestException as e:
        #     print(f"Error fetching data from the NewsAPI: {e}")
        # return None


get_bad_image('https://chatgpt.com/c/67420edc-e3ac-800b-b6e2-98c4a26f8fcb')
