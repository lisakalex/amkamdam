#!/home/al/.venv/bin/python3
import glob2
from bs4 import BeautifulSoup
import requests
import time
from pathlib import Path
import shutil
from datetime import datetime

dirs = ['sport/boxing-sport',
        'sport/cricket-sport',
        'sport/football-sport',
        'sport/formula-1-racing',
        'sport/tennis-sport',
        'culture/popular-films',
        'culture/music',
        'culture/books',
        'culture/art',
        'culture/photography',
        'lifestyle/shopping',
        'lifestyle/beauty',
        'lifestyle/tech-news',
        'lifestyle/money',
        'lifestyle/fashion',
        'finance/financial-markets',
        'finance/property-market',
        'finance/stocks-and-shares',
        'finance/brexit',
        'finance/crypto'
        # 'xxx',
        # 'xxx',
        # 'xxx',
        # 'xxx',
        # 'xxx',
        # 'xxx',
        # 'xxx',
        # 'xxx',
        # 'xxx',
        # 'xxx',
        # 'xxx',
        # 'xxx',
        # 'xxx',
        # 'xxx',
        # 'xxx',
        # 'xxx',
        # 'xxx',
        # 'xxx',
        # 'xxx',
        # 'xxx',
        # 'xxx',
        # 'xxx',
        # 'xxx',
        # 'xxx',
        # 'xxx',
        # 'xxx',
        # 'xxx',
        # 'xxx',
        # 'xxx',
        # 'xxx',
        # 'xxx',
        # 'xxx',
        # 'xxx',
        # 'xxx',
        # 'xxx',
        # 'xxx',
        # 'xxx',
        # 'xxx',
        # 'xxx',
        # 'xxx'
        ]

for i in dirs:
    Path('../html/' + i).mkdir(parents=True, exist_ok=True)
    Path('../html/paged').mkdir(parents=True, exist_ok=True)
    Path('../test/newsapi').mkdir(parents=True, exist_ok=True)
    dir_name = i.split('/')

    with open('me-index.html', 'r') as f:
        soup = BeautifulSoup(f.read(), features='html.parser')

    breadcrumbs = soup.find('div', class_='breadcrumbs')
    link = breadcrumbs.find_all('a')
    link[1]['href'] = '/' + dir_name[0] + '/'
    link[1].string = dir_name[0]
    link[2]['href'] = '/' + i + '/'
    link[2].string = dir_name[1]

    buttonmore = soup.find('a', class_='button-more')
    buttonmore['loadmoretype'] = dir_name[1]

    with open('../html/' + i + '/index.html', 'w') as f:
        f.write(str(soup))

    buttonmore = soup.find('a', class_='button-more')
    buttonmore['loadmoretype'] = dir_name[0]

    link[2].decompose()
    with open('../html/' + dir_name[0] + '/index.html', 'w') as f:
        f.write(str(soup))

    with open('../html/paged/' + dir_name[0] + '-1.json', 'w') as f:
        f.write('[]')

    with open('../html/paged/' + dir_name[1] + '-1.json', 'w') as f:
        f.write('[]')
