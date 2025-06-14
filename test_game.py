import os
import unittest
import pygame
from game import Game


class GameInitTestCase(unittest.TestCase):
    def test_game_initializes(self):
        os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
        # On initialise le jeu sans ouvrir de fenêtre OpenGL
        game = Game(640, 480, init_display=False)
        self.assertIsNotNone(game)
        pygame.quit()


if __name__ == "__main__":
    unittest.main()
