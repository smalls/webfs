# WebFS


## Getting Started

I've only tested this on a Mac, but I'd imagine that it'd work anywhere
that has [FUSE](https://github.com/libfuse/libfuse).

On the Mac, that means [osxfuse](https://github.com/osxfuse/osxfuse).
There are other ways of getting [osxfuse](https://github.com/osxfuse/osxfuse)
installed, but [Homebrew](http://brew.sh) is pretty easy:

	brew cask install osxfuse

Clone this repo, and:

	virtualenv venv-webfs
	source venv-webfs/bin/activate
	pip install -r requirements.txt

Make sure that the unit tests are passing:

	python webfstest.py


## Sources

Credit where it's due. I took inspiration from:

 * https://www.stavros.io/posts/python-fuse-filesystem/
 * https://medium.com/the-python-corner/writing-a-fuse-filesystem-in-python-5e0f2de3a813
 * https://github.com/terencehonles/fusepy
