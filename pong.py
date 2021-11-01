import pygame,threading,time
from button import Text

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)


class Ball:
    def __init__(self,size,screen):
        self.screen = screen
        self.w,self.h = size
        self.block_size = 10
        self.velocity = [5, 2]
        self.pos_x = self.w / 2
        self.pos_y = self.h / 2
        self.rect = pygame.Rect(self.pos_x, self.pos_y, self.block_size, self.block_size)


    def trajectory(self):
        OFFSETX = 30
        OFFSETY = 50
        pos_x,pos_y = self.pos_x, self.pos_y
        velocity_dummy = self.velocity.copy()
        while pos_x > 57:
            pos_x += velocity_dummy[0]
            pos_y += velocity_dummy[1]
            if pos_x + self.block_size > self.w + OFFSETX or pos_x < 0 + OFFSETX:
                velocity_dummy[0] = -velocity_dummy[0]

            if pos_y + self.block_size > self.h + OFFSETY or pos_y < 0 + OFFSETY:
                velocity_dummy[1] = -velocity_dummy[1]
        target = pygame.Rect(pos_x, pos_y, self.block_size, self.block_size)

        return target

    def update(self):
        OFFSETX = 30
        OFFSETY =50
        self.pos_x += self.velocity[0]
        self.pos_y += self.velocity[1]
        val = 0
        if self.pos_x + self.block_size > self.w - OFFSETX+20:
            val = 2
        if self.pos_x + self.block_size < OFFSETX+20:
            val= 1
        if self.pos_x + self.block_size > self.w+OFFSETX or self.pos_x < 0+ OFFSETX:
            self.velocity[0] = -self.velocity[0]

        if self.pos_y + self.block_size > self.h+OFFSETY or self.pos_y < 0+OFFSETY:
            self.velocity[1] = -self.velocity[1]

        self.rect = pygame.Rect(self.pos_x, self.pos_y, self.block_size, self.block_size)
        pygame.draw.rect(self.screen, white, self.rect )
        return val
    def bounce(self):
        self.velocity[0] = -self.velocity[0]
        self.pos_x += self.velocity[0]


