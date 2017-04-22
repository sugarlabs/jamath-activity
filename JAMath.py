#!/usr/bin/env python
# -*- coding: utf-8 -*-

import gtk
from sugar.activity import activity
import sugargame.canvas

from juego import Game

from sugar.graphics.toolbarbox import ToolbarBox
from sugar.activity.widgets import ActivityToolbarButton
from sugar.activity.widgets import StopButton
from sugar.graphics.toolbutton import ToolButton

class JAMath(activity.Activity):

    def __init__(self, handle):
        activity.Activity.__init__(self, handle)

        self.max_participants = 1
        
        self.jamath_activity = Game()
        self.build_toolbar()
        self._pygamecanvas = sugargame.canvas.PygameCanvas(self)
        self.set_canvas(self._pygamecanvas)
        self._pygamecanvas.run_pygame(self.jamath_activity.run)

    def build_toolbar(self):

        toolbox = ToolbarBox()
        activity_button = ActivityToolbarButton(self)
        toolbox.toolbar.insert(activity_button, -1)
        activity_button.show()

        barra = toolbox.toolbar

        separator2 = gtk.SeparatorToolItem()
        separator2.props.draw = False
        separator2.set_expand(True)
        barra.insert(separator2, -1)

        stop_button = StopButton(self)
        stop_button.props.accelerator = '<Ctrl>q'
        barra.insert(stop_button, -1)
        stop_button.show()

        self.set_toolbar_box(toolbox)

        toolbox.show_all()




