import pygame, time, threading,random

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

    def start(self):
        OFFSETX = 30
        OFFSETY =50
        self.pos_x += self.velocity[0]
        self.pos_y += self.velocity[1]
        if self.pos_x + self.block_size > self.w+OFFSETX or self.pos_x < 0+ OFFSETX:
            self.velocity[0] = -self.velocity[0]

        if self.pos_y + self.block_size > self.h+OFFSETY or self.pos_y < 0+OFFSETY:
            self.velocity[1] = -self.velocity[1]

        self.rect = pygame.Rect(self.pos_x, self.pos_y, self.block_size, self.block_size)
        pygame.draw.rect(self.screen, white, self.rect )
    def bounce(self):
        self.velocity[0] = -self.velocity[0]
        self.pos_x += self.velocity[0]



class player:
    def __init__(self, screen, player, size):
        self.w,self.h = size
        self.screen = screen
        self.factor_speed = 1
        self.moving = 0
        if player == 1:
            self.position = (60, self.h//2  , 10, 70)
        else:
            self.position = (self.w - 70, self.h//2, 10, 70)  # left,top,width,height

        self.rect = pygame.Rect(self.position[0], self.position[1], 10, 70)
        self.update()


    def update(self):
        pygame.draw.rect(self.screen, white, self.position, 5, 3)

    def start(self):
        self.freeze = 0
    def stop(self):
        self.freeze = 1
        self.moving = 0
    def move(self, up):
        while not self.freeze:
            if up:
                self.moving = 1
                move_by_size = -self.factor_speed
            else:
                self.moving = -1
                move_by_size = self.factor_speed

            if self.position[1] + move_by_size < 65:
                move_by_size = 0
            if self.position[1] + move_by_size > self.h - 140:
                move_by_size = 0

            self.position = (self.position[0], self.position[1] + move_by_size, 10, 70)
            self.rect = pygame.Rect(self.position[0], self.position[1], 10, 70)
            self.update()
            time.sleep(0.001)




class pingpong:
    def __init__(self):
        self.FPS = 120
        self.clock = pygame.time.Clock()
        self.size = self.width, self.height = 1100, 600
        pygame.init()
        self.screen = pygame.display.set_mode(self.size)
        self.play()

    def player_move(self, player, up):
        player.start()
        thread = threading.Thread(target=player.move, args=(up,))
        thread.start()

    def player_stop_or_other_direction(self,player,oppositekey,up):
        player.stop()
        keys = pygame.key.get_pressed()
        if keys[oppositekey]:
            time.sleep(0.1)
            self.player_move(player, up)

    def play(self):
        game = 1
        player1 = player(screen=self.screen, player=1, size= self.size)
        player2 = player(screen=self.screen, player=2, size= self.size)
        size = self.width - 40, self.height - 100
        ball = Ball(size, self.screen)

        while game:
            self.screen.fill(black)
            pygame.draw.rect(self.screen, white, (20, 50, self.width - 40, self.height - 100), 3, 3)
            ball.start()
            player1.update()
            player2.update()
            pygame.display.update()

            if ball.rect.colliderect(player1.rect) or ball.rect.colliderect(player2.rect):
                ball.bounce()

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    game = 0
                    break
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_e and player1.moving == 0:
                        self.player_move(player1, 1)
                    if event.key == pygame.K_d and player1.moving == 0:
                        self.player_move(player1, 0)
                    if event.key == pygame.K_o and player2.moving == 0:
                        self.player_move(player2, 1)
                    if event.key == pygame.K_l and player2.moving == 0:
                        self.player_move(player2, 0)
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_e and player1.moving == 1:
                        self.player_stop_or_other_direction(player1,pygame.K_d,0)
                    if event.key == pygame.K_d and player1.moving == -1:
                        self.player_stop_or_other_direction(player1,pygame.K_e,1)
                    if event.key == pygame.K_o and player2.moving == 1:
                        self.player_stop_or_other_direction(player2, pygame.K_l, 0)
                    if event.key == pygame.K_l and player2.moving == -1:
                        self.player_stop_or_other_direction(player2, pygame.K_o, 1)

            self.clock.tick(self.FPS)

if __name__ == "__main__":
    pingpong()
