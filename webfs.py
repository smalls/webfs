#!/usr/bin/env python
#
# (c) 2017 Matt Small
#

import sys

from errno import ENOENT
from stat import S_IFDIR
from sys import argv
from time import time
import logging

from fuse import FUSE, FuseOSError, Operations, LoggingMixIn

import requests
from bs4 import BeautifulSoup as bs


class WebFS(Operations):
	__page = None

	def __init__(self, rootUrl, relative=None):
		self.__page = Page(rootUrl)
	
	def __get_page(self, path):
		""" Split the path into entries, and use those names to recurse
		along the list of pages. """

		if path == '/':
			return self.__page

		entries = path.split('/')[1:]
		print('elements: %s from path %s' % (entries, path))

		if not entries:
			return self.__page
		else:
			return self.__page.recurse(entries)


	def getattr(self, path, fh=None):

		page = self.__get_page(path)
		print('getattr(%s), page: %s' % (path, page))

		if page:
			return dict(st_mode=(S_IFDIR | 0o755), st_ctime=time(),
								   st_mtime=time(), st_atime=time(), st_nlink=2)

		if path not in ['/']: # or not inlist:
			raise FuseOSError(ENOENT)

		return dict(st_mode=(S_IFDIR | 0o755), st_ctime=time(),
							   st_mtime=time(), st_atime=time(), st_nlink=2)

	def readdir(self, path, fh):
		print('readdir(%s)' % path)
		page = self.__get_page(path)

		entries = ['.', '..']
		entries.extend(page.child_names())
		for e in entries:
			yield e
	
class Page(object):
	"""
	Represents a webpage.
	"""

	__urls_by_name = {}
	__cached_children = {}
	__url = None

	def __init__(self, url):
		self.__url = url
		self.__urls_by_name = {}
		self.__cached_children = {}

		body = self._get_data(url)

		soup = bs(body, 'html.parser')
		for anchor in soup.find_all('a'):
			target = anchor['href']
			if anchor.string is not None:
				name = anchor.string
			else:
				name = target
			self.__urls_by_name[name] = target
	
	def _get_data(self, url):
		return requests.get(url).text

	def _create_child(self, url):
		return Page(url)
	
	def child_names(self):
		"""
		Returns a list of valid children of this page (the names which can be
		iterated down).
		"""
		return self.__urls_by_name.keys()
	
	def recurse(self, linknames):
		"""Returns the page specified by the list of link names (`linknames`)."""
		name = linknames[0]
		linknames = linknames[1:]
		print ('recurse name %s linknames %s' % (name, linknames))

		if name not in self.__urls_by_name:
			return None

		if name in self.__cached_children:
			page = self.__cached_children[name]
		else:
			page = self._create_child(self.__urls_by_name[name])
			self.__cached_children[name] = page

		if not linknames:
			return page
		else:
			return page.recurse(linknames)

def main(rootUrl, mountpoint):
	# XXX logging.basicConfig(level=logging.DEBUG)
	FUSE(WebFS(rootUrl), mountpoint, nothreads=True, foreground=True)

if __name__=='__main__':
	main(sys.argv[1], sys.argv[2])
