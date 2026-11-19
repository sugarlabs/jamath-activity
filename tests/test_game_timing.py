"""Exercise the real play loop with SDL's headless video and audio drivers.

Run from a Sugar development environment with pygame installed:
    python -m unittest discover -s tests
"""
import os
import random
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

os.environ.setdefault('SDL_VIDEODRIVER', 'dummy')
os.environ.setdefault('SDL_AUDIODRIVER', 'dummy')

import pygame

import juego


class GameTimingTest(unittest.TestCase):
    def setUp(self):
        self.random_state = random.getstate()
        self.cwd = Path.cwd()
        os.chdir(Path(__file__).resolve().parents[1])
        self.profile = tempfile.TemporaryDirectory()
        Path(self.profile.name, 'data').mkdir()
        self.environment = patch.dict(
            os.environ, {'SUGAR_ACTIVITY_ROOT': self.profile.name})
        self.environment.start()
        pygame.init()
        self.screen = pygame.display.set_mode((1200, 900))
        juego.scale_x = juego.scale_y = 1

    def tearDown(self):
        pygame.quit()
        self.environment.stop()
        self.profile.cleanup()
        os.chdir(self.cwd)
        random.setstate(self.random_state)

    def test_menu_time_is_discarded_on_every_game_entry(self):
        game = juego.Game(None)
        game.screen = self.screen
        for size in (32, 60, 130):
            setattr(game, 'fuente_' + str(size),
                    pygame.font.Font('data/fuente.ttf', size))
        update_sprites = pygame.sprite.Group.update

        for level in ('facil', 'medio', 'dificil'):
            for entry in ('new game', 'replay'):
                with self.subTest(level=level, entry=entry):
                    random.seed(123)
                    game.running = True
                    # Model five seconds in menus, then normal 30 fps frames.
                    game.clock = Mock()
                    game.clock.tick.side_effect = [5000, 33, 33, 33]
                    frames = []

                    def track_update(group, delta, speed, difficulty):
                        update_sprites(group, delta, speed, difficulty)
                        frames.append(delta)
                        self.assertTrue(all(n.rect.y < 900 for n in group))

                    def stop_after_three_frames():
                        if len(frames) == 3:
                            game.running = False

                    group_patch = patch.object(
                        pygame.sprite.Group, 'update', track_update)
                    display_patch = patch.object(
                        pygame.display, 'update', stop_after_three_frames)
                    with group_patch, display_patch:
                        game.play(level)

                    self.assertEqual(frames, [0.033, 0.033, 0.033])
                    calls = game.clock.tick.call_args_list
                    self.assertEqual(calls[0].args, ())
                    for call in calls[1:]:
                        self.assertEqual(call.args, (30,))


if __name__ == '__main__':
    unittest.main()
