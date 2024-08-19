import requests
from datetime import date, timedelta

y = date.today() - timedelta(days=1)
yesterday = y.strftime('%Y-%m-%d')

url = ('https://newsapi.org/v2/everything?'
       'q=finance&' + yesterday + '&'
       # 'from=2024-08-09&'
       # 'to=2024-08-09&'
       'sortBy=publishedAt&'
       'language=en&'
       # 'page=3&'
       'apiKey=41e2e097fbb4457c9b714ee6acd4185b')
# GET https://newsapi.org/v2/everything?q=apple&from=2024-08-09&to=2024-08-09&sortBy=popularity&apiKey=41e2e097fbb4457c9b714ee6acd4185b

with open("newsapi/newsapi.json", "w") as file:
    file.write(requests.get(url).text)



huy = None
