from imports import *

class Text:
    def __init__(self,screen,color,text,posx,posy,fontsize=30):
        self.text = text
        self.myfont = pygame.font.Font('slkscr.ttf', fontsize)
        self.textsurface = self.myfont.render(text,False,color)
        self.screen = screen
        self.posx, self.posy = posx,posy
        w,h = self.textsurface.get_size()
        self.rect = pygame.Rect(self.posx, self.posy,w,h )


    def update_color(self,color):
        self.textsurface = self.myfont.render(self.text, False, color)

    def update(self):

        self.screen.blit(self.textsurface, (self.posx, self.posy))

    def check_click(self,mouse_pos):
        mouse = pygame.Rect(mouse_pos[0],mouse_pos[1],10,10)
        return mouse.colliderect(self.rect)