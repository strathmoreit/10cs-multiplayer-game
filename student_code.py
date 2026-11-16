# student_code.py
import pygame
from modules.entities import BasePlayer

class Player(BasePlayer):
    # students write the code for their player here

    def update(self):
        # this is the code that runs every time the screen is updated
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.x = self.x - 5