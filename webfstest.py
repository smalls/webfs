#!/usr/bin/env python
#
# (c) 2017 Matt Small
#

import unittest
from unittest.mock import MagicMock, patch

from webfs import Page

class PageTest(unittest.TestCase):

    def testSimplePage(self):
        simplepage="""
<html>
    <body>
        <a href="first.html"/>
        <a href="second.gif">second name</a>
    </body>
</html>
        """
        with patch.object(Page, '_get_data', return_value=simplepage):
            page = Page('http://www.foo.com')
            page.method = MagicMock(return_value=3)
            self.assertEqual(2, len(page.links()))
            self.assertTrue('first.html' in page.links())
            self.assertEqual('first.html', page.links()['first.html'])
            self.assertTrue('second name' in page.links())

if __name__=='__main__':
    unittest.main()
