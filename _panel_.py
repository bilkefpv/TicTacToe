from _imports_ import *


class Player_Panel:
    def __init__(self, screen, player, size):
        self.score = 0
        self.w, self.h = size
        self.screen = screen
        self.factor_speed = 4
        self.moving = 0
        self.width = 15
        self.height = self.w // 9.5 + 4

        if player == 1:
            self.position = (20 + 30, self.h // 2, self.width, self.height)
        else:
            self.position = (self.w - 30, self.h // 2, self.width, self.height)  # left,top,width,height
        self.panel(self.position[0], self.position[1], self.width, self.height)
        self.update()
        self.freeze = 0

    def point(self):
        self.score += 1

    def panel(self, left, top, width, height):
        self.rect = pygame.Rect(left, top, width, height)
        top_height = height // 5
        self.top_rect = pygame.Rect(left, top, width, top_height)
        center_height = height - (top_height * 2)
        self.center_rect = pygame.Rect(left, top + top_height, width, center_height)

        self.bot_rect = pygame.Rect(left, top + top_height + center_height, width, top_height)

    def update(self):
        pygame.draw.rect(self.screen, white, self.rect)

    def start(self):
        self.freeze = 0

    def stop(self):
        self.freeze = 1
        self.moving = 0

    def move(self):
        if self.moving == 1:
            move_by_size = -self.factor_speed
        elif self.moving == -1:
            move_by_size = self.factor_speed
        else:
            return

        if self.position[1] + move_by_size < 56:
            move_by_size = 0
        if self.position[1] + move_by_size > self.h - 26:
            move_by_size = 0

        self.position = (self.position[0], self.position[1] + move_by_size, self.width, self.height)
        self.panel(self.position[0], self.position[1], self.width, self.height)

        self.update()

    def move_to_target(self, target):

        if target[1] < self.position[1]:
            self.moving = 1
        else:
            self.moving = -1
        if not self.freeze:
            self.move()
