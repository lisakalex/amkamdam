import unittest
from unittest.mock import patch, mock_open, MagicMock
from pathlib import Path
import os
from bs4 import BeautifulSoup

# Assuming the functions are imported from the main script
from makedirs_chatgpt import (
    create_directories, generate_breadcrumbs, modify_button, save_files, process_directories
)

class TestMainScript(unittest.TestCase):

    @patch('main_script.Path.mkdir')
    def test_create_directories(self, mock_mkdir):
        # Test that the necessary directories are created
        create_directories()

        # Check that directories were created with correct paths
        mock_mkdir.assert_any_call(parents=True, exist_ok=True)
        self.assertTrue(mock_mkdir.call_count > 2)  # Should create at least two directories

    def test_generate_breadcrumbs(self):
        html_content = """
        <div class="breadcrumbs"></div>
        """
        soup = BeautifulSoup(html_content, 'html.parser')

        # Test breadcrumb generation
        generate_breadcrumbs(soup, 'sport/boxing-sport/huy')

        breadcrumbs = soup.find_all('a')

        # Check root breadcrumb
        self.assertEqual(breadcrumbs[0].string, 'da')
        self.assertEqual(breadcrumbs[0]['href'], '/')

        # Check breadcrumb hierarchy
        self.assertEqual(breadcrumbs[1].string, 'sport')
        self.assertEqual(breadcrumbs[1]['href'], '/sport/')

        self.assertEqual(breadcrumbs[2].string, 'boxing sport')
        self.assertEqual(breadcrumbs[2]['href'], '/sport/boxing-sport/')

        self.assertEqual(breadcrumbs[3].string, 'huy')
        self.assertEqual(breadcrumbs[3]['href'], '/sport/boxing-sport/huy/')

    def test_modify_button(self):
        html_content = """
        <a class="button-more"></a>
        """
        soup = BeautifulSoup(html_content, 'html.parser')

        modify_button(soup, 'boxing-sport')

        button_more = soup.find('a', class_='button-more')

        # Check if the button-more attribute has been updated correctly
        self.assertEqual(button_more['loadmoretype'], 'boxing-sport')

    @patch("builtins.open", new_callable=mock_open)
    def test_save_files(self, mock_file):
        soup = BeautifulSoup('<html></html>', 'html
