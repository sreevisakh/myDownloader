# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
### BEGIN LICENSE
# This file is in the public domain
### END LICENSE

import gettext
from gettext import gettext as _
gettext.textdomain('mydownloader')

from gi.repository import Gtk # pylint: disable=E0611
import logging
logger = logging.getLogger('mydownloader')
import utility
from mydownloader_lib import Window
from mydownloader.AboutMydownloaderDialog import AboutMydownloaderDialog
from mydownloader.PreferencesMydownloaderDialog import PreferencesMydownloaderDialog
from mydownloader.AddnewdownloadDialog import AddnewdownloadDialog
# See mydownloader_lib.Window.py for more details about how this class works
class MydownloaderWindow(Window):
    __gtype_name__ = "MydownloaderWindow"
    priority = 0
    def finish_initializing(self, builder): # pylint: disable=E1002
        """Set up the main window"""
        super(MydownloaderWindow, self).finish_initializing(builder)

        self.AboutDialog = AboutMydownloaderDialog
        self.PreferencesDialog = PreferencesMydownloaderDialog
        self.set_position(0)

        # Code for other initialization actions should be added here.
    def on_mnu_new_activate(self,widget,data=None):
        dir(logger)
        adder = AddnewdownloadDialog()
        result = adder.run()
        url = adder.get_url
        adder.destroy()
        if not utility.validateUrl(url):
            msg = Gtk.MessageDialog(parent=self, flags=0, type=Gtk.MessageType.WARNING, buttons=Gtk.ButtonsType.OK, message_format="Can't Process a malformed url")   
            msg.run()
            msg.destroy()
        else:
            #check dialogbox result
            if result!=Gtk.ResponseType.OK:
                return

            details = utility.getUrlDetails(url)            
            if details['error']:
                msg = Gtk.MessageDialog(parent=self, flags=0, type=Gtk.MessageType.ERROR, buttons=Gtk.ButtonsType.OK, message_format=details['error'])   
                msg.run()
                msg.destroy()
            #add list of files to treeview
            else:
                urllist = self.builder.get_object('liststore1')
                self.priority +=1
                urllist.append([self.priority,details['filename'],details['url'],details['Content-Length'],"0%"])

    
