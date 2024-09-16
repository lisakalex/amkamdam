import unittest
from bs4 import BeautifulSoup
from dateutil import parser
from news_updater import NewsUpdater  # Replace 'your_module' with the actual module name


class TestNewsUpdater(unittest.TestCase):
    def setUp(self):
        self.updater = NewsUpdater()
        self.article_html = '''
        <article>
            <a class="article__image" href="old_url"></a>
            <img src="old_src" srcset="old_srcset" alt="old_alt">
            <a class="article__badge">Old Source</a>
            <div class="article__badge-date">Old Date</div>
            <a class="article__title" href="old_url">Old Title</a>
        </article>
        '''
        self.news_item = {
            'url': 'https://example.com/new',
            'urlToImage': 'https://example.com/new_image.jpg',
            'title': 'New Title',
            'source': {'name': 'New Source'},
            'publishedAt': '2023-09-15T12:00:00Z'
        }

    def test_update_article(self):
        article = BeautifulSoup(self.article_html, 'html.parser')
        updated_article = self.updater.update_article(article, self.news_item)

        # Test article__image link
        image_link = updated_article.find('a', class_='article__image')
        self.assertEqual(image_link['href'], 'https://example.com/new')

        # Test img attributes
        img = updated_article.find('img')
        self.assertEqual(img['src'], 'https://example.com/new_image.jpg')
        self.assertEqual(img['srcset'], '')
        self.assertEqual(img['alt'], 'New Title')

        # Test article__badge
        badge = updated_article.find('a', class_='article__badge')
        self.assertEqual(badge.string, 'New Source')

        # Test article__badge-date
        badge_date = updated_article.find('div', class_='article__badge-date')
        expected_date = parser.isoparse('2023-09-15T12:00:00Z').strftime('%d %b %Y')
        self.assertEqual(badge_date.string, expected_date)

        # Test article__title
        title_link = updated_article.find('a', class_='article__title')
        self.assertEqual(title_link['href'], 'https://example.com/new')
        self.assertEqual(title_link.string, 'New Title')

    def test_update_article_missing_elements(self):
        # Test with an article missing some elements
        incomplete_html = '<article><a class="article__image"></a></article>'
        article = BeautifulSoup(incomplete_html, 'html.parser')

        # This should not raise an exception
        updated_article = self.updater.update_article(article, self.news_item)

        # The existing element should be updated
        image_link = updated_article.find('a', class_='article__image')
        self.assertEqual(image_link['href'], 'https://example.com/new')

        # Missing elements should not be added
        self.assertIsNone(updated_article.find('img'))
        self.assertIsNone(updated_article.find('a', class_='article__badge'))

    def test_update_article_invalid_date(self):
        # Test with an invalid publishedAt date
        invalid_news_item = self.news_item.copy()
        invalid_news_item['publishedAt'] = 'invalid_date'

        article = BeautifulSoup(self.article_html, 'html.parser')

        # This should not raise an exception, but the date should remain unchanged
        updated_article = self.updater.update_article(article, invalid_news_item)

        badge_date = updated_article.find('div', class_='article__badge-date')
        self.assertEqual(badge_date.string, 'Old Date')
        # self.assertEqual(badge_date.string, '15 Sep 2023')


if __name__ == '__main__':
    unittest.main()
