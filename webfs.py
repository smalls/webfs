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
	"""
	Represents a webpage.
	"""

	__links = {}
	__cached_children = {}

	def __init__(self, url):
		self.__links = {}
		self.__cached_children = {}

		body = self._get_data(url)

		soup = bs(body, 'html.parser')
		for anchor in soup.find_all('a'):
			target = anchor['href']
			if anchor.string is not None:
				name = anchor.string
			else:
				name = target
			self.__links[name] = target
	
	def _get_data(self, url):
		return requests.get(url).text

	def _create_child(self, url):
		return Page(url)
	
	def links(self):
		"""
		Returns a list of URLs that this page links to, as Strings.
		"""
		return self.__links

	def child(self, link):
		"""
		Returns the specified child Page.

		:param link: the child URL to return; note that URL must be part of
		the set returned from `links()`.
		:returns: a Page representing the URL specified by `link`. 
		"""

		if not link in self.links():
			raise Exception('link %s must be in set links %s' %
					(link, self.links()))

		if link in self.__cached_children:
			return self.__cached_children[link]

		page = self._create_child(link)
		self.__cached_children[link] = page
		return page




def main(mountpoint, rootUrl):
	FUSE(WebFS(rootUrl), mountpoint, nothreads=True, foreground=True)

if __name__=='__main__':
	main(sys.argv[1], sys.argv[2])
