import json

# with open(f'../test/newsapi/world-news.json', "r") as f:
with open(f'../test/newsapi/test.json', "r") as f:
    data = json.load(f)

titles = [article["title"] for article in data["articles"]]
duplicates = set([title for title in titles if titles.count(title) > 1])
m = ''
if duplicates:
    k = m
kk = None
