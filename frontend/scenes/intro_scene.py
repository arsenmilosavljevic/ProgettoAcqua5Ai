import pygame
from frontend.scenes.map_scene import MapScene

class IntroScene:

    def __init__(self,manager):

        self.manager = manager
        self.font = pygame.font.SysFont(None,50)

    def update(self,events,state):

        for e in events:

            if e.type == pygame.MOUSEBUTTONDOWN:

                self.manager.change(MapScene(self.manager))

    def draw(self,screen,state):

        text = self.font.render(
        "Raggiungere il 2100 senza guerra per l'acqua",True,(255,255,255))

        screen.blit(text,(120,250))