#!/usr/bin/env python
#
# (c) 2017 Matt Small
#

import unittest
import os

import webfs

class PageTest(unittest.TestCase):

    def testSimplePage(self):
        with open('test_data/simplepage.html') as fd:
            page = webfs.Page('http://www.foo.com', fd.read())
            self.assertEqual(2, len(page.links()))
            self.assertTrue('first.html' in page.links())
            self.assertEqual('first.html', page.links()['first.html'])
            self.assertTrue('second name' in page.links())

if __name__=='__main__':
    unittest.main()
