import pygame
from const import *
from pygame.sprite import Group

class Image(pygame.sprite.Sprite):
    def __init__(self, img_pathfmt, img_index, indexcount, img_size, img_pos):
        self.pathfmt=img_pathfmt
        self.index=img_index
        self.indexcount=indexcount
        self.size=img_size
        self.pos=list(img_pos)
        self.UpdateImage()

    def UpdateImage(self):
        path=self.pathfmt
        if self.indexcount != 0:
            path=path % self.index
        self.image=pygame.transform.scale(pygame.image.load(path), self.size)
    
    def UpdateSize(self,size):
        self.size=size
        self.UpdateImage()

    def UpdateIndex(self,index):
        self.index=index
        self.UpdateImage()

    def Get_Rect(self):
        rect=self.image.get_rect()
        rect.x , rect.y = self.pos
        return rect

    def draw(self, DS):
        DS.blit(self.image, self.Get_Rect())

        