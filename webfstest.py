#!/usr/bin/env python
#
# (c) 2017 Matt Small
#

import unittest
from unittest.mock import MagicMock, patch

from webfs import Page

class MockedPage(Page):
    root="""
    <html>
    <body>
        <a href="http://www.foo.com/second.html">second</a>
        <a href="second.gif">second name</a>
    </body>
    </html>
    """

    secondlevel="""
    <html>
    <body>
        <a href="http://www.baz.com/third.html">third</a>
        <a href="fourth.gif">fourth name</a>
        <a href="5.gif">5 name</a>
    </body>
    </html>
    """

    thirdlevel="""
    <html>
    <body>
        <a href="http://www.foo.com/seventh.html">seventh</a>
    </body>
    </html>
    """

    def _get_data(self, url):
        if url == 'http://www.foo.com':
            return self.root
        elif url == 'http://www.foo.com/second.html':
            return self.secondlevel
        elif url == 'http://www.baz.com/third.html':
            return self.thirdlevel
        else:
            raise Exception('unknown url: %s' % (url,))

    def _create_child(self, url):
        return MockedPage(url)

class PageTest(unittest.TestCase):

    def testSimplePage(self):
        page = MockedPage('http://www.foo.com')
        self.assertEqual(2, len(page.child_names()))
        self.assertTrue('second' in page.child_names())
        self.assertTrue('second name' in page.child_names())

    def testRecurseToChild(self):
        page = MockedPage('http://www.foo.com')

        child = page.recurse(['second'])
        self.assertEqual(3, len(child.child_names()))
        self.assertTrue('third' in child.child_names())

        child = page.recurse(['second', 'third'])
        self.assertEqual(1, len(child.child_names()))
        self.assertTrue('seventh' in child.child_names())

if __name__=='__main__':
    unittest.main()
