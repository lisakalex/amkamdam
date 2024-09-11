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
    url = ('https://static.tweaktown.com/news/1/0/100416_2_jmgo-unveils-two-new-portable-4k-projectors-with-its-impressive-triple-laser-optics_full.jpg')
    kak = requests.get(url)
    kak1 = kak.status_code

    hu = None
    # with open('newsapi-' + str(yesterday) + '.json', 'w') as f:
    #     f.write(requests.get(url).text)


def main():
    paged('\"Formula 1 Racing\"')


if __name__ == '__main__':
    main()
