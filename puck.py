import os
import sys
import math
import json
import random
import imghdr
import shutil
import urllib.request
import urllib.parse

from colorthief import ColorThief


def main():
	if len(sys.argv) != 2:
		print('usage: python puck.py [url|subreddit|filepath]')
		sys.exit(1)

	# To bypass user-agent retrictions
	opener = urllib.request.build_opener()
	opener.addheaders = [
		('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')
	]
	urllib.request.install_opener(opener)

	if os.path.exists('wallpaper.png'):
		os.remove('wallpaper.png')

	if os.path.exists(sys.argv[1]):
		try:
			if imghdr.what(sys.argv[1]) is None:
				print("error: The specified file is not an image.")
				sys.exit(1)
		except IsADirectoryError:
			print('error: You passed a folder, not an image.')
			sys.exit(1)

		shutil.copy(sys.argv[1], 'wallpaper.png')

	elif urllib.parse.urlparse(sys.argv[1]).scheme == "":
		print("=> Downloading..")
		success = False

		while not success:
			url = grab_random_picture(sys.argv[1])
			urllib.request.urlretrieve(url, 'wallpaper.png')

			if imghdr.what('wallpaper.png') is not None:
				success = True
			else:
				print('Not a valid image, trying again..')
	else:
		print("=> Downloading..")
		print(sys.argv[1])
		urllib.request.urlretrieve(sys.argv[1], 'wallpaper.png')
		
	print("=> Setting wallpaper")
	os.system("gsettings set org.gnome.desktop.background picture-uri 'file:///home/jude/puck/wallpaper.png'")


def grab_random_picture(subreddit):
	print("=> Grabbing random top wallpaper from /r/{}".format(sys.argv[1]))

	request = urllib.request.urlopen('https://www.reddit.com/r/{}/top/.json?count=100&limit=100&t=month'.format(subreddit))
	data = json.loads(request.read().decode(request.info().get_param('charset') or 'utf-8'))

	posts = data['data']['children']

	index = random.randint(0, len(posts))

	post = posts[index]['data']

	url = post['url']

	if urllib.parse.urlparse(post['url']).netloc == 'imgur.com' and (
		not url.endswith('.png') and not url.endswith('.jpg') and not url.endswith('.jpeg') and not url.endswith('.gif')
	):
		url = '{}.png'.format(url)

	print(post['title'])
	print(url)

	return url

if __name__ == '__main__':
	main()
