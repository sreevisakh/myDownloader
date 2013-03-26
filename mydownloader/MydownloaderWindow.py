# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
### BEGIN LICENSE
# This file is in the public domain
### END LICENSE

import gettext
import os
import time
from gettext import gettext as _
gettext.textdomain('mydownloader')
import thread
from gi.repository import Gtk # pylint: disable=E0611
import logging
logger = logging.getLogger('mydownloader')
import utility
import pdb
import thread
import gobject
import subprocess as sp
from mydownloader_lib import Window
from mydownloader.AboutMydownloaderDialog import AboutMydownloaderDialog
from mydownloader.PreferencesMydownloaderDialog import PreferencesMydownloaderDialog
from mydownloader.AddnewdownloadDialog import AddnewdownloadDialog
# See mydownloader_lib.Window.py for more details about how this class works
class MydownloaderWindow(Window):
    __gtype_name__ = "MydownloaderWindow"
    priority = 0
    handles={}
    downloading=[]
    def finish_initializing(self, builder): # pylint: disable=E1002
        """Set up the main window"""
        super(MydownloaderWindow, self).finish_initializing(builder)

        self.AboutDialog = AboutMydownloaderDialog
        self.PreferencesDialog = PreferencesMydownloaderDialog
        self.set_position(0)
        gobject.idle_add(utility.loadFromDb,self)
        # Code for other initialization actions should be added here.

    def on_mnu_new_activate(self,widget,data=None):
        adder = AddnewdownloadDialog()
        result = adder.run()
        url = adder.get_url
        adder.destroy()
        if result==Gtk.ResponseType.OK:
            gobject.idle_add(utility.addUrl,self,url)

   # def on_treeview1_selection_changed(window,selection):
       # print "Selected"
       # listStoreObject,treepath =  selection.get_selected_rows()
        #print listStoreObject[0][1]
    def on_treeview1_button_press_event(self, treeview, event):
        if event.button == 3:   #right click
            x = int(event.x)
            y = int(event.y)
            time = event.time
            treeview.grab_focus()
            pthinfo = treeview.get_path_at_pos(x, y)
            if pthinfo is not None:
                
                path, col, cellx, celly = pthinfo
                treeview.grab_focus()
                treeview.set_cursor( path, col, 0)
                
                listStore,treeiter= treeview.get_selection().get_selected()
                if treeiter is not None:
                    print listStore.get_value(treeiter,0)
                    self.ui.mnu_popup.popup(None,None,None,None,event.button,time)

            return True

    def on_Start_clicked(self,widget,data=None):
        listStore,treeiter = self.ui.treeview1.get_selection().get_selected()
        if treeiter is not None:
            #read id and url
            download_id = listStore.get_value(treeiter,0)
            download_url = listStore.get_value(treeiter,2)
            print download_url
            # gets a non existant name for the file
            filename = utility.findFileName(listStore.get_value(treeiter,1))
            print filename

            # updates location value in database
            utility.updateLoc(download_id,filename) 
                        
            #start download thread
            apt = sp.Popen(['axel','-n 1','-a',download_url,'--output=/tmp/'+filename],stdout = sp.PIPE)
            #print apt.stdout.read()
            self.downloading.append(download_id)

            #check filesize to get progress
            #thread.start_new_thread(self.pulse,(download_id,))

    def pulse(d_id):
        sleep(5)
        print calcPer(d_id)
        
