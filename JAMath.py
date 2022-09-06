#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import pygame
import sugargame.canvas

from juego import Game

from sugar3.activity.activity import Activity
from sugar3.graphics.toolbarbox import ToolbarBox
from sugar3.activity.widgets import ActivityToolbarButton
from sugar3.activity.widgets import StopButton
from sugar3.graphics.toolbutton import ToolButton

class JAMath(Activity):

    def __init__(self, handle):
        Activity.__init__(self, handle)

        self.max_participants = 1

        self.jamath_activity = Game(activity=self)
        self.build_toolbar()
        self._pygamecanvas = sugargame.canvas.PygameCanvas(self,
            main=self.jamath_activity.run,
            modules=[pygame.display, pygame.font, pygame.mixer])
        self.set_canvas(self._pygamecanvas)
        self._pygamecanvas.grab_focus()

    def build_toolbar(self):

        toolbox = ToolbarBox()
        self.set_toolbar_box(toolbox)
        toolbox.show()

        activity_button = ActivityToolbarButton(self)
        toolbox.toolbar.insert(activity_button, -1)
        activity_button.show()

        barra = toolbox.toolbar

        separator2 = Gtk.SeparatorToolItem()
        separator2.props.draw = False
        separator2.set_expand(True)
        barra.insert(separator2, -1)
        separator2.show()

        stop_button = StopButton(self)
        barra.insert(stop_button, -1)
        stop_button.show()
        stop_button.connect('clicked', self._stop_cb)

    def _stop_cb(self, button):
        self.jamath_activity.running = False





