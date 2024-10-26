#!/home/al/.venv/bin/python3
from bs4 import BeautifulSoup

with open('aa/c.htm', 'r') as f:
    soup = BeautifulSoup(f.read(), features='html.parser')

breadcrumbs = soup.find_all('span', class_='apiName--2Ofqy')
ku = []
for i in breadcrumbs:
    print(ku.append(i.text))
with open('b.txt', 'a') as f:
    for i in ku:
        f.write(i + '\n')

k = None
