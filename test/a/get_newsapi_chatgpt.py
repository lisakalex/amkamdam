import os
import urllib.parse
import requests
import json
from datetime import date, timedelta

def replace_text(path_file1):
    # Extract the keyword from the path
    keyword = os.path.basename(os.path.dirname(path_file1)).replace('-', ' ')

    # URL encode the keyword
    encoded_keyword = urllib.parse.quote_plus(keyword)

    # Get yesterday's date
    yesterday = (date.today() - timedelta(days=1)).strftime('%Y-%m-%d')

    # Build the URL for the NewsAPI request
    url = (f'https://newsapi.org/v2/everything?'
           f'q={encoded_keyword}&from={yesterday}&sortBy=publishedAt'
           f'&language=en&apiKey=41e2e097fbb4457c9b714ee6acd4185b')

    try:
        # Fetch data from the API
        response = requests.get(url)
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

if __name__ == '__main__':
    replace_text('sport/formula-1-racing')
