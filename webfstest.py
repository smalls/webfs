#!/usr/bin/env python
#
# (c) 2017 Matt Small
#

import unittest
from unittest.mock import MagicMock, patch

from webfs import Page

class MockedPage(Page):
    simplepage="""
    <html>
    <body>
        <a href="http://www.foo.com/first.html"/>
        <a href="second.gif">second name</a>
    </body>
    </html>
    """

    anothersimplepage="""
    <html>
    <body>
        <a href="third.html"/>
        <a href="fourth.gif">fourth name</a>
        <a href="5.gif">5 name</a>
    </body>
    </html>
    """

    def _get_data(self, url):
        if url == 'http://www.foo.com':
            return self.simplepage
        else:
            return self.anothersimplepage

    def _create_child(self, url):
        return MockedPage(url)

class PageTest(unittest.TestCase):

    def testSimplePage(self):
        page = MockedPage('http://www.foo.com')
        self.assertEqual(2, len(page.links().keys()))
        self.assertTrue('http://www.foo.com/first.html' in page.links().keys())
        self.assertEqual('http://www.foo.com/first.html', page.links()['http://www.foo.com/first.html'])
        self.assertTrue('second name' in page.links().keys())

    def testRecurseToChild(self):
        page = MockedPage('http://www.foo.com')

        child = page.child('http://www.foo.com/first.html')
        self.assertEqual(3, len(child.links().keys()))
        self.assertTrue('third.html' in child.links().keys())

        child = page.child('http://www.foo.com/first.html')

if __name__=='__main__':
    unittest.main()
