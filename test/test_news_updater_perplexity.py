import unittest
from unittest.mock import patch, mock_open, MagicMock
from bs4 import BeautifulSoup
from datetime import datetime
from collections import deque
from news_updater import NewsUpdater  # Assuming the class is in a file named news_updater.py


class TestNewsUpdater(unittest.TestCase):

    def setUp(self):
        self.updater = NewsUpdater()

    def test_init(self):
        self.assertIsInstance(self.updater.start_time, float)
        self.assertIsInstance(self.updater.today_time, str)
        self.assertEqual(self.updater.count_replace, 1)

    @patch('builtins.open', new_callable=mock_open, read_data='{"articles": []}')
    def test_load_news_api(self, mock_file):
        result = self.updater.load_news_api('test')
        self.assertEqual(result, {"articles": []})
        mock_file.assert_called_once_with('../test/newsapi/test.json', 'r')

    def test_filter_articles(self):
        articles = [
            {"url": "https://example.com", "source": {"name": "Test"}, "title": "Test", "description": "Test", "urlToImage": "test.jpg", "publishedAt": "2023-01-01", "content": "Test"},
            {"url": "https://removed.com", "source": {"name": "Test"}, "title": "Test", "description": "Test", "urlToImage": "test.jpg", "publishedAt": "2023-01-01", "content": "Test"},
            {"url": "https://example.com", "source": {}, "title": "Test", "description": "Test", "urlToImage": "test.jpg", "publishedAt": "2023-01-01", "content": "Test"},
        ]
        filtered = self.updater.filter_articles(articles)
        self.assertEqual(len(filtered), 1)
        self.assertEqual(filtered[0]['url'], "https://example.com")

    def test_update_article(self):
        article_html = '<article><a class="article__image"></a><img><a class="article__badge"></a><div class="article__badge-date"></div><a class="article__title"></a></article>'
#         article_html = """
#                         <article class="mb-30">
#     <div class="row">
#         <div class="col-4 col-md-12">
#             <a class="article__image article__image--sm-wider mb-15" href="/news/best-bitcoin-gambling-sites.htm">
#                 <div class="img-sized"><img alt="40+ Best Crypto &amp; Bitcoin Gambling Sites in 2023" class="img-fluid" loading="auto" src="https://cimg.co/news/88020/239918/lucky-block-casino.jpg" srcset="https://cimg.co/news/88020/239918/responsive-images/lucky-block-casino___media_library_original_960_540.jpg 960w, https://cimg.co/news/88020/239918/responsive-images/lucky-block-casino___media_library_original_900_506.jpg 900w, https://cimg.co/news/88020/239918/responsive-images/lucky-block-casino___media_library_original_720_405.jpg 720w, https://cimg.co/news/88020/239918/responsive-images/lucky-block-casino___media_library_original_600_338.jpg 600w, https://cimg.co/news/88020/239918/responsive-images/lucky-block-casino___media_library_original_300_169.jpg 300w" width="960"/></div>
#             </a>
#         </div>
#         <div class="col-8 col-md-12">
#             <div class="article__badge article__badge--sm">
#                 <a class="article__badge article__badge--sm" href="/news/sponsored/"> Sponsored </a>
#                 <div class="article__badge-date d-md-inline-block" data-utctime="2023-09-20 06:38:00"></div>
#             </div>
#             <a class="article__title article__title--md article__title--featured" href="/news/best-bitcoin-gambling-sites.htm">
#                 <h4>40+ Best Crypto &amp; Bitcoin Gambling Sites in 2023</h4>
#             </a>
#         </div>
#     </div>
# </article>
#
#                         """
        article = BeautifulSoup(article_html, 'html.parser')
        news_item = {
            "url": "https://example.com",
            "urlToImage": "test.jpg",
            "title": "Test Title",
            "source": {"name": "Test Source"},
            "publishedAt": "2023-01-01T00:00:00Z"
        }
        updated = self.updater.update_article(article, news_item)
        self.assertEqual(updated.find('a', class_='article__image')['href'], "https://example.com")
        self.assertEqual(updated.find('img')['src'], "test.jpg")
        self.assertEqual(updated.find('a', class_='article__badge').string, "Test Source")
        self.assertEqual(updated.find('a', class_='article__title').string, "Test Title")

    @patch('news_updater.NewsUpdater.load_paged_articles')
    @patch('news_updater.NewsUpdater.save_paged_articles')
    def test_update_paged_articles(self, mock_save, mock_load):
        mock_load.return_value = deque()
        soup = BeautifulSoup('<article></article>', 'html.parser')
        news_articles = [{"url": "https://example.com", "source": {"name": "Test"}, "title": "Test", "publishedAt": "2023-01-01T00:00:00Z"}]
        self.updater.update_paged_articles(soup, news_articles, 'test')
        mock_save.assert_called_once()

    @patch('builtins.open', new_callable=mock_open, read_data='[]')
    def test_load_paged_articles(self, mock_file):
        result = self.updater.load_paged_articles('test')
        self.assertIsInstance(result, deque)
        mock_file.assert_called_once_with('../html/paged/test-1.json', 'r')

    @patch('builtins.open', new_callable=mock_open)
    @patch('json.dump')
    def test_save_paged_articles(self, mock_json_dump, mock_file):
        self.updater.save_paged_articles('test', deque(['article1', 'article2']))
        mock_file.assert_called_once_with('../html/paged/test-1.json', 'w')
        mock_json_dump.assert_called_once()

    def test_should_process_file(self):
        self.assertTrue(self.updater.should_process_file('test.html', '/path/to/file'))
        self.assertFalse(self.updater.should_process_file('test.jpg', '/path/to/file'))
        self.assertFalse(self.updater.should_process_file('test.html', '/path/to/assets/file'))

    @patch('news_updater.NewsUpdater.process_files')
    @patch('builtins.open', new_callable=mock_open)
    def test_run(self, mock_file, mock_process):
        self.updater.run()
        mock_process.assert_called_once()
        mock_file.assert_called_with('../test/count_replace.txt', 'a')


if __name__ == '__main__':
    unittest.main()
