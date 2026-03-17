import pygame
from frontend.ui.water_bar import WaterBar
from frontend.ui.humor_bar import HumorBar
from frontend.sprites.character import Character
from frontend.settings import *

from backend.GlobalManager import GlobalManager
from backend import ChoiceEnum
from backend.Village import Village

from pathlib import Path

current_path = Path.cwd()

from frontend.scenes.good_ending_scene import GoodEnding

class MapScene:
    def __init__(self, manager, intro_choice=None):  # <-- aggiunto intro_choice
        self.manager = manager

        self.smoke_img = pygame.image.load(f"{current_path}/frontend/assets/smoke.png").convert_alpha()
        self.smoke_img = pygame.transform.scale(self.smoke_img, (200, 200))

        img_originale = pygame.image.load(f"{current_path}/frontend/assets/map.png").convert_alpha()
        self.map = pygame.transform.scale(img_originale, (1000, 600))

        self.barA = WaterBar(50, 50)
        self.barB = WaterBar(750, 50)
        self.humor_barA = HumorBar(50, 90)
        self.humor_barB = HumorBar(750, 90)

        self.timer = 0
        self.font = pygame.font.SysFont(None, 30)

        from frontend.ui.button import Button

        self.buttonA = Button("Villaggio A ha tutta l'acqua", 300, 250, 200, 50)
        self.buttonB = Button("Villaggio B ha tutta l'acqua", 550, 250, 200, 50)

        self.btn_collab = Button("Collaborazione", 250, 300, 200, 50)
        self.btn_guerra = Button("Guerra", 550, 300, 200, 50)

        self.village_a = None
        self.village_b = None
        self.char_walker = None

        self.characters = [
            Character(f"{current_path}/frontend/assets/villageA_chars.png", 150, 400, rect=pygame.Rect(0, 0, 150, 150)),
            Character(f"{current_path}/frontend/assets/villageA_chars.png", 220, 400, rect=pygame.Rect(150, 0, 150, 150)),
        ]

        # --- Gestione scelta dall'IntroScene ---
        if intro_choice == 0:
            # Collaborazione: entrambi condividono da subito
            GlobalManager.INSTANCE.choice = ChoiceEnum.SHARED
            self.char_walker = Character(
                f"{current_path}/frontend/assets/villageA_chars.png",
                500, 400, rect=pygame.Rect(0, 0, 150, 150)
            )
            self.fase_gioco = "collaborazione"

        elif intro_choice == 1:
            # Villaggio A ha tutta l'acqua → B soffre, parte da destra
            GlobalManager.INSTANCE.choice = ChoiceEnum.ALL_TO_A
            self.char_walker = Character(
                f"{current_path}/frontend/assets/villageB_chars.png",
                850, 400, rect=pygame.Rect(0, 0, 150, 150)
            )
            self.fase_gioco = "simulazione"

        elif intro_choice == 2:
            # Villaggio B ha tutta l'acqua → A soffre, parte da sinistra
            GlobalManager.INSTANCE.choice = ChoiceEnum.ALL_TO_B
            self.char_walker = Character(
                f"{current_path}/frontend/assets/villageA_chars.png",
                150, 400, rect=pygame.Rect(0, 0, 150, 150)
            )
            self.fase_gioco = "simulazione"

        else:
            # Nessuna scelta dall'intro: mostra la schermata classica
            self.fase_gioco = "scelta_iniziale"

    def update(self, events, state):

        state.humor_a = Village.VILLAGGIO_A.morale
        state.humor_b = Village.VILLAGGIO_B.morale

        if self.fase_gioco == "scelta_iniziale":
            for e in events:
                if self.buttonA.clicked(e):
                    GlobalManager.INSTANCE.choice = ChoiceEnum.ALL_TO_A
                    self.char_walker = Character(
                        f"{current_path}/frontend/assets/villageB_chars.png",
                        850, 400, rect=pygame.Rect(0, 0, 150, 150)
                    )
                    self.fase_gioco = "simulazione"

                if self.buttonB.clicked(e):
                    GlobalManager.INSTANCE.choice = ChoiceEnum.ALL_TO_B
                    self.char_walker = Character(
                        f"{current_path}/frontend/assets/villageA_chars.png",
                        150, 400, rect=pygame.Rect(0, 0, 150, 150)
                    )
                    self.fase_gioco = "simulazione"
            return

        elif self.fase_gioco == "simulazione":
            self.timer += 1
            if self.timer > 10:
                GlobalManager.INSTANCE.time.year_flow(GlobalManager.INSTANCE.choice)
                state.year = GlobalManager.INSTANCE.time.year
                self.timer = 0
                state.water_a = Village.VILLAGGIO_A.riserva_acqua
                state.water_b = Village.VILLAGGIO_B.riserva_acqua
                state.humor_a = Village.VILLAGGIO_A.morale
                state.humor_b = Village.VILLAGGIO_B.morale

            if state.year >= 2040 and not getattr(state, 'dam_built', False):
                state.dam_built = True

            if Village.VILLAGGIO_A.morale < 40 or Village.VILLAGGIO_B.morale < 40:
                self.fase_gioco = "camminata"

        elif self.fase_gioco == "camminata":
            if self.char_walker.x < 500: self.char_walker.x += 2
            elif self.char_walker.x > 500: self.char_walker.x -= 2
            if abs(self.char_walker.x - 500) <= 2:
                self.fase_gioco = "domanda"

        elif self.fase_gioco == "domanda":
            for e in events:
                if self.btn_collab.clicked(e):
                    self.fase_gioco = "collaborazione"
                    GlobalManager.INSTANCE.set_choice(ChoiceEnum.SHARED)

                if self.btn_guerra.clicked(e):
                    if GlobalManager.INSTANCE.choice == ChoiceEnum.ALL_TO_B:
                        self.enemy_char = Character(f"{current_path}/frontend/assets/villageA_chars.png", 150, 400, rect=pygame.Rect(0, 0, 150, 150))
                    else:
                        self.enemy_char = Character(f"{current_path}/frontend/assets/villageB_chars.png", 850, 400, rect=pygame.Rect(0, 0, 150, 150))
                    self.fase_gioco = "conflitto"
                    self.timer = 0

        elif self.fase_gioco == "conflitto":
            self.timer += 1
            if self.char_walker.x < 450: self.char_walker.x += 5
            elif self.char_walker.x > 550: self.char_walker.x -= 5
            if self.enemy_char.x < 450: self.enemy_char.x += 5
            elif self.enemy_char.x > 550: self.enemy_char.x -= 5
            if self.timer > 150:
                GlobalManager.INSTANCE.war()
                GlobalManager.INSTANCE.time.year_flow(GlobalManager.INSTANCE.choice)
                state.year = GlobalManager.INSTANCE.time.year
                self.timer = 0

                #if self.losing_village == "A": state.water_a -= 10
                #if self.losing_village == "B": state.water_b -= 10
                state.water_a = Village.VILLAGGIO_A.riserva_acqua
                state.water_b = Village.VILLAGGIO_B.riserva_acqua
                state.humor_a = Village.VILLAGGIO_A.morale
                state.humor_b = Village.VILLAGGIO_B.morale

                if Village.VILLAGGIO_A.estinto or Village.VILLAGGIO_B.estinto:
                    from frontend.scenes.bad_ending_scene import BadEnding
                    self.manager.change(BadEnding(self.manager))

        elif self.fase_gioco == "collaborazione":
            self.timer += 1
            if self.timer > 10:
                self.timer = 0
                if state.year < 2100:
                    GlobalManager.INSTANCE.time.year_flow(GlobalManager.INSTANCE.choice)
                    state.year = GlobalManager.INSTANCE.time.year
                    state.water_a = Village.VILLAGGIO_A.riserva_acqua
                    state.water_b = Village.VILLAGGIO_B.riserva_acqua
                    state.humor_a = Village.VILLAGGIO_A.morale
                    state.humor_b = Village.VILLAGGIO_B.morale
                else:
                    self.manager.change(GoodEnding(self.manager))

    def draw(self, screen, state):

        self.title_font = pygame.font.SysFont("Arial", 16)

        if self.fase_gioco == "scelta_iniziale":
            screen.fill((30, 30, 40))
            text = self.font.render("Quale villaggio perderà acqua?", True, (255, 255, 255))
            screen.blit(text, (330, 200))
            self.buttonA.draw(screen)
            self.buttonB.draw(screen)
            return

        screen.blit(self.map, (0, 0))

        self.barA.draw(screen, state.water_a)
        screen.blit(self.title_font.render("water", True, (255, 255, 255)), (50, 32))
        self.barB.draw(screen, state.water_b)
        screen.blit(self.title_font.render("water", True, (255, 255, 255)), (750, 32))

        self.humor_barA.draw(screen, state.humor_a)
        screen.blit(self.title_font.render("felicità", True, (255, 255, 255)), (50, 70))
        self.humor_barB.draw(screen, state.humor_b)
        screen.blit(self.title_font.render("felicità", True, (255, 255, 255)), (750, 70))

        year_text = self.font.render(f"Year: {state.year}", True, (255, 255, 255))
        screen.blit(year_text, (450, 20))

        numero_persone_a = Village.VILLAGGIO_A.num_persone
        numero_persone_b = Village.VILLAGGIO_B.num_persone
        screen.blit(self.font.render(f"Popolazione: {numero_persone_a}", True, (150, 75, 0)), (50, 110))
        screen.blit(self.font.render(f"Popolazione: {numero_persone_b}", True, (150, 75, 0)), (750, 110))

        for c in self.characters:
            c.draw(screen)

        if self.fase_gioco in ["camminata", "domanda", "collaborazione"]:
            self.char_walker.draw(screen)

        if self.fase_gioco == "domanda":
            q_text = self.font.render("L'acqua sta finendo! Cosa volete fare?", True, (255, 255, 255))
            screen.blit(q_text, (320, 200))
            self.btn_collab.draw(screen)
            self.btn_guerra.draw(screen)

        if self.fase_gioco == "conflitto":
            self.enemy_char.draw(screen)
            if abs(self.char_walker.x - self.enemy_char.x) < 100:
                import random
                offset_x = random.randint(-5, 5)
                offset_y = random.randint(-5, 5)
                screen.blit(self.smoke_img, (400 + offset_x, 350 + offset_y))
                screen.blit(self.font.render("SCONTRO!", True, (255, 0, 0)), (450, 300))