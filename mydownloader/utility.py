import re
import urllib2
import os
from gi.repository import Gtk
import sqlite3 as db
import traceback
import threading
import time
	#bad
	#global url1 = "http://google.com"
	#global url2 = "ht"
	#global url3 = "http://www.python.org/ftp/python/2.7.3/python-2.7.3.msi"
	#global url4 = "http://www.python.org/ftp/python/2.7.3/"

	#global url6 = "support.google.com/webmasters/bin/answer.py"

DOWNLOAD_DIR="/home/sv/Downloads/"
TEMP_DIR="/tmp/"

class DownloadItem:
    did=0
    ori_file_name=""
    download_name=""
    url = ""
    size=0
    download_size=0
    progress=0
    downloadHandler=""

    def __init__(self,did):
        self.did = did
        self.load_item()
    def __str__(self):
        print "ID: "+str(self.did)
        print "Orginal File Name: "+self.ori_file_name
        print "Download Name: "+self.download_name
        print "URL: "+self.url
        print "Size: "+human_readable(self.size)
        return ""

    def load_item(self):
        con = None
        try:
            con=db.connect('dlList.db')
            cursor = con.cursor()
            sql = "SELECT * FROM downloads WHERE id="+str(self.did)
            cursor.execute(sql)
            row = cursor.fetchone()
            self.ori_file_name = str(row[1])

            if row[4]=="":
                self.download_name = findFileName(self.ori_file_name)
                updateLoc(self.did,self.ori_file_name)
            else:
                self.download_name = str(row[4])
            self.url = str(row[2])
            self.size = long(row[3])
            self.progress = int(self.calcPercent())
            return
        except IOError as e:
            print e
    def calcPercent(self):
        download_size=0
        per = 0
        if os.path.exists(TEMP_DIR+self.download_name):
            download_size = os.path.getsize(TEMP_DIR+self.download_name)
        if self.size !=0:
            per = float(download_size) / float(self.size) * 100
        return per

###################################################
###Threading Section###############################
###################################################

class DownloadThread(threading.Thread):
    def __init__(self,DItem):
        threading.Thread.__init__(self)
        self.url=DItem.url
        self.filename = DItem.download_name
        self.completed = False
    def run(self):
        os.system('axel -an 1 '+self.url+' --output=/tmp/'+self.filename)
        for row in self.list:
            if row[0] == self.DItem.did:
                listIter = row.iter

class ProgressThread(threading.Thread):
    def __init__(self,DItem,window):
            threading.Thread.__init__(self)
            self.DItem = DItem
            #print DItem
            self.size = DItem.size
            self.filename = DItem.download_name
            self.progress = DItem.progress
            self.completed = False
            self.list = window.builder.get_object('liststore1')
            #print self.list
    def run(self):
        count=0
        for row in self.list:
            if row[0] == self.DItem.did:
                listIter = row.iter
                
        while not self.completed:
            count=count+1
            if count==5:
                self.completed = True
            #print self.list[0][1]
            #self.DItem.calcPercent()
            #if self.DItem.progress==100:
            #    self.completed = True
            self.list.set_value(listIter,4,self.DItem.progress)
            time.sleep(1)



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
	except IOError:
		return 0

def human_readable(num):
	num = long(num)
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
			details['Content-Length'] = str((details['Content-Length']))
		else:
			details['Content-Length'] ="Unavailable"
		#checking filetype
		if 'Content-Type' in details:
		    if 'text/html' in details['Content-Type'] and os.path.basename(details['url'])=="": #if no filename
			    details['url']=urlFile.geturl()+"index.html"
		details['filename'] = str.split(os.path.basename(details['url']),'?',1)[0]

		return details
	except IOError as e:
		return e


def status(window,msg):
	window.ui.label2.set_text(msg)

