#!/home/al/.venv/bin/python3
from bs4 import BeautifulSoup
import requests
import time
from pathlib import Path
from datetime import datetime, timedelta, date
import os
import json
import urllib.parse


# https://beautiful-soup-4.readthedocs.io/en/latest/


def paged(keyword):
    keyword = urllib.parse.quote_plus(keyword)
    y = date.today() - timedelta(days=1)
    yesterday = y.strftime('%Y-%m-%d')
    url = ('https://newsapi.org/v2/everything?'
           'q=' + keyword +
           '&' + yesterday +
           '&sortBy=publishedAt'
           '&language=en'
           '&apiKey=41e2e097fbb4457c9b714ee6acd4185b')

    with open('newsapi-' + str(yesterday) + '.json', 'w') as f:
        f.write(requests.get(url).text)


def main():
    paged('\"Formula 1 Racing\"')


if __name__ == '__main__':
    main()
