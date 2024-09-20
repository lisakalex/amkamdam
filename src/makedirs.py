#!/home/al/.venv/bin/python3
import glob2
from bs4 import BeautifulSoup
import requests
import time
from pathlib import Path
import shutil
from datetime import datetime
import os

dirs = ['sport',
        'sport/boxing-sport',
        'sport/boxing-sport/huy',
        'sport/cricket-sport',
        'sport/football-sport',
        'sport/formula-1-racing',
        'sport/tennis-sport',
        'culture',
        'culture/popular-films',
        'culture/music',
        'culture/books',
        'culture/art',
        'culture/photography',
        'lifestyle',
        'lifestyle/shopping',
        'lifestyle/beauty',
        'lifestyle/tech-news',
        'lifestyle/money',
        'lifestyle/fashion',
        'finance',
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

Path('../html/paged').mkdir(parents=True, exist_ok=True)
Path('../test/newsapi').mkdir(parents=True, exist_ok=True)

for i in dirs:
    Path('../html/' + i).mkdir(parents=True, exist_ok=True)
    keyword = os.path.basename(i)
    dir_name = i.split('/')

    with open('me-index.html', 'r') as f:
        soup = BeautifulSoup(f.read(), features='html.parser')

    breadcrumbs = soup.find('div', class_='breadcrumbs')
    tag = soup.new_tag("a", href='/')
    tag.string = 'da'
    breadcrumbs.append(tag)
    link = '/'
    for d in dir_name:
        link = f'{link}{d}/'
        tag = soup.new_tag("a", href=link)
        dd = d.replace('-', ' ')
        tag.string = dd
        breadcrumbs.append(tag)

    button_more = soup.find('a', class_='button-more')
    button_more['loadmoretype'] = keyword

    with open(f'../html/{i}/index.html', 'w') as f:
        f.write(str(soup))

    with open(f'../html/paged/{keyword}-1.json', 'w') as f:
        f.write('[]')
