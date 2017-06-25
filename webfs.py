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


class WebFS(Operations):
	def __init__(self):
		pass

	def getattr(self, path, fh=None):
		if path not in ['/', '/foo']:
			raise FuseOSError(ENOENT)

		return dict(st_mode=(S_IFDIR | 0o755), st_ctime=time(),
							   st_mtime=time(), st_atime=time(), st_nlink=2)

	def readdir(self, path, fh):
		entries = ['.', '..', 'foo']
		for e in entries:
			yield e

def main(mountpoint):
	FUSE(WebFS(), mountpoint, nothreads=True, foreground=True)

if __name__=='__main__':
	main(sys.argv[1])