class Player:
    def __init__(self, screen, player, size):
        self.score=0
        self.w,self.h = size
        self.screen = screen
        self.factor_speed =4
        self.moving = 0
        if player == 1:
            self.position = (60, self.h//2  , 10, 70)
        else:
            self.position = (self.w - 70, self.h//2, 10, 70)  # left,top,width,height

        self.rect = pygame.Rect(self.position[0], self.position[1], 10, 70)
        self.update()
        self.freeze = 0

    def point(self):
        self.score += 1

    def update(self):

        pygame.draw.rect(self.screen, white, self.position, 5, 3)

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
        if self.position[1] + move_by_size > self.h - 125:
            move_by_size = 0

        self.position = (self.position[0], self.position[1] + move_by_size, 10, 70)
        self.rect = pygame.Rect(self.position[0], self.position[1], 10, 70)
        self.update()
    def move_to_target(self,target):

        if target[1] < self.position[1]:
            self.moving = 1
        else:
            self.moving = -1
        if not self.freeze:
            self.move()


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
        self.p2_key_down =pygame.K_l
        self.FPS = 120
        self.clock = pygame.time.Clock()
        self.size = self.width, self.height = 900, 700
        pygame.init()
        self.screen = pygame.display.set_mode(self.size)

        self.start_screen()

    def start_screen(self):
        BTN_ONEPLAYER = Text(self.screen, red, "One player", self.width//2-100, self.height//2-100)
        BTN_TWOPLAYERS = Text(self.screen, blue, "Two players", self.width // 2-100, self.height // 2-100 + 80)
        BTN_CHANGE_INPUT = Text(self.screen, blue, "Setup input", self.width // 2-100, self.height // 2-100 + 160)

        choose =1
        while choose:
            self.screen.fill(black)
            BTN_ONEPLAYER.update()
            BTN_TWOPLAYERS.update()
            BTN_CHANGE_INPUT.update()
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    choose = 0
                    break
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if BTN_ONEPLAYER.check_click(mouse_pos):
                        self.oneplayer = True
                        self.play()

                    elif BTN_TWOPLAYERS.check_click(mouse_pos):
                        self.oneplayer = False
                        self.play()

                    elif BTN_CHANGE_INPUT.check_click(mouse_pos):
                        if (p:=self.get_key(1,"up")) != -1:
                            self.p1_key_up = p
                        else:
                            break
                        if (p:=self.get_key(1, "down")) != -1:
                            self.p1_key_down = p
                        else:
                            break
                        if (p:=self.get_key(2, "up")) != -1:
                            self.p2_key_up = p
                        else:
                            break
                        if (p:=self.get_key(2, "down")) != -1:
                            self.p2_key_down = p
                        else:
                            break

    def get_key(self,player,movement):
        self.screen.fill(black)
        up_key_p1 = Text(self.screen, white, "Press key to setup Player {} movement {}".format(player,movement.upper()), 100, 100)
        up_key_p1.update()
        pygame.display.update()
        setup = 1
        while setup:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return -1
                if event.type == pygame.KEYDOWN:
                    return event.key

    def draw_line(self,pos1,pos2,width,parts,vertical=False):
        x = pos1[0]
        y = pos1[1]
        border = pos2

        if vertical:
            distance_x = 0
            distance_y = abs(pos2[1]-pos1[1])//parts
            use = y
            border = border[1]
        else:
            distance_x = abs(pos2[0]-pos1[0])//parts
            distance_y = 0
            use = x
            border = border[0]

        while border >= use+distance_y+distance_x:
            pos1 =(pos1[0] , pos1[1])
            pygame.draw.line(self.screen,white,pos1,(pos1[0]+distance_x,pos1[1]+distance_y),width)
            pos1 = (pos1[0]+(distance_x*2), pos1[1]+(distance_y*2))
            use = pos1[0] if not vertical else pos1[1]
        if vertical:
            distance_y = border - pos1[1]
        else:
            distance_x = border - pos1[0]
        pygame.draw.line(self.screen, white, pos1, (pos1[0] + distance_x, pos1[1] + distance_y), width)

    def draw_game_border(self):
        game_rect = pygame.Rect(20, 50, self.width - 40, self.height - 100)
        self.draw_line(game_rect.topleft,game_rect.topright,3,60)
        self.draw_line(game_rect.bottomleft, game_rect.bottomright, 3, 60)
        self.draw_line(game_rect.topleft,game_rect.bottomleft,3,50,True)
        self.draw_line(game_rect.topright, game_rect.bottomright, 3, 60, True)
        middle_x = game_rect.topleft[0] + ((game_rect.topright[0]-game_rect.topleft[0])//2)
        middle_y = game_rect.topleft[1]


        middle_x1=middle_x
        middle_y1 =middle_y+game_rect.size[1]
        self.draw_line((middle_x,middle_y),(middle_x1,middle_y1), 3, 60, True)

    def play(self,player1=0,player2=0):
        game = 1
        player1 = Player(screen=self.screen, player=1, size= self.size) if not player1 else player1
        player2 = Player(screen=self.screen, player=2, size= self.size) if not player2 else player2

        size = self.width - 40, self.height - 100
        ball = Ball(size, self.screen)
        target = pygame.Rect(0,0,0,0)
        while game:
            self.screen.fill(black)

            self.draw_game_border()

            if (b:=ball.update())==1:
                player2.point()
                self.play(player1,player2)
                return

            elif b == 2:
                player1.point()
                self.play(player1,player2)
                return
            TEXT_SCORE_PLAYER1 = Text(self.screen, white, str(player1.score), self.width // 5, 20)
            TEXT_SCORE_PLAYER2 = Text(self.screen, white, str(player2.score), (self.width // 5) * 4, 20)

            TEXT_SCORE_PLAYER1.update()
            TEXT_SCORE_PLAYER2.update()

            player1.update()
            player2.update()

            if self.oneplayer and player1.rect.colliderect(ball.rect) or target.colliderect(pygame.Rect(player1.rect[0],player1.rect[1]+20,player1.rect[2],30)):
                player1.stop()

            player_move(player2)
            player_move(player1)

            if ball.rect.colliderect(player1.rect) or ball.rect.colliderect(player2.rect):
                ball.bounce()
                if self.oneplayer and ball.rect.colliderect(player2.rect):
                    target = ball.trajectory()
                    player1.start()
                    if target[1] < player1.position[1]:
                        player1.moving = 1
                    else:
                        player1.moving = -1

            pygame.display.update()

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    game = 0
                    break
                if event.type == pygame.KEYDOWN:
                    if not self.oneplayer and event.key == self.p1_key_up and player1.moving == 0:
                        player1.start()
                        player1.moving = 1
                    if not self.oneplayer and event.key == self.p1_key_down and player1.moving == 0:
                        player1.start()
                        player1.moving = -1
                    if event.key == self.p2_key_up and player2.moving == 0:
                        player2.start()
                        player2.moving = 1
                    if event.key == self.p2_key_down and player2.moving == 0:
                        player2.start()
                        player2.moving = -1
                if event.type == pygame.KEYUP:
                    if not self.oneplayer and event.key == self.p1_key_up and player1.moving == 1:
                        player_stop_or_other_direction(player1,self.p1_key_down,0)
                    if not self.oneplayer and event.key == self.p1_key_down and player1.moving == -1:
                        player_stop_or_other_direction(player1,self.p1_key_up,1)
                    if event.key == self.p2_key_up and player2.moving == 1:
                        player_stop_or_other_direction(player2, self.p2_key_down, 0)
                    if event.key == self.p2_key_down and player2.moving == -1:
                        player_stop_or_other_direction(player2, self.p2_key_up, 1)

            self.clock.tick(self.FPS)


if __name__ == "__main__":
    Pong()


def start():
    Pong()