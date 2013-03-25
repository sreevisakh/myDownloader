# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
### BEGIN LICENSE
# This file is in the public domain
### END LICENSE

import gettext
from gettext import gettext as _
gettext.textdomain('mydownloader')
import thread
from gi.repository import Gtk # pylint: disable=E0611
import logging
logger = logging.getLogger('mydownloader')
import utility
import pdb
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
    def printme(st):
        print st
    def on_mnu_new_activate(self,widget,data=None):
        dir(logger)
        adder = AddnewdownloadDialog()
        result = adder.run()
        url = adder.get_url
        adder.destroy()
        self.printme("hello1")
        thread.start_new_thread(self.printme, ("hello", ))
        pdb.pm()


