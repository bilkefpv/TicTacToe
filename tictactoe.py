import pygame
import time

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)


class TICTACTOE:
    def __init__(self):
        self.scoreP1 = 0
        self.scoreP2 = 0
        self.rects = set()
        self.game_active_squares = {}
        pygame.init()
        size = width, height = 640, 480
        self.screen = pygame.display.set_mode(size)
        self.screen.fill(black)
        self.P1, self.P2 = [], []
        self.player_one, self.player_two = True, False
        self.display_restart_btn()
        self.new_game()
        self.play()

    def new_game(self):
        pygame.draw.rect(self.screen, black, (120, 40, 400, 400))
        startx, starty = 120, 40
        # t_pos = background rect
        t_pos = []
        for r in range(3):
            for c in range(3):
                t_pos.append((startx, starty))
                starty += 133
            startx += 133
            starty = 40
        for x, y in t_pos:
            self.rects.add((x, y, x + 133, y + 133))
            pygame.draw.rect(self.screen, white, (x, y, 133, 133), 3)

        self.P1, self.P2 = [], []
        self.player_one, self.player_two = True, False
        self.game_active_squares = {(rect[0], rect[1]): False for rect in self.rects}
        self.display_player()
        pygame.display.update()

    def play(self):
        game = True
        self.display_player()
        while game:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    game = False
                    break
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        pos = pygame.mouse.get_pos()
                        clicked_restart_btn = self.restart_btn[0] < pos[0] < self.restart_btn[0] + 75 and \
                                              self.restart_btn[1] < pos[1] < self.restart_btn[1] + 75
                        if clicked_restart_btn:
                            self.new_game()
                        clicked_on_empty_square = (p := self.is_inside(pos[0], pos[1])) and not \
                        self.game_active_squares[p]
                        if clicked_on_empty_square:
                            if self.player_two:
                                self.P2.append(p)
                                pygame.draw.circle(self.screen, white, (p[0] + 66.5, p[1] + 66.5), 54, 3)
                            else:
                                self.P1.append(p)
                                pygame.draw.line(self.screen, white, (p[0], p[1] + 133), (p[0] + 133, p[1]), 3)
                                pygame.draw.line(self.screen, white, (p[0], p[1]), (p[0] + 133, p[1] + 133), 3)
                            self.game_active_squares[p] = 1
                            self.player_one, self.player_two = not self.player_one, not self.player_two
                            self.display_player()
                        if len(self.P1) > 2 or len(self.P2) > 2:
                            self.check_winner()
                        if len(self.P1) + len(self.P2) == 9:
                            self.end_match(tie=True)
            else:
                pygame.display.update()

    def filled_diag(self, diag, player):
        for c in diag:
            if c not in player:
                break
        else:
            return True
        return False

    def check_winner(self):
        diag_1 = (120, 40), (253, 173), (386, 306)
        diag_2 = (386, 40), (253, 173), (120, 306)

        if self.filled_diag(diag_1, self.P1) or self.filled_diag(diag_2, self.P1):
            self.end_match(winner="Player 1")
            return

        if self.filled_diag(diag_1, self.P2) or self.filled_diag(diag_2, self.P2):
            self.end_match(winner="Player 2")
            return

        y_s = [coord[1] for coord in self.P1]
        x_s = [coord[0] for coord in self.P1]

        if max([y_s.count(coord[1]) for coord in self.P1]) >= 3 or max([x_s.count(coord[0]) for coord in self.P1]) >= 3:
            self.end_match(winner="Player 1")
            return

        y_s = [coord[1] for coord in self.P2]
        x_s = [coord[0] for coord in self.P2]
        if max([y_s.count(coord[1]) for coord in self.P2]) >= 3 or max([x_s.count(coord[0]) for coord in self.P2]) >= 3:
            self.end_match(winner="Player 2")
            return

    def display_text(self, text_inp, font, center, color=white):
        font = pygame.font.Font(None, font)
        text = font.render(text_inp, True, color)
        text_rect = text.get_rect(center=center)
        if text_inp == "Restart":
            self.restart_btn = text_rect
        pygame.draw.rect(self.screen, black, text_rect)
        self.screen.blit(text, text_rect)
        pygame.display.update()

    def display_restart_btn(self):
        self.display_text("Restart", 25, (50, 50), color=red)

    def display_winner(self, winner):
        if winner == "Player 1":
            self.scoreP1 += 1
        else:
            self.scoreP2 += 1
        self.display_text(f"Player 1: {str(self.scoreP1)}", 25, (120, 460), color=blue)
        self.display_text(f"Player 2: {str(self.scoreP2)}", 25, (520, 460), color=green)
        self.display_text(f"Victory {winner}", 50, (640 / 2, 480 / 2), color=white)

    def display_player(self):
        player = "Player 1" if self.player_one else "Player 2"
        color = blue if self.player_one else green
        self.display_text(player, 25, (640 / 2, 25), color=color)

    def display_tie(self):
        self.display_text("TIE", 50, (640 / 2, 480 / 2), color=red)

    def is_inside(self, x, y):
        for x1, y1, x1max, y1max in self.rects:
            if x1 < x < x1max and y1 < y < y1max:
                return x1, y1
        return False

    def end_match(self, tie=False, winner=False):
        self.display_tie() if tie else self.display_winner(winner)
        time.sleep(2)
        self.new_game()


if __name__ == "__main__":
    TICTACTOE()

def start():
    TICTACTOE()