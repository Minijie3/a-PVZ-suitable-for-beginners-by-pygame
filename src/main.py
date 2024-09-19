import pygame
import sys
import objectbase as ob
from image import *
from pygame import *
from const import *
from game import *

def pvz():
    pygame.init()

    DS=pygame.display.set_mode(WINDOW_SIZE)

    Game = game(DS)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                Game.mouseClickHandler(event.button)

                #  R   B   G    ( maxmum=255, minimum=0 )
        DS.fill( (255,255,255) )

        Game.addFreeSunshine()
        Game.addZombie()
        Game.CheckFight()
        Game.eat()
        Game.CheckCache()
        Game.update()
        Game.lose_game()
        Game.draw()
        pygame.display.update()

if __name__ == '__main__':
    pvz()

