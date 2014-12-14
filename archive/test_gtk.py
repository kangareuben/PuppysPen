#!/usr/bin/python

# what's the difference between these two?
#from gi.repository import Gtk
#from gtk import gdk

import os
import gobject
import gtk

import Constants

class Window(gtk.Window):

    def __init__(self):
        gtk.Window.__init__(self)
        self.set_resizable(False)
        self.set_size_request(Constants.WIDTH, Constants.HEIGHT)
        self.main_bbox = None
        self.game_bbox = None

        #self.main_screen()
        self.game_screen()

    def main_screen(self):
        if (self.game_bbox):
            self.remove(self.game_bbox)
            self.game_bbox = None

        self.main_bbox = gtk.HButtonBox()
        self.main_bbox.connect('expose-event', self.draw_background)
        self.start_btn = gtk.Button("Start")
        self.start_btn.connect('clicked', self.game_clicked)
        self.main_bbox.pack_start(self.start_btn, True, False, 10)
        self.add(self.main_bbox)
        print(self.main_bbox)

    def game_screen(self):
        if (self.main_bbox):
            self.remove(self.main_bbox)
            self.main_bbox = None

        self.game_bbox = gtk.HButtonBox()
        self.back_btn = gtk.Button("Menu")
        self.back_btn.connect('clicked', self.menu_clicked)
        self.game_bbox.pack_start(self.back_btn, True, False, 10)
        self.add(self.game_bbox)
        print(self.game_bbox)

    def game_clicked(self, event):
        print("Start clicked")
        self.game_screen()

    def menu_clicked(self, event):
        print("Menu clicked")
        self.main_screen()

    def draw_background(self, widget, event):
        path = "./test_background.jpg"
        pixbuf = gtk.gdk.pixbuf_new_from_file(path)
        widget.window.draw_pixbuf(widget.style.bg_gc[gtk.STATE_NORMAL], pixbuf, 0, 0, 0, 0)

#class MainScreen(object):

    #def __init__(self, window):
        #self.w = window
        #self.w.hbbox = gtk.HButtonBox()
        #self.w.add(window.hbbox)
        #self.w.hbbox.connect('expose-event', self.w.draw_background)
        #self.w.start_btn = gtk.Button("Start")
        #self.w.start_btn.connect('clicked', self.start_clicked)
        #self.w.hbbox.pack_start(self.w.start_btn, True, False, 10)

    #def start_clicked(self, event):
        #print("Start clicked")
        #GameScreen(self.w)

#class GameScreen(object):

    #def __init__(self, window):
        #self.w = window
        #self.w.hbbox = gtk.HButtonBox()
        #self.w.add(self.w.hbbox)
        #self.w.start_btn = gtk.Button("Menu")
        #self.w.start_btn.connect('clicked', self.menu_clicked)
        #self.w.hbbox.pack_start(self.w.start_btn, True, False, 10)

    #def menu_clicked(self, event):
        #print("Menu clicked")
        #MainScreen(self.w)

win = Window()
win.connect("delete-event", gtk.main_quit)
win.show_all()
gtk.main()
