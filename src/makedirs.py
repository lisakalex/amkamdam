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
    tag.string = 'kak'
    breadcrumbs.append(tag)
    for d in dir_name:
        tag = soup.new_tag("a", href=f'/{d}/')
        tag.string = 'kak'
        breadcrumbs.append(tag)
        # link = breadcrumbs.find_all('a')
        # link[i+1]['href'] = '/' + dir_name[0] + '/'
        # link[i+1].string = dir_name[0]
        # link[i+2]['href'] = '/' + i + '/'
        # link[2].string = dir_name[1]

    button_more = soup.find('a', class_='button-more')
    button_more['loadmoretype'] = keyword

    with open(f'../html/{i}/index.html', 'w') as f:
        f.write(str(soup))

    with open(f'../html/paged/{keyword}-1.json', 'w') as f:
        f.write('[]')
