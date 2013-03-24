# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
### BEGIN LICENSE
# This file is in the public domain
### END LICENSE

import gettext
from gettext import gettext as _
gettext.textdomain('mydownloader')

import logging
logger = logging.getLogger('mydownloader')

from mydownloader_lib.AboutDialog import AboutDialog

# See mydownloader_lib.AboutDialog.py for more details about how this class works.
class AboutMydownloaderDialog(AboutDialog):
    __gtype_name__ = "AboutMydownloaderDialog"
    
    def finish_initializing(self, builder): # pylint: disable=E1002
        """Set up the about dialog"""
        super(AboutMydownloaderDialog, self).finish_initializing(builder)

        # Code for other initialization actions should be added here.

