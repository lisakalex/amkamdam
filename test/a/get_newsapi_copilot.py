import urllib.parse
import requests
import json
from datetime import date, timedelta
import os
import urllib.parse
import requests
import json
from datetime import date, timedelta


def replace_text(keyword):
    keyword = urllib.parse.quote_plus(keyword)
    yesterday = (date.today() - timedelta(days=1)).strftime('%Y-%m-%d')
    base_url = 'https://newsapi.org/v2/everything'
    params = {
        'q': keyword,
        'from': yesterday,
        'sortBy': 'publishedAt',
        'language': 'en',
        'apiKey': '41e2e097fbb4457c9b714ee6acd4185b'
    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Raise an exception for HTTP errors
        newsapi_data = response.json()

        output_path = os.path.join('newsapi', f'{keyword}.json')
        with open(output_path, 'w') as f:
            json.dump(newsapi_data, f, indent=4)

        return newsapi_data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from the NewsAPI: {e}")
    return None


if __name__ == '__main__':
    replace_text('sport')