def addUrl(window,url):
	"""Function used to add url to download list"""
	#try:

	#check already exists
	result = checkUrlExists(window,url)
	if result==1:
		handleError(window,"Duplicate Download",Gtk.MessageType.WARNING) # NEED UPDATE
		return 0
	status(window,'Validating')
	result = validateUrl(url)
	if result == 0:
		handleError(window,"Can't add malformed url",Gtk.MessageType.ERROR)
	else:
		status(window,'Getting URL details')
		result = getUrlDetails(url)
		if type(result) ==dict:
			status(window,'Adding to List')
			if addToDb(window,result):
				listObject = window.builder.get_object('liststore1') #dependant
				listObject.append([1,result['filename'],result['url'],str(human_readable(result['Content-Length'])),"0%",""])
			status(window,'Idle')
			return 0
		else:
			handleError(window,result,Gtk.MessageType.WARNING)
			return 0
	#except IOError as e:
	#	handleError(window,e,Gtk.MessageType.ERROR)
	#	return 0

def findFileName(filename):
	"""Find non exist filename to save download content"""
	num = 0
	while os.path.exists(TEMP_DIR+filename) or os.path.exists(DOWNLOAD_DIR+filename):
		name,ext = os.path.splitext(filename)
		name = name+"("+str(num)+")"
		filename = name+ext
	return filename

def calcPer(file_id):
	try:
		con=db.connect('dlList.db')
		dlSize=0
		cursor = con.cursor()
		sql = "SELECT loc,size FROM downloads WHERE id="+str(file_id)
		cursor.execute(sql)
		row = cursor.fetchone()
		totalSize = row[1]
		fileloc= row[0]
		con.close()
		if os.path.exists(os.path.getsize(TEMP_DIR+fileloc)):
			dlSize = os.path.getsize(TEMP_DIR+fileloc)
		per = long(dlSize)/long(totalSize) *100
		return str(per)+"%"
	except Exception:
		return "0%"
		
def checkandUpdate(store,percent,treeiter):
    
    store.set_value(treeiter,4,str(int(percent))+"%")


#######################################
# DB RELATED CODES
#######################################

def addToDb(window,d):
	"""Add download urls to database"""
	con = None
	try:
		con = db.connect('dlList.db')
		sql = "INSERT INTO downloads (filename,fileurl,size,loc) values('"+d['filename']+"','"+d['url']+"','"+d['Content-Length']+"','')"
		con.execute(sql)
		con.commit()
		return 1
	except IOError as e:
		handleError(window,e,Gtk.MessageType.ERROR)
		return 0

def loadFromDb(window):
	"""Load download list from db"""
	con = None
	try:
		con=db.connect('dlList.db')
		cursor = con.cursor()
		sql = "SELECT * FROM downloads"
		cursor.execute(sql)
		rows = cursor.fetchall()
		listObject = window.builder.get_object('liststore1') #dependant
		for result in rows:

			listObject.append([result[0],result[1],result[2],human_readable(result[3]),calcPer(result[0]),result[4]])
		return
	except IOError as e:
		handleError(window,e,Gtk.MessageType.ERROR)

def checkUrlExists(window,url):
	"""Checks and return if url already in downloadlist"""
	con = None
	try:
		con=db.connect('dlList.db')
		cursor = con.cursor()
		sql = "SELECT * FROM downloads WHERE fileurl='"+url+"'"
		cursor.execute(sql)
		rows = cursor.fetchall()
		if len(rows)>0:
			return 1
		else:
			return 0
	except IOError as e:
		handleError(window,e,Gtk.MessageType.ERROR)
def updateLoc(a,b): #a=Id,b=filename
	"""Update download location of file"""
	con = None
	try:
		con=db.connect('dlList.db')
		cursor = con.cursor()
		sql = "UPDATE downloads SET loc='"+b+"' WHERE id="+str(a)
		cursor.execute(sql)
		con.commit()
	except IOError as e:
		print e
def handleError(window,e,t):
	"""Handles error Messages via messagebox"""
	if type(e)==IOError:
		traceback.print_last()
	msg = Gtk.MessageDialog(parent=window, flags=0, type=t, buttons=Gtk.ButtonsType.OK, message_format=str(e))
	msg.run()
	msg.destroy()





