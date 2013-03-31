# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
### BEGIN LICENSE
# This file is in the public domain
### END LICENSE

import gettext
import os
import time
import utility
import gobject
import threading
import subprocess as sp

from gettext import gettext as _
gettext.textdomain('mydownloader')
from gi.repository import Gtk,Gdk,GObject,GLib # pylint: disable=E0611

import logging
logger = logging.getLogger('mydownloader')
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
        try: 
            pass#os.unlink('/tmp/test')
        except:
            pass
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
                   # print listStore.get_value(treeiter,0)
                    self.ui.mnu_popup.popup(None,None,None,None,event.button,time)

            return True

    def on_Start_clicked(self,widget,data=None):
        listStore,treeiter = self.ui.treeview1.get_selection().get_selected()
        
        if treeiter is not None:
            #read id
        
            download_id = listStore.get_value(treeiter,0)
            if download_id not in self.downloading:
                dItem = utility.DownloadItem(download_id)
                print dItem
                fnull = open(os.devnull,'w')
                handler = sp.Popen(['axel','-n 1','-a',dItem.url,'--output=/tmp/'+dItem.download_name],stdout=fnull)
                self.handles[download_id]=handler
                GLib.timeout_add(500,self.calc,dItem,treeiter)
                
                self.downloading.append(download_id)
    def on_Stop_clicked(self,widget,data=None):
        listStore,treeiter = self.ui.treeview1.get_selection().get_selected()
        if treeiter is not None:  
            download_id = listStore.get_value(treeiter,0)
            if download_id in self.downloading:    
                h = self.handles[download_id]
                if h is not None:
                    h.terminate()
                    self.downloading.remove(download_id)
                    
                    
                        
    def calc(self,dItem,treeiter):
        per=dItem.calcPercent()
        store=self.builder.get_object('liststore1')
        store.set_value(treeiter,4,str(int(per))+"%")
        if per<=100:
            return True
        else:
            return False

        
