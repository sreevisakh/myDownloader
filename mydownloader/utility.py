import re
import urllib2
import os
from gi.repository import Gtk
	#bad
	#global url1 = "http://google.com"
	#global url2 = "ht"
	#global url3 = "http://www.python.org/ftp/python/2.7.3/python-2.7.3.msi"
	#global url4 = "http://www.python.org/ftp/python/2.7.3/"	
	#global url5 = "support.google.com/webmasters/bin/answer.py?hl=en&answer=1408986"
	#global url6 = "support.google.com/webmasters/bin/answer.py"


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
	"""gets url details result in details"""
	try:
		details={}
		#getting and parsing and storing
		urlFile = urllib2.urlopen(url)
		urlDetails = str(urlFile.info())
		details = dict(map(str.strip, line.split(':', 1)) for line in urlDetails.splitlines())
		details['error']=""
		details['url']=urlFile.geturl()
		if 'Content-Length' in  details:
			details['Content-Length'] = str(human_readable(details['Content-Length']))
		else:
			details['Content-Length'] ="Unavailable"
		#checking filetype
		if 'text/html' in details['Content-Type'] and os.path.basename(details['url'])=="": #if no filename
			details['url']=urlFile.geturl()+"index.html"
		details['filename'] = str.split(os.path.basename(details['url']),'?',1)[0]
		
		return details
	except Exception as e:
		return e




def addUrl(window,url):
	"""Function used to add url to download list"""
	try:
	
		#passing url
		result = validateUrl(url)
		if result == 0:
			handleError(window,"Can't add malformed url",Gtk.MessageType.ERROR)
		else:
			result = getUrlDetails(url)
			if type(result) ==dict:
				
				listObject = window.builder.get_object('liststore1') #dependant
				listObject.append([1,result['filename'],result['url'],result['Content-Length'],"0%",""])
				return 1
			else:
				handleError(window,result,Gtk.MessageType.WARNING)
				return 0		
	except Exception as e:
		handleError(window,e,Gtk.MessageType.ERROR)
		return 0

def handleError(window,e,t):
	"""Handles error Messages via messagebox"""
	msg = Gtk.MessageDialog(parent=window, flags=0, type=t, buttons=Gtk.ButtonsType.OK, message_format=str(e))   
	msg.run()
	msg.destroy() 

#Tests
import unittest

def unit():
	#testing validateurl
	self.assertEqual(validateUrl(self,url),details)








	
