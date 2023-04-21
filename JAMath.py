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
from sugar3.activity.widgets import ActivityToolbarButton, StopButton


class JAMath(Activity):

    def __init__(self, handle):
        Activity.__init__(self, handle)

        self.max_participants = 1

        self.jamath_activity = Game(activity=self)
        self.build_toolbar()
        self._pygamecanvas = sugargame.canvas.PygameCanvas(
            self,
            main=self.jamath_activity.run,
            modules=[pygame.display, pygame.font, pygame.mixer])
        self.set_canvas(self._pygamecanvas)
        self._pygamecanvas.grab_focus()
        # Add a timer to the game
        self.timer_seconds = 60
        self.timer_label = Gtk.Label(label=f'Time Left: {self.timer_seconds}')
        self.timer_label.set_margin_right(10)
        self.toolbar_box.toolbar.pack_end(self.timer_label, False, False, 0)
        self.timer_label.show()

        # Add sound effects to the game
        self.correct_sound = pygame.mixer.Sound("correct.wav")
        self.incorrect_sound = pygame.mixer.Sound("incorrect.wav")

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
    # Update the timer label every second
    def update_timer(self):
        self.timer_seconds -= 1
        if self.timer_seconds == 0:
            self.jamath_activity.running = False
        else:
            self.timer_label.set_label(f'Time Left: {self.timer_seconds}')
            return True

    # Play a sound effect when a number is answered correctly
    def play_correct_sound(self):
        self.correct_sound.play()

    # Play a sound effect when a number is answered incorrectly
    def play_incorrect_sound(self):
        self.incorrect_sound.play()

    # Override the run method to add the timer and sound effects
    def run(self):
        # Start the timer
        GObject.timeout_add_seconds(1, self.update_timer)

        # Set the sound effects on the game object
        self.jamath_activity.play_correct_sound = self.play_correct_sound
        self.jamath_activity.play_incorrect_sound = self.play_incorrect_sound

        # Call the original run method
        super(JAMath, self).run()
