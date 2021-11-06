from _imports_ import *
import random
import time
from _text_ import Text


class Grid:
    def __init__(self,screen,size):
        rects=[]
        self.reward = False
        self.reward_rect = False
        self.rect_grid=[]
        self.screen = screen
        self.my_dict = dict()
        self.size = size
        for x in np.arange(0,size[0]-15,15):
            for y in np.arange(15, size[1]-15, 15):
                rects.append(pygame.Rect(x,y,15,15))
                pygame.draw.rect(self.screen,blue, (x,y,15,15),1,1)
                if x != 0:
                    self.my_dict[(x,y)]=0
            rects=[]
            self.rect_grid.append(rects)
    def fill_square(self,key):
        self.my_dict[key] = not self.my_dict[key]
    def draw_grid(self):
        pygame.draw.rect(self.screen, white, (15, 15, self.size[0] - 25, self.size[1] - 25), 1, 1)
        for key, value in self.my_dict.items():
            x, y = key
            if value == 0:
                continue

            if key == (self.reward_rect.x,self.reward_rect.y):
                pygame.draw.rect(self.screen, blue, (x, y, 15, 15))

            else:
                pygame.draw.rect(self.screen, white, (x, y, 15, 15))
                pygame.draw.rect(self.screen, black, (x, y, 15, 15), 1, 1)

    def next_to_me(self,relative_item,up=False,down=False,left=False,right=False):

        for i,column in enumerate(self.rect_grid):
            if i==0:
                borderleft=True
            else:
                borderleft=False

            if i == len(self.rect_grid) - 2:
                borderright =True
            else:
                borderright=False

            for j,item in enumerate(column):
                if j == 0:
                    bordertop = True
                else:
                    bordertop=False
                if j == len(column) - 1:
                    borderbot= True
                else:
                    borderbot=False

                if item.x==relative_item[0] and item.y == relative_item[1]:
                    if down and borderbot:
                        return -1
                    if up and bordertop:
                        return -1
                    if left and borderleft:
                        return -1
                    if right and borderright:
                        return -1
                    if down:
                        return self.rect_grid[i][j+1]
                    if up:
                        return self.rect_grid[i][j-1]
                    if left:
                        return self.rect_grid[i-1][j]
                    if right:

                        return self.rect_grid[i+1][j]

    def spawn_reward(self):
        if not self.reward:
            shuffled_dict = [(i,v) for i,v in self.my_dict.items()]
            random.shuffle(shuffled_dict)
            for key,val in shuffled_dict:
                if self.my_dict[key] == 0:
                    self.reward_rect = pygame.Rect(key[0],key[1],15,15)
                    self.fill_square(key)
                    break

            self.reward = True


class Snake:
    def __init__(self,size,grid):
            self.score = 1
            self.grid = grid
            self.size = size

            self.position = (choice([a for a in range(15*5, size[0]-15*2, 15)]), choice([a for a in range(15*5, size[1]-(15*5), 15)]))
            self.rect = pygame.Rect(self.position[0], self.position[1], 15, 15)
            self.positions = [self.position]
            pos = self.position
            for _ in range(4):
                rect_down = grid.next_to_me(pos,down=1)

                position_below = (rect_down.x,rect_down.y)
                self.positions.append(position_below)
                pos=position_below

            for pos in self.positions:
                grid.fill_square(pos)
            self.moving = [0,0,1,0] # up,down,left,right


    def move(self):
            up,down,left,right = self.moving
            rect_next_to_me = self.grid.next_to_me(self.position,up,down,left,right)
            if rect_next_to_me == -1:
                return -1
            possition_next_to_me =rect_next_to_me.x,rect_next_to_me.y
            for pos in self.positions:

                rect = pygame.Rect(pos[0],pos[1],15,15)
                if rect==self.rect:
                    continue
                if rect_next_to_me.colliderect(rect):
                    return -1
            self.position = possition_next_to_me
            self.rect = pygame.Rect(self.position[0], self.position[1], 15, 15)

            if self.rect.colliderect(self.grid.reward_rect):
                self.grid.reward = False
                self.grid.fill_square(self.position)
                self.grid.fill_square(self.positions[-1])
                self.positions.append(self.positions[-1])
                self.score += 1



            self.positions.insert(0,self.position)
            self.grid.fill_square(self.position)
            self.grid.fill_square(self.positions.pop())


    def rotate(self,up=False,down=False,left=False,right=False):
        finish =False
        if up and self.moving[1] != 1:
            finish=1
        if down and self.moving[0] != 1:
            finish = 1
        if left and self.moving[3] != 1:
            finish = 1
        if right and self.moving[2] != 1:
            finish = 1
        if finish:
            self.moving = [up,down,left,right]
            self.move()
        else:
            return -1


class SnakeGame:
    def __init__(self):
        self.FPS = 120
        self.clock = pygame.time.Clock()
        self.size = self.width, self.height = 700, 550
        pygame.init()
        self.screen = pygame.display.set_mode(self.size)
        self.play()

    def play(self):
        game =1
        grid = Grid(self.screen, self.size)
        grid.spawn_reward()
        snake = Snake(self.size, grid)
        time_before = time.time()
        while game:
            self.screen.fill(black)
            score_txt = str(snake.score)
            score = Text(self.screen, white,score_txt, self.size[0] // 2, 20, 20)
            score.update()
            grid.draw_grid()
            grid.spawn_reward()
            if time.time()-time_before > 0.09:
                if snake.move() == -1:
                    self.play()
                    return
                time_before=time.time()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game = 0
                    return
                if event.type == pygame.KEYDOWN:
                    keys = [0,0,0,0]
                    if event.key == pygame.K_ESCAPE:
                        game = 0
                        break
                    if event.key == pygame.K_UP:
                        keys[0] = 1

                    if event.key == pygame.K_DOWN:
                        keys[1] = 1

                    if event.key == pygame.K_LEFT:
                        keys[2] = 1

                        time_before = time.time()
                    if event.key == pygame.K_RIGHT:
                        keys[3] = 1
                    if sum(keys) != 0:
                        up,down,left,right = keys
                        p = snake.rotate(up=up,down=down,left=left,right=right)
                        if p != -1:
                            time_before = time.time()

            # UPDATE DISPLAY
            pygame.display.update()
            self.clock.tick(self.FPS)

if __name__=="__main__":
    s = SnakeGame()

def start():
    s= SnakeGame()