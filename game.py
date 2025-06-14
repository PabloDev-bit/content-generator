import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *


class Game:
    def __init__(self, width=800, height=600, init_display=True):
        """Initialize the game.

        Parameters
        ----------
        width, height : int
            Taille de la fenêtre.
        init_display : bool
            Si ``True``, initialise la fenêtre OpenGL. Utile pour lancer le jeu
            normalement mais facultatif pour les tests unitaires.
        """
        pygame.init()
        self.width = width
        self.height = height
        if init_display:
            pygame.display.set_mode((width, height), DOUBLEBUF | OPENGL)
            glEnable(GL_DEPTH_TEST)
            gluPerspective(75, (width / height), 0.1, 50.0)
        self.clock = pygame.time.Clock()
        self.x, self.y, self.z = 0.0, 0.0, -5.0

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[K_w]:
            self.z += 0.1
        if keys[K_s]:
            self.z -= 0.1
        if keys[K_a]:
            self.x += 0.1
        if keys[K_d]:
            self.x -= 0.1

    def draw_scene(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        glTranslatef(self.x, self.y, self.z)

        # Simple cube in front of the player
        glBegin(GL_QUADS)
        glColor3f(1, 0, 0)
        glVertex3f(1, 1, -1)
        glVertex3f(-1, 1, -1)
        glVertex3f(-1, -1, -1)
        glVertex3f(1, -1, -1)
        glEnd()

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
            self.handle_input()
            self.draw_scene()
            pygame.display.flip()
            self.clock.tick(60)
        pygame.quit()


if __name__ == "__main__":
    Game().run()
