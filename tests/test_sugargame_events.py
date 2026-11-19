"""Regression checks for the vendored sugargame keyboard and resize bridge."""
import unittest
from types import SimpleNamespace

import gi
import pygame

gi.require_version('Gtk', '3.0')
from gi.repository import Gdk, Gtk  # noqa: E402

from sugargame.event import Translator  # noqa: E402


class SugarGameEventsTest(unittest.TestCase):
    def setUp(self):
        pygame.display.init()
        pygame.display.set_mode((640, 480))
        self.window = Gtk.Window()
        self.canvas = Gtk.EventBox()
        self.window.add(self.canvas)
        self.translator = Translator(self.window, self.canvas)
        pygame.event.clear()

    def tearDown(self):
        self.window.destroy()
        pygame.quit()

    def key(self, name, pressed):
        event = SimpleNamespace(keyval=Gdk.keyval_from_name(name))
        callback = (self.translator._keydown_cb if pressed
                    else self.translator._keyup_cb)
        self.assertTrue(callback(self.canvas, event))
        events = pygame.event.get((pygame.KEYDOWN, pygame.KEYUP))
        self.assertEqual(len(events), 1)
        return events[0]

    def test_activity_keys_round_trip(self):
        for name, key, text in (
                ('Escape', pygame.K_ESCAPE, ''),
                ('0', pygame.K_0, '0'),
                ('9', pygame.K_9, '9'),
                ('minus', pygame.K_MINUS, '-'),
                ('BackSpace', pygame.K_BACKSPACE, '\b'),
                ('Return', pygame.K_RETURN, '\r')):
            with self.subTest(key=name):
                down = self.key(name, True)
                self.assertEqual((down.type, down.key), (pygame.KEYDOWN, key))
                if name != 'Escape':
                    self.assertEqual(down.unicode, text)
                up = self.key(name, False)
                self.assertEqual((up.type, up.key), (pygame.KEYUP, key))
                self.assertEqual(up.mod, 0)

    def test_large_pygame2_modifier_keycodes(self):
        self.assertGreater(pygame.K_LALT, 322)
        for name, key, modifier in (
                ('Alt_L', pygame.K_LALT, pygame.KMOD_LALT),
                ('Alt_R', pygame.K_RALT, pygame.KMOD_RALT),
                ('Control_L', pygame.K_LCTRL, pygame.KMOD_LCTRL),
                ('Control_R', pygame.K_RCTRL, pygame.KMOD_RCTRL),
                ('Shift_L', pygame.K_LSHIFT, pygame.KMOD_LSHIFT),
                ('Shift_R', pygame.K_RSHIFT, pygame.KMOD_RSHIFT)):
            with self.subTest(key=name):
                self.assertEqual(self.key(name, True).key, key)
                self.assertEqual(self.key('1', True).mod & modifier, modifier)
                self.key('1', False)
                self.key(name, False)
                self.assertEqual(self.key('1', True).mod & modifier, 0)
                self.key('1', False)

    def test_canvas_allocation_posts_resize(self):
        allocation = Gdk.Rectangle()
        allocation.width, allocation.height = 800, 600
        self.canvas.show()
        self.canvas.emit('size-allocate', allocation)
        events = pygame.event.get(pygame.VIDEORESIZE)
        self.assertEqual(len(events), 1)
        self.assertEqual(events[0].size, (800, 600))
        self.assertEqual((events[0].width, events[0].height), (800, 600))


if __name__ == '__main__':
    unittest.main()
