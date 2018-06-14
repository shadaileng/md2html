#!/usr/bin/python3
#-*- coding: utf-8 -*-

"""
	*****************
	*    MD2HTML    *
	*****************
	     PowerBy %s
"""

__author__ = "Shadaileng"

import markdown, time, sys, os

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class MyFileSystemEventHandler(FileSystemEventHandler):
	def __init__(self, fn):
		super(MyFileSystemEventHandler, self).__init__()
		self.covert = fn
	def on_any_event(self, event):
		print(event.key)
		if event.key[0] in ['moved', 'modified'] and event.key[1].endswith('.md'):
			print('Markdown(%s) file changed' % event.key[1])
			self.covert(event.key[2])

def start_watch(path, callback):
	# paths = ('./' if(path.rfind('/') < 0 and path.rfind('\\') < 0) else path[:(path.rfind('/') < 0 or path.rfind('\\')) + 1], path[0 if(path.rfind('/') < 0 and path.rfind('\\') < 0) else (path.rfind('/') or path.rfind('\\')) + 1:])
	observer = Observer()
	observer.schedule(MyFileSystemEventHandler(md2html), os.path.dirname(path), recursive=True)
	observer.start()
	md2html(path)
	try:
		while(True):
			time.sleep(0.5)
	except KeyboardInterrupt:
		observer.stop()
	observer.join()



def md2html(path):
	text = ''
	with open(path, 'rb') as file:
		text = file.read().decode("UTF-8")

	if '' != text:
		exts = ['markdown.extensions.extra', 'markdown.extensions.codehilite','markdown.extensions.tables','markdown.extensions.toc']

		html = '''<!DOCTYPE html>
<html lang="zh-cn">
	<head>
		<meta content="text/html; charset=utf-8" http-equiv="content-type" />
		<link href="../markdown.css" rel="stylesheet">
	</head>
	<body>
		%s
	</body>
</html>
		'''
		ret = markdown.markdown(text,extensions=exts)
		with open('./dist/' + os.path.basename(path)[:-2]  + 'html', 'wb') as file:
			file.write((html % ret).encode('utf-8'))
#		print(html % ret)

_usage = '''
	Usage: python3 src/md2html.py path
'''

if __name__ == '__main__':
	print(__doc__ % __author__)
	argv = sys.argv[1:]
	print(argv)
	if len(argv) < 1:
		print(_usage)
	else:
		path = argv[0]
		if os.path.exists(path) and path.endswith('.md'):
			# start_watch(path, None)
			md2html(path)
		else:
			print('%s 不存在' % path)