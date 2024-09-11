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
    Path('html/' + i).mkdir(parents=True, exist_ok=True)
    Path('html/paged').mkdir(parents=True, exist_ok=True)
    Path('html/newsapi').mkdir(parents=True, exist_ok=True)
    paged = i.split('/')

    with open('me-index.html', 'r') as f:
        soup = BeautifulSoup(f.read(), features='html.parser')

    breadcrumbs = soup.find('div', class_='breadcrumbs')
    link = breadcrumbs.find_all('a')
    link[1]['href'] = '/' + paged[0] + '/'
    link[1].string = paged[0]
    link[2]['href'] = '/' + i + '/'
    link[2].string = paged[1]

    buttonmore = soup.find('a', class_='button-more')
    buttonmore['loadmoretype'] = paged[1]

    with open('html/' + i + '/index.html', 'w') as f:
        f.write(str(soup))

    buttonmore = soup.find('a', class_='button-more')
    buttonmore['loadmoretype'] = paged[0]

    link[2].decompose()
    with open('html/' + paged[0] + '/index.html', 'w') as f:
        f.write(str(soup))

    # with open('html/paged/' + paged[0] + '-1.json', 'w') as f:
    #     f.write('[]')
    #
    # with open('html/paged/' + paged[1] + '-1.json', 'w') as f:
    #     f.write('[]')
