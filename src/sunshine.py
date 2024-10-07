import objectbase
import time
from const import *

class sunshine(objectbase.Object):
    def __init__(self, id, img_pos):
        super(sunshine,self).__init__(id, img_pos)
        self.interval_time = 0
        self.interval_cnt = 0
        self.loot_flag = False

    def CheckPos_D(self):
        judgement = super(sunshine,self).CheckPos()
        if judgement and self.pos[1] <= WINDOW_SIZE[1] - 100:
            self.pos[1] += self.get_Data()['SPEED_D']
        else:
            return judgement
        
    def CheckPos_U(self):
        judgement = super(sunshine,self).CheckPos()
        if judgement:
            self.pos[1] -= self.get_Data()['SPEED_U']
        else:
            return judgement
        
    def CheckSummon_interval(self, interval_time):
        if time.time() - self.interval_time <= interval_time and self.interval_cnt == 1:
            return True
        else :
            if self.interval_cnt == 0:
                self.interval_time = time.time()
                self.interval_cnt += 1
            elif self.interval_cnt == 1:
                self.loot_flag = True
            return False

class sunshine_down(sunshine):
    def Move(self):
        self.CheckPos_D()

    def draw(self, DS):
        judgement = self.CheckSummon_interval(self.get_Data()['INTERVAL_DOWN'])
        if judgement:
            super(sunshine_down,self).draw(DS)

class sunshine_summon_sunflower(sunshine):
    def __init__(self, id, img_pos):
        super().__init__(id, img_pos)
        self.cnt = 0
        self.start = img_pos # self.start = self.pos is not good.
    def Move(self):
        if self.start[1] - self.pos[1] <= 30 and self.cnt == 0 :
            self.CheckPos_U()
            if self.start[1] - self.pos[1] >= 30:
                self.cnt = 1
        elif self.cnt == 1 and self.pos[1] - self.start[1] + 10 < 42 :
            self.CheckPos_D()
        elif self.pos[1]- self.start[1] + 10 >= 42 :
            pass
    def draw(self, DS):
        judgement = self.CheckSummon_interval(self.get_Data()['INTERVAL_SUMMON_SUNFLOWER'])
        if judgement:
            super(sunshine_summon_sunflower,self).draw(DS)

            