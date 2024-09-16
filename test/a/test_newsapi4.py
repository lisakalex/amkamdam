import unittest
from unittest.mock import mock_open, patch, MagicMock
from bs4 import BeautifulSoup
from collections import deque
from datetime import datetime
from newsapi4 import NewsUpdater


# Custom mock for BeautifulSoup
class MockBeautifulSoup:
    def __init__(self, *args, **kwargs):
        self.find_all_results = []
        self.find_results = {}

    def find_all(self, *args, **kwargs):
        return self.find_all_results

    def find(self, *args, **kwargs):
        return self.find_results.get(args[0], MagicMock())


class TestNewsUpdater(unittest.TestCase):
    def setUp(self):
        self.updater = NewsUpdater()

    def test_load_news_api(self):
        mock_json = '{"articles": [{"title": "Test Article"}]}'
        with patch('builtins.open', mock_open(read_data=mock_json)):
            result = self.updater.load_news_api('test')
        self.assertEqual(result, {"articles": [{"title": "Test Article"}]})

    def test_filter_articles(self):
        articles = [
            {"url": "https://example.com", "urlToImage": "image.jpg"},
            {"url": "https://removed.com", "urlToImage": "image.jpg"},
            {"url": "https://example.com", "urlToImage": None}
        ]
        result = self.updater.filter_articles(articles)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["url"], "https://example.com")

    def test_update_article(self):
        mock_article = MagicMock()
        mock_article.find.side_effect = [
            MagicMock(name='link'),
            MagicMock(name='img'),
            MagicMock(name='badge'),
            MagicMock(name='badge_date'),
            MagicMock(name='link1')
        ]
        news_item = {
            "url": "https://example.com",
            "urlToImage": "image.jpg",
            "title": "Test Title",
            "source": {"name": "Test Source"},
            "publishedAt": "2023-05-20T12:00:00Z"
        }
        self.updater.update_article(mock_article, news_item)
        mock_article.find.assert_called()

    def test_replace_text(self):
        with patch('newsapi4.BeautifulSoup', MockBeautifulSoup):
            with patch('newsapi4.NewsUpdater.load_news_api') as mock_load:
                with patch('newsapi4.NewsUpdater.filter_articles') as mock_filter:
                    mock_load.return_value = {"articles": []}
                    mock_filter.return_value = []

                    with patch('builtins.open', mock_open()):
                        self.updater.replace_text("<html></html>", "path/to/file.html")

                    mock_load.assert_called_once()
                    mock_filter.assert_called_once()

    def test_should_process_file(self):
        self.assertTrue(self.updater.should_process_file("test.html", "html/test"))
        self.assertFalse(self.updater.should_process_file("test.jpg", "html/test"))
        self.assertFalse(self.updater.should_process_file("test.html", "html/assets"))


if __name__ == '__main__':
    unittest.main()
