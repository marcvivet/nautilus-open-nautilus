#!/usr/bin/python

from __future__ import ( division, absolute_import, print_function, unicode_literals )
import os
import pwd
import urllib
import subprocess
from gi.repository import Nautilus, GObject

class OpenNautilusExtension(GObject.GObject, Nautilus.MenuProvider):
    def __init__(self):
        pass
        
    def _open_nautilus(self, file):
    
        if 'nautilus-desktop:///' in file.get_uri():
            filename = '/home/' + pwd.getpwuid( os.getuid() ).pw_name + '/Desktop'
        else:
            uri_scheme = file.get_uri_scheme()

            if uri_scheme == 'file':
                filename = urllib.unquote(file.get_uri()[len(uri_scheme) + 3:])
            else:
                if uri_scheme == 'sftp':
                    uri = urllib.unquote(file.get_uri()[len(uri_scheme) + 3:])
                    aux_vals = uri.split('/')
                    
                    host = aux_vals[0]
                    user = None
                    
                    path = ''
                    
                    for val in aux_vals[1:]:
                        path += '/' + val
                    
                    if '@' in host:
                        aux_host = host.split('@')
                        user = aux_host[0]
                        host = aux_host[1]
                    
                    filename = '/run/user/' + str(os.getuid()) + '/gvfs/sftp:host=' + host
                    if user:
                        filename += ',user=' + user
                        
                    filename += path
                else:
                    filename = '/home/' + pwd.getpwuid( os.getuid() ).pw_name

        os.system('nautilus -w "{}" &'.format(filename))
        
    def menu_activate_cb(self, menu, file):
        self._open_nautilus(file)
        
    def menu_background_activate_cb(self, menu, file): 
        self._open_nautilus(file)
       
    def get_file_items(self, window, files):
        if len(files) != 1:
            return
        
        file = files[0]
        
        item = Nautilus.MenuItem(name='NautilusPython::open_nautilus',
                                 label='Open Nautilus' ,
                                 tip='Open Nautilus In %s' % file.get_name())
        item.connect('activate', self.menu_activate_cb, file)
        return item,

    def get_background_items(self, window, file):
        item = Nautilus.MenuItem(name='NautilusPython::open_nautilus',
                                 label='Open Nautilus',
                                 tip='Open Nautilus In This Directory')
        item.connect('activate', self.menu_background_activate_cb, file)
        return item,

