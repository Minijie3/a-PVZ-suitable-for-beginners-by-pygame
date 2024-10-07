import pygame
import objectbase as ob
import peashooter
import sunshine
import sunflower
import zombiebase as zom
import random
import time
import image
from const import *

class game(object):
    def __init__(self, DS) :
        self.window = DS
        self.gold = 100
        self.goldfont = pygame.font.Font(None, 60)
        self.zomcnt = 0
        self.zombieGenTime = time.time()
        self.freeSunshineGenTime = time.time()
        self.back = ob.Object(0, (0,0))
        self.lose = image.Image(LOSE_PATH, 0, 0, WINDOW_SIZE, (0,0))
        self.begin_page = image.Image(BEGIN_PATH, 0, 0, WINDOW_SIZE, (0,0))
        self.begin_button = image.Image(BEGIN_BUTTON_PATH, 0, 0, BEGIN_BUTTON_SIZE, BEGIN_BUTTON_POS)
        self.islose = False
        self.isbegin = False
        self.plants = []
        self.zombies = []
        self.others = []
        self.summons = []

        self.Hasplant = []
        for i in range(GRID_CNT[0]):
            col = []
            for j in range(GRID_CNT[1]):
                col.append(0)
            self.Hasplant.append(col)
    def CheckAddPlant(self, gridIndex, plantID):
        if gridIndex[0] < 0 or gridIndex[1] < 0 or gridIndex[0] > GRID_CNT[0] - 1 or gridIndex[1] >= GRID_CNT[1]:
            return
        elif self.Hasplant[gridIndex[0]][gridIndex[1]] == 1:
            return  
        else:
            self.Hasplant[gridIndex[0]][gridIndex[1]] = 1
        if plantID == NORM_SUNFLOWER_ID:
            self.addSunflower(gridIndex)
        if plantID == NORM_PEASHOOTER_ID:
            self.addPeashooter(gridIndex)
    def addSunflower(self, gridIndex):
        addPos = (LEFT_TOP[0] + gridIndex[0] * GRID_SIZE[0], LEFT_TOP[1] + gridIndex[1] * GRID_SIZE[1])
        item = sunflower.sunflower(NORM_SUNFLOWER_ID, addPos)
        if self.judge_price(item):
            self.plants.append(item)
            self.gold -= item.get_price()

    def addPeashooter(self, gridIndex):
        addPos = (LEFT_TOP[0] + gridIndex[0] * GRID_SIZE[0], LEFT_TOP[1] + gridIndex[1] * GRID_SIZE[1])
        item = peashooter.peashooter(NORM_PEASHOOTER_ID, addPos)
        if self.judge_price(item):
            self.plants.append(item)
            self.gold -= item.get_price()

    def addZombie(self):
        flag = self.zomcnt // 4
        zomtime = 15 - flag if (15 - flag) > 5 else 5
        if time.time() - self.zombieGenTime > zomtime: 
            addPos = (WINDOW_SIZE[0], LEFT_TOP[1] + random.randint(0, 4) * GRID_SIZE[1])
            item = zom.zombiebaseob(NORM_ZOMBIE_ID, addPos)
            self.zombies.append(item)
            self.zombieGenTime = time.time()
            self.zomcnt += 1

    def addFreeSunshine(self):
        if time.time() - self.freeSunshineGenTime > 8: 
            addPos = (random.randint(LEFT_TOP[0], LEFT_TOP[0] + (GRID_CNT[0] - 1) * GRID_SIZE[0]), 0)
            item = sunshine.sunshine_down(SUNSHINE_ID, addPos)
            self.others.append(item)
            self.freeSunshineGenTime = time.time()

    def renew(self,obj):
        obj.update()
        if obj.hassummon:
            item = obj.Summon() # Using 'item' is necessary.
            if item != None:
                self.summons.append(item)

    def update(self):
        for plant in self.plants:
            self.renew(plant)
        for zombie in self.zombies:
            self.renew(zombie)
        for other in self.others:
            self.renew(other)
        for summon in self.summons:
            self.renew(summon)

    def draw(self):
        if not self.isbegin:
            self.begin_page.draw(self.window)
            self.begin_button.draw(self.window)
        elif not self.islose and self.isbegin:
            self.back.draw(self.window)
            for plant in self.plants:
                plant.draw(self.window)
            for zombie in self.zombies:
                zombie.draw(self.window)
            for other in self.others:
                other.draw(self.window)
            for summon in self.summons:
                summon.draw(self.window)
            self.renderfont()
        elif self.islose:
            self.lose.draw(self.window)

    def renderfont(self):
        textImage = self.goldfont.render('Gold:' + str(self.gold), True, (255, 255, 255))
        self.window.blit(textImage, (13, 23))
    def mouseClickHandler(self, btn):
        if self.islose:
            return
        mousePos = pygame.mouse.get_pos()
        if not self.isbegin:
            self.begin_game(mousePos)
            return 
        lootcheck_summon = self.CheckLoot_summon(mousePos)
        lootcheck_other = self.CheckLoot_other(mousePos)
        if lootcheck_summon or lootcheck_other: # If there is happening a loot, ignore other things.
            return
        gridIndex = self.posGridIndex(mousePos)
        if btn == 1: # Left button
            self.CheckAddPlant(gridIndex, NORM_SUNFLOWER_ID)
        if btn == 3: # Right button
            self.CheckAddPlant(gridIndex, NORM_PEASHOOTER_ID)
        if btn == 2: # Middle button
            self.CheckEradicate(mousePos)
    def CheckLoot_summon(self, mousePos):
        for summon in self.summons:
            if summon.CheckCanLoot():
                rect = summon.Get_Rect()
                if rect.collidepoint(mousePos):
                    if summon.get_type() == 'SUNSHINE':
                        self.gold += summon.get_price()
                    self.summons.remove(summon)
                    return True
            else:
                continue # Cannot write return False cause it's a circulate, but beabullet is also a summon.
            
    def CheckLoot_other(self, mousePos):
        for other in self.others:
            rect = other.Get_Rect()
            if rect.collidepoint(mousePos):
                if other.get_type() == 'SUNSHINE':
                    self.gold += other.get_price()
                self.others.remove(other)
                return True
            else:
                return False # Here can be written return False.
    def CheckEradicate(self, mousePos):
        for plant in self.plants:
            rect = plant.Get_Rect()
            if rect.collidepoint(mousePos):
                remove_index = self.posGridIndex(plant.pos)
                self.Hasplant[remove_index[0]][remove_index[1]] = 0
                self.plants.remove(plant)

    def CheckFight(self):
        for zombie in self.zombies:
            for summon in self.summons:
                if zombie.Get_Rect().colliderect(summon.Get_Rect()):
                    self.fight(summon, zombie)

    def posGridIndex(self, mousePos):
        x = ( mousePos[0] - LEFT_TOP[0] ) // GRID_SIZE[0]
        y = ( mousePos[1] - LEFT_TOP[1] ) // GRID_SIZE[1]
        return (x, y)

    def judge_price(self, item):
        if self.gold < item.get_price():
            return False
        else:
            return True
    
    def fight(self, summon, zombie):
        if summon.get_type() == 'NORM_PEABULLET':
            zombie.hp -= summon.attack
            summon.hp -= zombie.attack
            if zombie.hp <= 0:
                self.zombies.remove(zombie)
            if summon.hp <= 0:
                self.summons.remove(summon)

    def eat(self):
        for zombie in self.zombies:
            z_rect = zombie.Get_Rect()
            z_rect.width -= 45
            z_rect.height -= 45
            for plant in self.plants:
                p_rect = plant.Get_Rect()
                p_rect.width -= 45
                p_rect.height -= 45
                if z_rect.colliderect(p_rect):
                    zombie.eat_flag = True
                    plant.hp -= zombie.attack
                    if plant.hp <= 0:
                        self.plants.remove(plant)
                else:
                    zombie.eat_flag = False

    def CheckCache(self):
        for summon in self.summons:
            if summon.get_type() == 'SUNSHINE':
                if summon.loot_flag:
                    self.summons.remove(summon)
            if summon.get_type() == 'NORM_PEABULLET':
                if summon.pos[0] > WINDOW_SIZE[0]:
                    self.summons.remove(summon)
        for other in self.others:
            if other.get_type() == 'SUNSHINE':
                if other.loot_flag:
                    self.others.remove(other)

    def begin_game(self,mousePos):
        rect = self.begin_button.Get_Rect()
        if rect.collidepoint(mousePos):
            self.isbegin = True
        self.zombieGenTime = time.time()
        self.freeSunshineGenTime = time.time()

    def lose_game(self):
        for zombie in self.zombies:
            if zombie.pos[0] <= 220:
                self.islose = True

