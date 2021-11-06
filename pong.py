from imports import *
from text import Text
from wheel import Wheel
from ball import Ball
from panel import Player_Panel


def player_move(player):
    if not player.freeze and player.moving != 0:
        player.move()


def player_stop_or_other_direction(player, oppositekey, up):
    player.stop()
    keys = pygame.key.get_pressed()
    if keys[oppositekey]:
        player.start()
        if up:
            player.moving = 1
        else:
            player.moving = -1
        player_move(player)


class Pong:
    def __init__(self):
        self.p1_key_up = pygame.K_e
        self.p1_key_down = pygame.K_d
        self.p2_key_up = pygame.K_o
        self.p2_key_down = pygame.K_l
        self.FPS = 120
        self.clock = pygame.time.Clock()
        self.size = self.width, self.height = 700, 550
        pygame.init()
        self.screen = pygame.display.set_mode(self.size)
        self.start_screen()

    def start_screen(self):
        size = self.width - 40, self.height - 100
        WHEE = Wheel(random=True)
        ball = Ball(size, self.screen, WHEE)

        BTN_ONEPLAYER = Text(self.screen, blue, "One player", self.width // 2 - 100, self.height // 2 - 100)
        BTN_TWOPLAYERS = Text(self.screen, blue, "Two players", self.width // 2 - 100, self.height // 2 - 100 + 80)
        BTN_CHANGE_INPUT = Text(self.screen, blue, "Setup input", self.width // 2 - 100, self.height // 2 - 100 + 160)
        buttons = [BTN_ONEPLAYER,BTN_TWOPLAYERS,BTN_CHANGE_INPUT]
        choose = 1
        choose_text_wheel = Wheel()
        choose_text_wheel.list_indexes(buttons)
        choose_text_wheel.next_state()
        while choose:
            self.screen.fill(black)

            buttons[choose_text_wheel.current].update_color(red)
            for i,btn in enumerate(buttons):
                if i == choose_text_wheel.current:
                    continue
                btn.update_color(blue)
            BTN_ONEPLAYER.update()
            BTN_TWOPLAYERS.update()
            BTN_CHANGE_INPUT.update()
            pygame.display.update()
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    choose = 0
                    break
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        choose_text_wheel.next_state()
                    if event.key == pygame.K_RETURN:
                        if buttons[choose_text_wheel.current] == BTN_ONEPLAYER:
                            self.oneplayer = True
                            WHEE.computer_player()
                            self.play(ball)
                        elif buttons[choose_text_wheel.current] == BTN_TWOPLAYERS:
                            self.oneplayer = False
                            self.play(ball)
                        elif buttons[choose_text_wheel.current] == BTN_CHANGE_INPUT:
                            if (p := self.get_key(1, "up")) != -1:
                                self.p1_key_up = p
                            else:
                                break
                            if (p := self.get_key(1, "down")) != -1:
                                self.p1_key_down = p
                            else:
                                break
                            if (p := self.get_key(2, "up")) != -1:
                                self.p2_key_up = p
                            else:
                                break
                            if (p := self.get_key(2, "down")) != -1:
                                self.p2_key_down = p
                            else:
                                break

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()

                    if BTN_ONEPLAYER.check_click(mouse_pos):
                        self.oneplayer = True
                        WHEE.computer_player()
                        self.play(ball)

                    elif BTN_TWOPLAYERS.check_click(mouse_pos):
                        self.oneplayer = False
                        self.play(ball)

                    elif BTN_CHANGE_INPUT.check_click(mouse_pos):
                        if (p := self.get_key(1, "up")) != -1:
                            self.p1_key_up = p
                        else:
                            break
                        if (p := self.get_key(1, "down")) != -1:
                            self.p1_key_down = p
                        else:
                            break
                        if (p := self.get_key(2, "up")) != -1:
                            self.p2_key_up = p
                        else:
                            break
                        if (p := self.get_key(2, "down")) != -1:
                            self.p2_key_down = p
                        else:
                            break

    def get_key(self, player, movement):
        self.screen.fill(black)
        up_key_p1 = Text(self.screen, white,
                         "Press key to setup Player {} movement {}".format(player, movement.upper()), 20, 20,fontsize=23)
        up_key_p1.update()
        pygame.display.update()
        setup = 1
        while setup:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return -1
                if event.type == pygame.KEYDOWN:
                    return event.key

    def draw_line(self, pos1, pos2, width, parts, vertical=False):
        x = pos1[0]
        y = pos1[1]
        border = pos2

        if vertical:
            distance_x = 0
            distance_y = abs(pos2[1] - pos1[1]) // parts
            use = y
            border = border[1]
        else:
            distance_x = abs(pos2[0] - pos1[0]) // parts
            distance_y = 0
            use = x
            border = border[0]

        while border >= use + distance_y + distance_x:
            pos1 = (pos1[0], pos1[1])
            pygame.draw.line(self.screen, white, pos1, (pos1[0] + distance_x, pos1[1] + distance_y), width)
            pos1 = (pos1[0] + (distance_x * 2), pos1[1] + (distance_y * 2))
            use = pos1[0] if not vertical else pos1[1]
        if vertical:
            distance_y = border - pos1[1]
        else:
            distance_x = border - pos1[0]
        pygame.draw.line(self.screen, white, pos1, (pos1[0] + distance_x, pos1[1] + distance_y), width)

    def draw_game_border(self):
        game_rect = pygame.Rect(20, 50, self.width - 40, self.height - 100)

        self.draw_line(game_rect.topleft, game_rect.topright, 3, 60)
        self.draw_line(game_rect.bottomleft, game_rect.bottomright, 3, 60)
        self.draw_line(game_rect.topleft, game_rect.bottomleft, 3, 50, True)
        self.draw_line(game_rect.topright, game_rect.bottomright, 3, 60, True)
        middle_x = game_rect.topleft[0] + ((game_rect.topright[0] - game_rect.topleft[0]) // 2)
        middle_y = game_rect.topleft[1]

        middle_x1 = middle_x
        middle_y1 = middle_y + game_rect.size[1]
        self.draw_line((middle_x, middle_y), (middle_x1, middle_y1), 6, 20, True)

    def play(self, ball, player1=0, player2=0):
        game = 1
        game_rect = pygame.Rect(20, 50, self.width - 40, self.height - 100)

        player1 = Player_Panel(screen=self.screen, player=1, size=game_rect.size) if not player1 else player1
        player2 = Player_Panel(screen=self.screen, player=2, size=game_rect.size) if not player2 else player2

        target = pygame.Rect(0, 0, 0, 0)
        while game:
            self.screen.fill(black)
            text = "MUTE" if ball.audio else "UNMUTE"
            MUTE_AUDIO = Text(self.screen, white, text, 10, 10)
            self.draw_game_border()
            # is ball behind panel of player 2 or 1
            if (b := ball.update()) == 1:
                player2.point()
                ball.restore()
                self.play(ball, player1, player2)
                return
            elif b == 2:
                player1.point()
                ball.restore()
                self.play(ball, player1, player2)
                return
            # draw score text
            TEXT_SCORE_PLAYER1 = Text(self.screen, white, str(player1.score), (self.width // 6)*2, 20)
            TEXT_SCORE_PLAYER2 = Text(self.screen, white, str(player2.score), (self.width // 6) * 4, 20)
            MUTE_AUDIO.update()
            TEXT_SCORE_PLAYER1.update()
            TEXT_SCORE_PLAYER2.update()

            # draw player panels
            player1.update()
            player2.update()

            # computer player logic
            if self.oneplayer and player1.rect.colliderect(ball.rect) or target.colliderect(
                    pygame.Rect(player1.rect[0], player1.rect[1] + 20, player1.rect[2], 30)):
                player1.stop()
                # stops moving if computer bounces the ball or moves to the target position

            player_move(player2)
            player_move(player1)

            bounce_back = [a for a in np.arange(4,5,0.15)]
            plus = [a for a in np.arange(0.75,1.25,0.05)]
            vel_back = [(x:=choice(bounce_back)),x+choice(plus)]
            if ball.rect.colliderect(player2.top_rect):
                ball.bounce(vel=[vel_back, [1, -1]])
            if ball.rect.colliderect(player2.bot_rect):
                ball.bounce(vel=[vel_back, [1, 1]])
            if ball.rect.colliderect(player2.center_rect):
                ball.bounce(vel=[[6, choice([a for a in np.arange(0.3, 2.5, 0.12)])], [1, 1]])
            if ball.rect.colliderect(player1.center_rect):
                ball.bounce(vel=[[6, choice([a for a in np.arange(0.3, 2.5, 0.12)])], [-1, 1]])
            if ball.rect.colliderect(player1.top_rect):
                ball.bounce(vel=[vel_back, [-1, -1]])
            if ball.rect.colliderect(player1.bot_rect):
                ball.bounce(vel=[vel_back, [-1, 1]])

            # if computer is playing and is computer turn
            if self.oneplayer and ball.rect.colliderect(player2.rect):
                # calculate the ball trajectory
                target = ball.trajectory()

                player1.start()
                # computer player move up or down
                if target[1] < player1.position[1]:
                    player1.moving = 1
                else:
                    player1.moving = -1

            # UPDATE DISPLAY
            pygame.display.update()

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    game = 0
                    break
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()

                    if MUTE_AUDIO.check_click(mouse_pos):
                        ball.mute()
                if event.type == pygame.KEYDOWN:
                    # p1 move up
                    if not self.oneplayer and event.key == self.p1_key_up and player1.moving == 0:
                        player1.start()
                        player1.moving = 1
                    # p1 move down
                    if not self.oneplayer and event.key == self.p1_key_down and player1.moving == 0:
                        player1.start()
                        player1.moving = -1
                    # p2 move up
                    if event.key == self.p2_key_up and player2.moving == 0:
                        player2.start()
                        player2.moving = 1
                    # p2 move down
                    if event.key == self.p2_key_down and player2.moving == 0:
                        player2.start()
                        player2.moving = -1
                if event.type == pygame.KEYUP:
                    # p1 stop move up
                    if not self.oneplayer and event.key == self.p1_key_up and player1.moving == 1:
                        player_stop_or_other_direction(player1, self.p1_key_down, 0)
                    # p1 stop move down
                    if not self.oneplayer and event.key == self.p1_key_down and player1.moving == -1:
                        player_stop_or_other_direction(player1, self.p1_key_up, 1)
                    # p2 stop move up
                    if event.key == self.p2_key_up and player2.moving == 1:
                        player_stop_or_other_direction(player2, self.p2_key_down, 0)
                    # p2 stop move down
                    if event.key == self.p2_key_down and player2.moving == -1:
                        player_stop_or_other_direction(player2, self.p2_key_up, 1)

            self.clock.tick(self.FPS)


if __name__ == "__main__":
    Pong()


def start():
    Pong()
