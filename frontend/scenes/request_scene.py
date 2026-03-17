import pygame
from frontend.ui.button import Button
from frontend.scenes.good_ending_scene import GoodEnding
from frontend.scenes.war_scene import WarScene

class RequestScene:

    def __init__(self,manager):

        self.manager = manager

        self.share = Button("Condividere acqua",350,300,200,50)
        self.refuse = Button("Rifiutare",350,380,200,50)

        self.font = pygame.font.SysFont(None,40)

    def update(self,events,state):

        for e in events:

            if self.share.clicked(e):

                state.water_b += 20
                state.water_a -= 20

                self.manager.change(GoodEnding(self.manager))

            if self.refuse.clicked(e):

                self.manager.change(WarScene(self.manager))

    def draw(self,screen,state):

        text = self.font.render(
        "Abbiamo bisogno di acqua. Potete condividerla?",True,(255,255,255))

        screen.blit(text,(200,200))

        self.share.draw(screen)
        self.refuse.draw(screen)