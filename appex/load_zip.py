# coding: utf-8

import appex
import urllib2

def main():
	if not appex.is_running_extension():
		print 'Running in Pythonista app, using test data...\n'
		url = 'https://raw.githubusercontent.com/marcus67/pyzipista/master/build/pyzipista_zip.py'
	else:
		url = appex.get_url()
	if url:
		# TODO: Your own logic here...
		print 'Input URL: %s' % (url,)

		attempts = 0
		success = False

		while attempts < 3:
			try:
				response = urllib2.urlopen(url, timeout = 5)
				content = response.read()
				f = open( "archive.py", 'w' )
				f.write( content )
				f.close()
				success = True
				break
			except urllib2.URLError as e:
				attempts += 1
				print type(e)
		
		if success:
			import archive
			archive.main()
		
	else:
		print 'No input URL found.'

if __name__ == '__main__':
	main()