import pygame
from frontend.scenes.map_scene import MapScene

class Button:

    def __init__(self, x, y, width, height, text, font):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.hovered = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return True
        return False

    def draw(self, screen):
        color = (70, 130, 180) if self.hovered else (40, 80, 120)
        border_color = (100, 180, 255) if self.hovered else (60, 120, 180)
        pygame.draw.rect(screen, color, self.rect, border_radius=8)
        pygame.draw.rect(screen, border_color, self.rect, width=2, border_radius=8)
        label = self.font.render(self.text, True, (255, 255, 255))
        label_rect = label.get_rect(center=self.rect.center)
        screen.blit(label, label_rect)


class IntroScene:

    def __init__(self, manager):
        self.manager = manager
        self.font = pygame.font.SysFont(None, 50)
        self.btn_font = pygame.font.SysFont(None, 24)

        self.cursor_default = pygame.SYSTEM_CURSOR_ARROW
        self.cursor_hand    = pygame.SYSTEM_CURSOR_HAND
        self._current_cursor = self.cursor_default
        pygame.mouse.set_cursor(self.cursor_default)

        btn_width = 280
        btn_height = 50
        btn_y = 370
        spacing = 30
        total_width = btn_width * 3 + spacing * 2
        start_x = (1000 - total_width) // 2

        self.buttons = [
            Button(start_x,                              btn_y, btn_width, btn_height, "Collaborazione",               self.btn_font),
            Button(start_x + btn_width + spacing,        btn_y, btn_width, btn_height, "Villaggio A ha tutta l'acqua", self.btn_font),
            Button(start_x + (btn_width + spacing) * 2,  btn_y, btn_width, btn_height, "Villaggio B ha tutta l'acqua", self.btn_font),
        ]

    def update(self, events, state):
        mouse_pos = pygame.mouse.get_pos()
        any_hovered = any(btn.rect.collidepoint(mouse_pos) for btn in self.buttons)
        desired = self.cursor_hand if any_hovered else self.cursor_default
        if desired != self._current_cursor:
            self._current_cursor = desired
            pygame.mouse.set_cursor(desired)

        for e in events:
            for i, btn in enumerate(self.buttons):
                if btn.handle_event(e):
                    state.intro_choice = i
                    pygame.mouse.set_cursor(self.cursor_default)
                    self.manager.change(MapScene(self.manager, intro_choice=i))

    def draw(self, screen, state):
        text = self.font.render(
            "Raggiungere il 2100 senza guerra per l'acqua", True, (255, 255, 255))
        screen.blit(text, (120, 250))
        for btn in self.buttons:
            btn.draw(screen)