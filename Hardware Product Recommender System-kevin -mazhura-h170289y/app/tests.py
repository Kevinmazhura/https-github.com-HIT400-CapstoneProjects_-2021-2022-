"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".
"""

from turtle import pd
from bs4 import BeautifulSoup
import django
from django.test import TestCase
import requests

# TODO: Configure your database in settings.py and sync before running tests.

class ViewTest(TestCase):
    """Tests for the application views."""

    if django.VERSION[:2] >= (1, 7):
        # Django 1.7 requires an explicit setup() when running tests in PTVS
        @classmethod
        def setUpClass(cls):
            super(ViewTest, cls).setUpClass()
            django.setup()

    def scrap_halsteds(self):
        url="https://www.halsteds.co.zw/"
        source=requests.get(url)
        soup=BeautifulSoup(source.text,features="html.parser")
        ps = soup.find_all("ul", {"class": "brands-slider"})
        df = []
        df = pd.DataFrame(columns=['store','menu_links', 'my_items'])
        print(df)
        #print(ps)
        # response = self.client.get('/')
        # self.assertContains(response, 'Home Page', 1, 200)

    # def test_contact(self):
    #     """Tests the contact page."""
    #     response = self.client.get('/contact')
    #     self.assertContains(response, 'Contact', 3, 200)

    # def test_about(self):
    #     """Tests the about page."""
    #     response = self.client.get('/about')
    #     self.assertContains(response, 'About', 3, 200)
