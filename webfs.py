#!/usr/bin/env python
#
# (c) 2017 Matt Small
#

import sys

from errno import ENOENT
from stat import S_IFDIR
from sys import argv
from time import time

from fuse import FUSE, FuseOSError, Operations, LoggingMixIn

import requests
from bs4 import BeautifulSoup as bs


class WebFS(Operations):
	__rootPage = None

	def __init__(self, rootUrl):
		self.__rootPage = Page(rootUrl)

	def getattr(self, path, fh=None):
		if path not in ['/', '/foo']:
			raise FuseOSError(ENOENT)

		return dict(st_mode=(S_IFDIR | 0o755), st_ctime=time(),
							   st_mtime=time(), st_atime=time(), st_nlink=2)

	def readdir(self, path, fh):
		entries = ['.', '..', 'foo']
		for e in entries:
			yield e
	
class Page(object):
	__links = {}
	__children = {}

	def __init__(self, url):
		body = self._get_data(url)

		soup = bs(body, 'html.parser')
		for anchor in soup.find_all('a'):
			target = anchor['href']
			if anchor.string is not None:
				name = anchor.string
			else:
				name = target
			self.__links[name] = target
			#self.__children[name] = Page(target)
	
	def _get_data(self, url):
		return requests.get(url).text
	
	def links(self):
		return self.__links


def main(mountpoint, rootUrl):
	FUSE(WebFS(rootUrl), mountpoint, nothreads=True, foreground=True)

if __name__=='__main__':
	main(sys.argv[1], sys.argv[2])
