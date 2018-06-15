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
<html>
	<head>
		<meta charset="utf-8">
		<meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">
		<title>%s</title>
		<style type="text/css">
			html, body, * {
				margin: 0;
				padding: 0;
			}
			#index {
				position: absolute;
				width: 100%%;
			}
			#content {
				position: absolute;
				width: 70%%;
				left: 25%%;
			}
		</style>
		<link href="../css/zTreeStyle.css" rel="stylesheet">
		<link href="../css/markdown.css" media="all" rel="stylesheet" type="text/css"/>
		<script type="text/javascript" src="../js/jquery-1.4.4.min.js"></script>
		<script type="text/javascript" src="../js/jquery.ztree.core-3.5.js"></script>
		<script type="text/javascript" src="../js/ztree_toc.js"></script>
		<script type="text/javascript">
			$(function () {
				$('#readme').css({
					// 'width':'70%%',
					// 'margin-left':'25%%'
				});
				$('#tree').ztree_toc({
					debug:false,
					is_auto_number:true,
					documment_selector:'.markdown-body',
					ztreeStyle: {
						width:'25%%',
						overflow: 'auto',
						position: 'fixed',
						// 'padding-top': '88px',
						'z-index': 2147483647,
						border: '0px none',
						'border-right': '1px dotted #efefef',
						left: '0px',
						top: '0px',
						// 'overflow-x': 'hidden',
						'height': $(window).height() + 'px'
					}
				});

			});

		</script>
	</head>
	<body style="width: auto; height: auto;">
	    <div id="index">
			<div>
				<ul id="tree" class="ztree" style='width:100%%'>

				</ul>
			</div>
		</div>

		<div id="content">
			<div id='readme' style='width:70%%; margin-left:10%%;'>
				<article class='markdown-body'>
%s
	</article>
			</div>
		</div>
	</body>
</html>
		'''
		ret = markdown.markdown(text,extensions=exts)
		with open('./dist/' + os.path.basename(path)[:-2]  + 'html', 'wb') as file:
			file.write((html % (os.path.basename(path), ret)).encode('utf-8'))
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