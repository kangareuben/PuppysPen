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
        #Gtk.Window.__init__(self, title="Puppy's Pen")
        #self.set_resizable(False)
        #self.set_size_request(Constants.WIDTH, Constants.HEIGHT)

        #self.menu = Gtk.Fixed()

        #self.area = Gtk.DrawingArea()
        #self.area.set_app_paintable(True)
        #self.area.set_size_request(Constants.WIDTH, Constants.HEIGHT)
        #self.add(self.area)
        #self.area.realize()

        #self.hbbox = Gtk.HButtonBox()
        #self.add(self.hbbox)
        #self.hbbox.connect('draw', self.draw_background)

        #self.button = Gtk.Button(label="Start")
        #self.button.connect("clicked", self.start_clicked)
        #self.menu.put(self.button, Constants.WIDTH/3, Constants.HEIGHT/2)
        #self.add(self.menu)

        gtk.Window.__init__(self)
        self.set_resizable(False)
        self.set_size_request(Constants.WIDTH, Constants.HEIGHT)

        self.hbbox = gtk.HButtonBox()
        self.add(self.hbbox)
        self.hbbox.connect('expose-event', self.draw_background)
        self.start_btn = gtk.Button("Start")
        self.hbbox.pack_start(self.start_btn, True, False, 10)

    def start_clicked(self, button):
        print("Start clicked")

    def draw_background(self, widget, event):
        path = "./test_background.jpg"
        pixbuf = gtk.gdk.pixbuf_new_from_file(path)
        widget.window.draw_pixbuf(widget.style.bg_gc[gtk.STATE_NORMAL], pixbuf, 0, 0, 0, 0)

class MainScreen(object):
    pass

class GameScreen(object):
    pass

win = Window()
win.connect("delete-event", gtk.main_quit)
win.show_all()
gtk.main()
