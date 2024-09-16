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
    # Extract keyword from path
    # keyword = path_file1.split('/')[-2]
    # keyword = os.path.basename(os.path.dirname(keyword))
    base_url = 'https://newsapi.org/v2/everything'
    keyword = urllib.parse.quote_plus(keyword)
    yesterday = (date.today() - timedelta(days=1)).strftime('%Y-%m-%d')

    params = {
        'q': keyword,
        'from': yesterday,
        'sortBy': 'publishedAt',
        'language': 'en',
        'apiKey': '41e2e097fbb4457c9b714ee6acd4185b'
    }

    # Fetch and save the news data
    # response = requests.get(base_url, params=params)
    # newsapi_json = response.text
    # newsapi = response.json()

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Raise an exception for HTTP errors
        newsapi_data = response.json()

        # Save the data as a JSON file
        output_path = os.path.join('newsapi', f'{keyword}.json')
        with open(output_path, 'w') as f:
            json.dump(newsapi_data, f, indent=4)

        return newsapi_data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from the NewsAPI: {e}")
    return None

    # with open(f'{keyword}.json', 'w') as f:
    #     f.write(newsapi_json)
    #
    # return newsapi


if __name__ == '__main__':
    replace_text('formula-1-racing')
