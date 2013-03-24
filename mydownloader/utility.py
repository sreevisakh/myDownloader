import re
import urllib2
import os


def validateUrl(url):
	""" Helps to validate urls"""
	try:
		regex = re.compile(r'^(?:http|ftp)s?://' # http:// or https://
		r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
		r'localhost|' #localhost...
		r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
		r'(?::\d+)?' # optional port
		r'(?:/?|[/?]\S+)$', re.IGNORECASE)
		match = regex.match(url)
		if match:
			return 1
		else:
			return 0
	except Exception:
		return 0

def human_readable(num):
	num = int(num)
	for x in ['bytes','KB','MB','GB','TB']:
		if num < 1024.0:
			return "%3.1f %s" % (num, x)
		num /= 1024.0


def getUrlDetails(url):
	"""gets url details"""
	try:
		#stores url details
		details={}
		
		#getting and parsing and storing
		urlFile = urllib2.urlopen(url)
		urlDetails = str(urlFile.info())
		details = dict(map(str.strip, line.split(':', 1)) for line in urlDetails.splitlines())
		details['error']=""
		details['url']=urlFile.geturl(	)
		if 'Content-Length'in  details:
			details['Content-Length'] = str(human_readable(details['Content-Length']))
		else:
			details['Content-Length'] ="Unavailable"
		#checking filetype
		if 'text/html' in details['Content-Type'] and os.path.basename(details['url'])=="": #if no filename
			details['url']=urlFile.geturl()+"index.html"

		details['filename'] = str.split(os.path.basename(details['url']),'?',1)[0]
		details['error']=""
		return details
	except Exception as e:
		details['error'] = e
		return details
	
	
